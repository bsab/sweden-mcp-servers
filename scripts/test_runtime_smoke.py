"""Deterministic protocol checks; no external servers or credentials."""

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime_smoke import HttpClient, StdioClient, read_http_response, response_result, safe_environment, smoke


class Response(io.BytesIO):
    def __init__(self, payload, content_type="application/json", session=None):
        super().__init__(payload if isinstance(payload, bytes) else json.dumps(payload).encode())
        self.headers = {"Content-Type": content_type}
        if session:
            self.headers["Mcp-Session-Id"] = session


def rpc(request_id, result):
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


class FakeClient:
    def __init__(self, result=None, tools=None):
        self.messages = []
        self.closed = False
        self.result = result if result is not None else {"content": [{"type": "text", "text": "fixture"}]}
        self.tools = tools if tools is not None else [{"name": "read_public"}]

    def send(self, message):
        self.messages.append(message)
        if message["method"] == "initialize":
            return {"protocolVersion": "2025-06-18", "serverInfo": {"name": "fixture", "version": "1"}}
        if message["method"] == "tools/list":
            return {"tools": self.tools}
        if message["method"] == "tools/call":
            return self.result
        return None

    def close(self):
        self.closed = True


class RuntimeSmokeTests(unittest.TestCase):
    def test_environment_excludes_credentials_and_redirects_state(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
            "GITHUB_TOKEN": "not-real", "AWS_SECRET_ACCESS_KEY": "not-real", "NODE_OPTIONS": "untrusted",
            "PYTHONPATH": "untrusted", "HTTP_PROXY": "", "HTTPS_PROXY": "", "ALL_PROXY": "",
            "http_proxy": "", "https_proxy": "", "all_proxy": "",
        }, clear=False):
            env = safe_environment(Path(directory))
            for name in ("GITHUB_TOKEN", "AWS_SECRET_ACCESS_KEY", "NODE_OPTIONS", "PYTHONPATH"):
                self.assertNotIn(name, env)
            for name in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "TEMP", "TMP"):
                self.assertTrue(Path(env[name]).is_relative_to(directory))
            self.assertEqual(env["PYTHON_DOTENV_DISABLED"], "1")

    def test_authenticated_proxy_is_not_inherited(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"HTTPS_PROXY": "http://user:password@proxy.invalid"}):
            with self.assertRaisesRegex(ValueError, "Authenticated proxy"):
                safe_environment(Path(directory))

    def test_jsonrpc_rejects_wrong_id_and_errors(self):
        for payload in (rpc(99, {}), {"jsonrpc": "2.0", "id": 1, "error": {"code": -1}}, rpc(1, [])):
            with self.assertRaises(ValueError):
                response_result(payload, 1)

    def test_http_negotiation_session_notification_and_pagination(self):
        requests = []
        responses = [
            Response(rpc(1, {"protocolVersion": "2025-03-26", "serverInfo": {"name": "fixture"}}), session="opaque-fixture"),
            Response(b""),
            Response(b': heartbeat\n\ndata: {"jsonrpc":"2.0","method":"notifications/progress"}\n\n' +
                     b'data: ' + json.dumps(rpc(2, {"tools": [{"name": "first"}], "nextCursor": "next"})).encode() + b'\n\n', "text/event-stream"),
            Response(rpc(3, {"tools": [{"name": "read_public"}]})),
            Response(rpc(20, {"content": [{"type": "text", "text": "fixture, not live evidence"}]})),
        ]

        def opener(request, timeout):
            requests.append(request)
            return responses.pop(0)

        report = smoke(HttpClient("https://example.invalid/mcp", opener=opener), "read_public", {"limit": 1})
        self.assertEqual(report["status"], "tool_response_requires_review")
        self.assertEqual(len(report["tools"]), 2)
        self.assertEqual(report["negotiated_protocol"], "2025-03-26")
        headers = {key.lower(): value for key, value in requests[1].header_items()}
        self.assertEqual(headers["mcp-session-id"], "opaque-fixture")
        self.assertEqual(headers["mcp-protocol-version"], "2025-03-26")
        self.assertNotIn("id", json.loads(requests[1].data))
        self.assertEqual(json.loads(requests[3].data)["params"], {"cursor": "next"})
        self.assertNotIn("opaque-fixture", json.dumps(report))

    def test_sse_requires_matching_response(self):
        response = Response(b'data: {"jsonrpc":"2.0","id":9,"result":{}}\n\n', "text/event-stream")
        with self.assertRaisesRegex(ValueError, "without matching"):
            read_http_response(response, 1)

    def test_response_size_and_elapsed_bounds(self):
        with patch("runtime_smoke.MAX_BYTES", 16):
            with self.assertRaisesRegex(ValueError, "Oversized"):
                read_http_response(Response(b"x" * 17), 1)
        with patch("runtime_smoke.time.monotonic", side_effect=[0, 0, 26]):
            with self.assertRaisesRegex(TimeoutError, "elapsed"):
                read_http_response(Response(b": heartbeat\n\n", "text/event-stream"), 1)

    def test_tool_error_is_failure_not_success(self):
        client = FakeClient({"isError": True, "content": [{"type": "text", "text": "upstream failed"}]})
        report = smoke(client, "read_public")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["failed_phase"], "tool_call")
        self.assertTrue(client.closed)

    def test_empty_nonerror_result_still_requires_review(self):
        self.assertEqual(smoke(FakeClient({}), "read_public")["status"], "tool_response_requires_review")

    def test_tools_only_is_partial_and_never_chooses_a_tool(self):
        client = FakeClient()
        self.assertEqual(smoke(client)["status"], "partial_tools_only")
        self.assertNotIn("tools/call", [message["method"] for message in client.messages])
        self.assertTrue(client.closed)

    def test_unadvertised_tool_is_not_called(self):
        client = FakeClient()
        report = smoke(client, "not_advertised")
        self.assertEqual(report["status"], "failed")
        self.assertNotIn("tools/call", [message["method"] for message in client.messages])

    def test_malformed_tools_fail_with_phase(self):
        report = smoke(FakeClient(tools=["not-a-tool-object"]))
        self.assertEqual(report["failed_phase"], "tools_list")

    def test_pagination_is_bounded(self):
        client = FakeClient()
        send = client.send

        def paginated(message):
            if message["method"] == "tools/list":
                return {"tools": [], "nextCursor": "again"}
            return send(message)

        client.send = paginated
        report = smoke(client)
        self.assertEqual(report["failed_phase"], "tools_list")
        self.assertIn("five-page", report["error"])

    def test_reviewed_fixture_stdio_and_cleanup(self):
        source = '''import json, sys
print("fixture diagnostic", file=sys.stderr, flush=True)
for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request: continue
    method = request["method"]
    result = ({"protocolVersion": "2025-06-18", "serverInfo": {"name": "fixture"}}
              if method == "initialize" else {"tools": [{"name": "read_public"}]}
              if method == "tools/list" else {"content": [{"type": "text", "text": "fixture"}]})
    print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
'''
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "fixture.py"
            script.write_text(source, encoding="utf-8")
            client = StdioClient([sys.executable, str(script)], root, root / "state", timeout=5)
            report = smoke(client, "read_public")
            self.assertEqual(report["status"], "tool_response_requires_review")
            self.assertIn("fixture diagnostic", report["stderr_excerpt"])
            self.assertIsNotNone(client.process.poll())
            self.assertTrue(all(not thread.is_alive() for thread in client.threads))

    def test_stdout_pollution_fails_protocol(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            client = StdioClient([sys.executable, "-c", "print('not JSON', flush=True)"], root, root / "state", timeout=5)
            report = smoke(client)
            self.assertEqual(report["failed_phase"], "initialize")
            self.assertEqual(report["status"], "failed")
            self.assertIsNotNone(client.process.poll())


if __name__ == "__main__":
    unittest.main()
