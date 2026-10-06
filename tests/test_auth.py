def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert 'Admin Authentication' in response.data.decode('utf-8')


def test_login_successful(client):
    response = client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'Password123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Dashboard Overview' in response.data.decode('utf-8')


def test_login_invalid_credentials(client):
    response = client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'WrongPassword!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid username or password' in response.data.decode('utf-8')


def test_logout(auth_client):
    response = auth_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'You have been securely signed out' in response.data.decode('utf-8')
