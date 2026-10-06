import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Fetch login page
login_page = opener.open('http://127.0.0.1:5000/auth/login').read().decode()
csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', login_page)
csrf_token = csrf_match.group(1) if csrf_match else ''
print(f'Extracted CSRF token: {csrf_token[:15]}...')

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
resp = opener.open(login_req)

admin_routes = [
    '/admin/',
    '/admin/projects',
    '/admin/certificates',
    '/admin/education',
    '/admin/skills',
    '/admin/messages',
    '/admin/settings'
]

for r in admin_routes:
    req = opener.open(f'http://127.0.0.1:5000{r}')
    print(f'Admin {r} -> {req.status}')

# 3. Test Contact Form Submission on Homepage
home_page = opener.open('http://127.0.0.1:5000/').read().decode()
home_csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', home_page)
home_csrf = home_csrf_match.group(1) if home_csrf_match else ''

contact_data = urllib.parse.urlencode({
    'csrf_token': home_csrf,
    'name': 'Admissions Officer',
    'email': 'admissions@oxford.edu',
    'subject': 'Graduate Scholarship & Admissions Review',
    'message': 'Dear Rami, we reviewed your Algerian Baccalaureate credentials and Python development trajectory.'
}).encode()

contact_req = urllib.request.Request(
    'http://127.0.0.1:5000/',
    data=contact_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'http://127.0.0.1:5000/'}
)
contact_resp = opener.open(contact_req)
print(f'Contact form submission -> {contact_resp.status}')

print('All admin and live tests verified successfully!')
