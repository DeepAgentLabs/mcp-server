"""Isolated HTTP worker for a hard total Tower request deadline.

The parent sends credentials on stdin, never command-line arguments. Only bounded
JSON results leave this worker; redirects and raw server error bodies are refused.
"""

import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> None:
        return None


def request(payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload["arguments"]).encode() if payload["write"] else None
    req = Request(
        payload["url"],
        data=body,
        method="POST" if payload["write"] else "GET",
        headers={"Authorization": "Bearer " + payload["token"], "Content-Type": "application/json"},
    )
    try:
        with build_opener(NoRedirect()).open(req, timeout=9) as response:
            data = response.read(1024 * 1024 + 1)
            if len(data) > 1024 * 1024:
                return {"ok": False, "error": "Tower response exceeds connector limit"}
            return {"ok": True, "data": json.loads(data)}
    except HTTPError as exc:
        return {"ok": False, "error": f"Tower HTTP {exc.code}"}
    except (URLError, OSError, ValueError):
        return {"ok": False, "error": "Tower unavailable or invalid response"}


if __name__ == "__main__":
    try:
        result = request(json.loads(sys.stdin.buffer.read(65537)))
    except Exception:
        result = {"ok": False, "error": "Invalid Tower HTTP request"}
    print(json.dumps(result))
