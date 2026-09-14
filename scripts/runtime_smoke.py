#!/usr/bin/env python3
"""Manual, bounded MCP smoke client; never run automatically in CI.

Only use a reviewed server and an explicitly selected read-only tool. A tool response
is recorded for human review, not automatically certified as a successful live call.
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

PROTOCOL = "2025-06-18"
SUPPORTED_PROTOCOLS = {PROTOCOL, "2025-03-26", "2024-11-05"}
MAX_BYTES = 2 * 1024 * 1024
CLIENT = {"name": "sweden-catalog-runtime-smoke", "version": "1.0"}


def safe_environment(state: Path, executable_dirs: list[str] | None = None) -> dict[str, str]:
    """Allowlist non-secret process settings; never inherit user credentials/config."""
    state.mkdir(parents=True, exist_ok=True)
    environment = {
        key: os.environ[key]
        for key in ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "SYSTEMDRIVE")
        if key in os.environ
    }
    paths = list(executable_dirs or []) + [str(Path(sys.executable).parent)]
    if "SYSTEMROOT" in environment:
        paths += [str(Path(environment["SYSTEMROOT"]) / "System32"), environment["SYSTEMROOT"]]
    environment["PATH"] = os.pathsep.join(paths)
    for key in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "TEMP", "TMP"):
        directory = state / key.lower()
        directory.mkdir(exist_ok=True)
        environment[key] = str(directory)
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"):
        value = os.environ.get(key) or os.environ.get(key.lower())
        if value:
            if key != "NO_PROXY" and (urlsplit(value).username or urlsplit(value).password):
                raise ValueError("Authenticated proxy requires separate authorization; not inherited")
            environment[key] = value
    environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", "PYTHONNOUSERSITE": "1", "PYTHON_DOTENV_DISABLED": "1",
                        "NEXT_TELEMETRY_DISABLED": "1", "DO_NOT_TRACK": "1", "NO_COLOR": "1", "CI": "1"})
    return environment


def response_result(payload: object, request_id: int) -> dict:
    if not isinstance(payload, dict) or payload.get("jsonrpc") != "2.0" or payload.get("id") != request_id:
        raise ValueError("Unexpected JSON-RPC response or request id")
    if "error" in payload:
        error = payload["error"]
        raise ValueError(f"JSON-RPC error: {json.dumps(error, ensure_ascii=True)[:600]}")
    result = payload.get("result")
    if not isinstance(result, dict):
        raise ValueError("JSON-RPC result is not an object")
    return result


def read_http_response(response, request_id: int, timeout: float = 25) -> object:
    content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
    deadline = time.monotonic() + timeout
    total, pending, data = 0, b"", []
    # read1 returns available bytes without waiting for a complete SSE line. This
    # lets the elapsed-time bound stop streams that send endless heartbeats.
    while True:
        if time.monotonic() >= deadline:
            raise TimeoutError("HTTP response exceeded elapsed-time limit")
        chunk = response.read1(8192)
        total += len(chunk)
        if total > MAX_BYTES:
            raise ValueError("Oversized HTTP response")
        pending += chunk
        if content_type == "text/event-stream":
            while b"\n" in pending:
                line, pending = pending.split(b"\n", 1)
                line = line.rstrip(b"\r")
                if not line and data:
                    payload = json.loads(b"\n".join(data))
                    data = []
                    if isinstance(payload, dict) and payload.get("id") == request_id:
                        return payload
                elif line.startswith(b"data:"):
                    data.append(line[5:].lstrip())
        if not chunk:
            if content_type != "text/event-stream":
                if not pending:
                    raise ValueError("Empty HTTP response")
                return json.loads(pending)
            raise ValueError("SSE ended without matching JSON-RPC response")


class HttpClient:
    def __init__(self, url: str, timeout: float = 25, opener=urlopen):
        self.url, self.timeout, self.opener = url, timeout, opener
        self.session = None
        self.protocol = None

    def send(self, message: dict) -> dict | None:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
                   "User-Agent": "sweden-catalog-runtime-smoke/1.0"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        if self.protocol:
            headers["MCP-Protocol-Version"] = self.protocol
        request = Request(self.url, data=json.dumps(message).encode(), headers=headers, method="POST")
        try:
            with self.opener(request, timeout=self.timeout) as response:
                if response.headers.get("Mcp-Session-Id"):
                    self.session = response.headers["Mcp-Session-Id"]
                if "id" not in message:
                    return None
                return response_result(read_http_response(response, message["id"], self.timeout), message["id"])
        except HTTPError as error:
            body = error.read(800).decode("utf-8", "replace")
            raise ValueError(f"HTTP {error.code}: {body[:600]}") from error

    def close(self):
        # Do not issue DELETE to external endpoints; the session expires server-side.
        pass


class StdioClient:
    def __init__(self, command: list[str], cwd: Path, state: Path, timeout: float = 25,
                 executable_dirs: list[str] | None = None, environment: dict[str, str] | None = None):
        self.timeout = timeout
        self.protocol = None
        self.messages = queue.Queue(maxsize=256)
        self.stderr = bytearray()
        env = safe_environment(state, executable_dirs)
        env.update(environment or {})
        self.process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.threads = [threading.Thread(target=self._stdout, daemon=True),
                        threading.Thread(target=self._stderr, daemon=True)]
        for thread in self.threads:
            thread.start()

    def _stdout(self):
        while True:
            line = self.process.stdout.readline(MAX_BYTES + 1)
            if not line:
                try:
                    self.messages.put_nowait(None)
                except queue.Full:
                    pass
                break
            try:
                if len(line) > MAX_BYTES:
                    raise ValueError("Oversized stdio message")
                self.messages.put_nowait(json.loads(line))
            except (ValueError, queue.Full) as error:
                try:
                    self.messages.put_nowait(ValueError(f"Invalid or excessive stdio output: {str(error)[:200]}"))
                except queue.Full:
                    pass
                break

    def _stderr(self):
        while True:
            data = self.process.stderr.read1(1024)
            if not data:
                break
            if len(self.stderr) < 16384:
                self.stderr.extend(data[:16384-len(self.stderr)])

    def send(self, message: dict) -> dict | None:
        self.process.stdin.write(json.dumps(message).encode() + b"\n")
        self.process.stdin.flush()
        if "id" not in message:
            return None
        deadline = time.monotonic() + self.timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Timed out waiting for MCP response")
            try:
                payload = self.messages.get(timeout=remaining)
            except queue.Empty as error:
                raise TimeoutError("Timed out waiting for MCP response") from error
            if payload is None:
                raise ValueError(f"Server exited before response (exit={self.process.poll()})")
            if isinstance(payload, Exception):
                raise payload
            if isinstance(payload, dict) and "id" not in payload:
                continue
            return response_result(payload, message["id"])

    def close(self):
        if self.process.poll() is None:
            if os.name == "nt":
                subprocess.run([str(Path(os.environ["SYSTEMROOT"]) / "System32" / "taskkill.exe"),
                                "/PID", str(self.process.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
            else:
                self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=10)
        for thread in self.threads:
            thread.join(timeout=2)
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            try:
                stream.close()
            except OSError:
                pass


def smoke(client, tool: str | None = None, arguments: dict | None = None) -> dict:
    report = {"started_at": datetime.now(timezone.utc).isoformat(), "client": CLIENT,
              "requested_protocol": PROTOCOL, "phases": {}, "status": "failed"}
    phase = "initialize"
    try:
        result = client.send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": CLIENT}})
        protocol = result.get("protocolVersion")
        if protocol not in SUPPORTED_PROTOCOLS:
            raise ValueError(f"Unsupported negotiated protocol: {protocol}")
        client.protocol = protocol
        report["negotiated_protocol"] = protocol
        report["server_info"] = result.get("serverInfo")
        report["phases"][phase] = "passed"
        phase = "initialized_notification"
        client.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        report["phases"][phase] = "sent"
        phase = "tools_list"
        tools = []
        cursor = None
        for page in range(5):
            result = client.send({"jsonrpc": "2.0", "id": 2 + page, "method": "tools/list",
                                  "params": {"cursor": cursor} if cursor else {}})
            if not isinstance(result.get("tools"), list) or any(
                not isinstance(item, dict) or not isinstance(item.get("name"), str)
                for item in result["tools"]
            ):
                raise ValueError("tools/list did not return valid tool objects")
            tools.extend(result["tools"])
            cursor = result.get("nextCursor")
            if not cursor:
                break
        else:
            raise ValueError("Tool pagination exceeded five-page limit")
        report["phases"][phase] = "passed"
        report["tools"] = tools
        report["status"] = "partial_tools_only"
        if tool:
            phase = "tool_call"
            if tool not in [item.get("name") for item in tools]:
                raise ValueError("Selected tool is not advertised by tools/list")
            report["tool_call"] = {"name": tool, "arguments": arguments or {}}
            result = client.send({"jsonrpc": "2.0", "id": 20, "method": "tools/call",
                                  "params": report["tool_call"]})
            report["tool_result"] = result
            if result.get("isError"):
                raise ValueError("tools/call returned isError=true")
            report["phases"][phase] = "response_received"
            report["status"] = "tool_response_requires_review"
    except (OSError, ValueError, TimeoutError) as error:
        report["status"] = "failed"
        report["failed_phase"] = phase
        report["error"] = str(error)[:1000]
    finally:
        client.close()
        if hasattr(client, "stderr"):
            report["stderr_excerpt"] = bytes(client.stderr).decode("utf-8", "replace")[:2000]
        report["completed_at"] = datetime.now(timezone.utc).isoformat()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--endpoint")
    source.add_argument("--command-json", help="JSON array of a reviewed executable and arguments")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--state", type=Path)
    parser.add_argument("--tool", help="An explicitly reviewed read-only tool; never automatically chosen")
    parser.add_argument("--arguments", default="{}")
    parser.add_argument("--timeout", type=float, default=25)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.endpoint:
        client = HttpClient(args.endpoint, args.timeout)
    else:
        if not args.state:
            parser.error("--state is required for an isolated stdio process")
        command = json.loads(args.command_json)
        client = StdioClient(command, args.cwd, args.state, args.timeout, [str(Path(command[0]).parent)])
    report = smoke(client, args.tool, json.loads(args.arguments))
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "phases", "error") if key in report}))
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
