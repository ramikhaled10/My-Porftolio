from app.models import ContactMessage, Project


def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Rami Khaled' in html
    assert 'École Nationale Polytechnique' in html
    assert '17.80' in html
    assert 'Morse Code Audio' in html


def test_projects_list_page(client):
    response = client.get('/projects', follow_redirects=True)
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Software Projects' in html
    assert 'Morse Code Audio' in html


def test_project_detail_page(client):
    response = client.get('/projects/morse-code-converter')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Morse Code Audio' in html
    assert 'THE PROBLEM IT SOLVES' in html
    assert 'WHAT I LEARNED' in html


def test_project_detail_404(client):
    response = client.get('/projects/non-existent-project')
    assert response.status_code == 404
    assert '404' in response.data.decode('utf-8')


def test_contact_form_submission(client, app):
    response = client.post('/', data={
        'name': 'Prof. John Adams',
        'email': 'jadams@university.edu',
        'subject': 'Research Inquiry',
        'message': 'Hello Rami, impressed by your academic record and Python projects.'
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
    assert '<?xml' in res_sitemap.data.decode('utf-8')
    assert '/projects/morse-code-converter' in res_sitemap.data.decode('utf-8')
