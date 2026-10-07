from app.models import Education


def test_admin_requires_authentication(client):
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Please log in to access this page' in response.data.decode('utf-8')


def test_admin_dashboard_authenticated(auth_client):
    response = auth_client.get('/admin/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Dashboard Overview' in html
    assert 'Projects' not in html


def test_admin_education_pages(auth_client):
    response = auth_client.get('/admin/education')
    assert response.status_code == 200
    assert 'École Nationale Polytechnique' in response.data.decode('utf-8')


def test_admin_create_education(auth_client, app):
    response = auth_client.post('/admin/education/new', data={
        'institution': 'Test Institute',
        'degree': 'Test Degree',
        'location': 'Algiers, Algeria',
        'start_year': '2024',
        'end_year': '2025',
        'grade': '18 / 20',
        'highlights': 'Mathematics: 20 / 20',
        'description': 'A test education entry.',
        'order_num': 10
    }, follow_redirects=True)

    assert response.status_code == 200
    with app.app_context():
        edu = Education.query.filter_by(institution='Test Institute').first()
        assert edu is not None
        assert edu.degree == 'Test Degree'


def test_admin_settings_and_messages(auth_client):
    assert auth_client.get('/admin/settings').status_code == 200
    assert auth_client.get('/admin/skills').status_code == 200
    assert auth_client.get('/admin/certificates').status_code == 200
    assert auth_client.get('/admin/messages').status_code == 200
    assert auth_client.get('/admin/projects').status_code == 404
