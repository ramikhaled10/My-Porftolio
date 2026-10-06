from app.models import Project, ContactMessage


def test_admin_requires_authentication(client):
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Please log in to access this page' in response.data.decode('utf-8')


def test_admin_dashboard_authenticated(auth_client):
    response = auth_client.get('/admin/')
    assert response.status_code == 200
    assert 'Dashboard Overview' in response.data.decode('utf-8')


def test_admin_create_project(auth_client, app):
    response = auth_client.post('/admin/projects/new', data={
        'title': 'New Automation Bot',
        'slug': 'new-automation-bot',
        'category': 'Automation',
        'technologies': 'Python, Selenium',
        'summary': 'Short bot description.',
        'description': 'Full bot description.',
        'problem': 'Repetitive browser tasks.',
        'approach': 'Automated script runner.',
        'key_features': '• Headless browsing\n• Logging',
        'key_learnings': 'DOM parsing.',
        'published': True,
        'featured': False,
        'order_num': 10
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        p = Project.query.filter_by(slug='new-automation-bot').first()
        assert p is not None
        assert p.title == 'New Automation Bot'


def test_admin_edit_project(auth_client, app):
    with app.app_context():
        p = Project.query.filter_by(slug='morse-code-converter').first()
        project_id = p.id

    response = auth_client.post(f'/admin/projects/{project_id}/edit', data={
        'title': 'Updated Morse Code Name',
        'slug': 'morse-code-converter',
        'category': 'Python',
        'technologies': 'Python, Audio, CLI',
        'summary': 'Updated summary description.',
        'description': 'Updated full description.',
        'published': True,
        'order_num': 1
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        from app.extensions import db
        updated = db.session.get(Project, project_id)
        assert updated.title == 'Updated Morse Code Name'


def test_admin_delete_project(auth_client, app):
    with app.app_context():
        p = Project.query.filter_by(slug='morse-code-converter').first()
        project_id = p.id

    response = auth_client.post(f'/admin/projects/{project_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        from app.extensions import db
        deleted = db.session.get(Project, project_id)
        assert deleted is None
