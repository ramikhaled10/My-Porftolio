import os
import socket
import urllib.request
import urllib.parse
import http.cookiejar
import re
import pytest


def is_live_server_running(host="127.0.0.1", port=5000):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


RUN_LIVE = os.environ.get("RUN_LIVE_TESTS") == "1"


@pytest.mark.skipif(
    not (RUN_LIVE and is_live_server_running()),
    reason="Live server tests require RUN_LIVE_TESTS=1 and a server running on 127.0.0.1:5000"
)
def test_live_server_smoke():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # 1. Fetch login page with explicit timeout
    login_page = opener.open('http://127.0.0.1:5000/auth/login', timeout=3).read().decode()
    csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', login_page)
    csrf_token = csrf_match.group(1) if csrf_match else ''

    # 2. Authenticate
    login_data = urllib.parse.urlencode({
        'csrf_token': csrf_token,
        'username': 'rami',
        'password': 'AdminRami2026!'
    }).encode()

    login_req = urllib.request.Request(
        'http://127.0.0.1:5000/auth/login',
        data=login_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://127.0.0.1:5000/auth/login'
        }
    )
    resp = opener.open(login_req, timeout=3)
    assert resp.status == 200

    admin_routes = [
        '/admin/',
        '/admin/certificates',
        '/admin/education',
        '/admin/skills',
        '/admin/messages',
        '/admin/settings'
    ]

    public_routes = [
        '/',
        '/about',
        '/education',
        '/skills',
        '/learning',
        '/vision',
        '/certificates',
        '/contact',
    ]
    for r in public_routes:
        req = opener.open(f'http://127.0.0.1:5000{r}', timeout=3)
        assert req.status == 200

    for r in admin_routes:
        req = opener.open(f'http://127.0.0.1:5000{r}', timeout=3)
        assert req.status == 200


if __name__ == '__main__':
    if is_live_server_running():
        test_live_server_smoke()
        print("Live smoke test passed!")
    else:
        print("Server is not running on 127.0.0.1:5000")
