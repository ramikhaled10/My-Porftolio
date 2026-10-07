from app.models import ContactMessage


PUBLIC_PAGES = [
    '/',
    '/about',
    '/education',
    '/skills',
    '/learning',
    '/vision',
    '/certificates',
    '/contact',
]


def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Rami Khaled' in html
    assert 'École Nationale Polytechnique' in html
    assert 'About Me' in html
    assert 'My Goals' in html
    assert 'Contact Me' in html
    assert 'rami_portrait.jpg' in html
    assert 'Explore Projects' not in html
    assert 'href="/projects"' not in html


def test_all_public_pages_return_200(client):
    for path in PUBLIC_PAGES:
        response = client.get(path)
        assert response.status_code == 200, f'{path} returned {response.status_code}'
        html = response.data.decode('utf-8')
        assert 'Rami Khaled' in html
        assert 'nav-link active' in html


def test_about_page_story(client):
    html = client.get('/about').data.decode('utf-8')
    assert '100 Days of Code' in html
    assert 'foundation' in html
    assert 'Souk El Tennine' in html


def test_education_page(client):
    html = client.get('/education').data.decode('utf-8')
    assert '17.80' in html
    assert 'École Nationale Polytechnique' in html


def test_skills_page(client):
    html = client.get('/skills').data.decode('utf-8')
    assert 'Python' in html
    assert 'Foundation' in html


def test_learning_page(client):
    html = client.get('/learning').data.decode('utf-8')
    assert 'Flutter' in html
    assert 'EDUCBA' in html
    assert 'Coursera' in html


def test_vision_page(client):
    html = client.get('/vision').data.decode('utf-8')
    assert 'Entrepreneurship' in html
    assert 'Innovation' in html
    assert 'solve real problems' in html


def test_certificates_page(client):
    html = client.get('/certificates').data.decode('utf-8')
    assert '100 Days of Code' in html


def test_projects_routes_removed(client):
    response = client.get('/projects')
    assert response.status_code == 404
    response = client.get('/projects/morse-code-converter')
    assert response.status_code == 404


def test_contact_form_submission(client, app):
    response = client.post('/contact', data={
        'name': 'Prof. John Adams',
        'email': 'jadams@university.edu',
        'subject': 'Research Inquiry',
        'message': 'Hello Rami, impressed by your academic record and Python work.'
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        msg = ContactMessage.query.filter_by(email='jadams@university.edu').first()
        assert msg is not None
        assert msg.name == 'Prof. John Adams'
        assert msg.subject == 'Research Inquiry'
        assert msg.is_read is False


def test_robots_and_sitemap(client):
    res_robots = client.get('/robots.txt')
    assert res_robots.status_code == 200
    assert 'User-agent: *' in res_robots.data.decode('utf-8')

    res_sitemap = client.get('/sitemap.xml')
    assert res_sitemap.status_code == 200
    xml = res_sitemap.data.decode('utf-8')
    assert '<?xml' in xml
    for path in PUBLIC_PAGES:
        assert path in xml or (path == '/' and xml)
    assert '/about' in xml
    assert '/vision' in xml
    assert '/projects' not in xml
