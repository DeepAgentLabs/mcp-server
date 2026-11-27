"""Exercise consent in Chromium, including browser-generated Origin and cookies.

HTTPS requests are bridged into an isolated ASGI app. No live accounts, network
MCP services or credentials are used. Install the browser extra and Chromium.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from urllib.parse import parse_qs, urlencode, urlsplit

from playwright.sync_api import Request as BrowserRequest
from playwright.sync_api import Route as BrowserRoute
from playwright.sync_api import sync_playwright
from starlette.testclient import TestClient

from deep_agentic_core_mcp.oauth import COOKIE, OAuthConfig
from deep_agentic_core_mcp.services.oauth_store import MemoryOAuthStore
from deep_agentic_core_mcp.services.remote_sessions import MemorySessionStore
from deep_agentic_core_mcp.transport_http import create_app

ORIGIN = "https://mcp.example.com"
CALLBACK = "https://chatgpt.com/connector_platform_oauth_redirect"
KEY = "a" * 40
VERIFIER = "v" * 64


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser-executable")
    parser.add_argument("--screenshot-dir")
    args = parser.parse_args()
    config = OAuthConfig(
        ORIGIN, {"browser-test": {"name": "Browser test", "redirect_uris": [CALLBACK]}}
    )
    app = create_app(
        api_keys={"browser-user": KEY},
        store=MemorySessionStore(),
        oauth_config=config,
        oauth_store=MemoryOAuthStore(),
        allowed_hosts=["mcp.example.com"],
    )
    with TestClient(app, base_url=ORIGIN) as client, sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=args.browser_executable, headless=True, args=["--no-sandbox"]
        )
        try:
            for decision in ("allow", "deny"):
                page = browser.new_page()
                submitted = []

                def bridge(
                    route: BrowserRoute,
                    request: BrowserRequest,
                    submitted: list[dict[str, str]] = submitted,
                ) -> None:
                    if urlsplit(request.url).path == "/favicon.ico":
                        route.fulfill(status=204)
                        return
                    if urlsplit(request.url).netloc != "mcp.example.com":
                        route.fulfill(status=200, body="OAuth callback received")
                        return
                    headers = request.all_headers()
                    if request.method == "POST":
                        submitted.append(headers)
                    response = client.request(
                        request.method,
                        request.url,
                        headers=headers,
                        content=request.post_data_buffer,
                        follow_redirects=False,
                    )
                    route.fulfill(
                        status=response.status_code,
                        headers=dict(response.headers),
                        body=response.content,
                    )

                page.route("**/*", bridge)
                challenge = base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest())
                query = {
                    "client_id": "browser-test",
                    "redirect_uri": CALLBACK,
                    "response_type": "code",
                    "resource": config.resource,
                    "scope": "mcp:tools",
                    "state": "browser-state",
                    "code_challenge_method": "S256",
                    "code_challenge": challenge.rstrip(b"=").decode(),
                }
                response = page.goto(ORIGIN + "/oauth/authorize?" + urlencode(query))
                assert response is not None and response.status == 200
                signup = page.get_by_role("link", name="Create New API Key")
                assert signup.get_attribute("target") == "_blank"
                assert signup.get_attribute("rel") == "noopener noreferrer"
                assert "(open in new tab)" in signup.inner_text()
                if args.screenshot_dir and decision == "allow":
                    from pathlib import Path

                    directory = Path(args.screenshot_dir)
                    directory.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(directory / "oauth-desktop.png"), full_page=True)
                    page.set_viewport_size({"width": 375, "height": 812})
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                    page.screenshot(path=str(directory / "oauth-mobile.png"), full_page=True)
                if decision == "allow":
                    page.get_by_label("API key").fill(KEY)
                page.on(
                    "console",
                    lambda msg: print("Browser console:", msg.text.split("?")[0], flush=True),
                )
                page.get_by_role(
                    "button", name="Allow access" if decision == "allow" else "Cancel", exact=True
                ).click(no_wait_after=True)
                page.wait_for_url(CALLBACK + "?**", timeout=10000)
                assert submitted[0]["origin"] == ORIGIN, "Browser suppressed the consent Origin"
                assert COOKIE + "=" in submitted[0].get("cookie", ""), "Browser lost consent cookie"
                result = parse_qs(urlsplit(page.url).query)
                assert result["state"] == ["browser-state"] and result["iss"] == [ORIGIN]
                if decision == "allow":
                    exchanged = client.post(
                        "/oauth/token",
                        data={
                            "grant_type": "authorization_code",
                            "client_id": "browser-test",
                            "redirect_uri": CALLBACK,
                            "resource": config.resource,
                            "code": result["code"][0],
                            "code_verifier": VERIFIER,
                        },
                    )
                    assert exchanged.status_code == 200
                    assert exchanged.json().get("refresh_token")
                else:
                    assert result["error"] == ["access_denied"]
                page.close()
                print("Chromium consent " + decision + ": origin, cookie and callback verified")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
