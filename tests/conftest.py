import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from app import create_app
from app.extensions import db
from app.models import User, SkillCategory, Skill, Education, Certification


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()

        admin = User(username='testadmin', email='admin@test.com', is_admin=True)
        admin.set_password('Password123!')
        db.session.add(admin)

        cat = SkillCategory(name='Programming', icon='code-2', order_num=1)
        db.session.add(cat)
        db.session.flush()

        skill = Skill(name='Python', category_id=cat.id, level='Foundation', description='Backend and automation', order_num=1)
        db.session.add(skill)

        edu = Education(
            institution="École Nationale Polytechnique d'Alger (ENP)",
            degree='First-Year Engineering Student',
            location='Algiers, Algeria',
            start_year='2026',
            end_year='Present',
            grade='First-Year',
            highlights='Mathematics: 18 / 20 | Physics: 19.5 / 20',
            order_num=1
        )
        db.session.add(edu)

        bac = Education(
            institution='High School — Souk El Tennine',
            degree='Technique Mathématiques — Génie Électrique',
            location='Souk El Tennine, Algeria',
            start_year='High school',
            end_year='2026',
            grade='17.80 / 20',
            highlights='Mathematics: 18 / 20',
            order_num=2
        )
        db.session.add(bac)

        cert = Certification(
            title='100 Days of Code: Python',
            issuer='Udemy / Angela Yu',
            issue_date='Completed',
            order_num=1
        )
        db.session.add(cert)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'Password123!'
    }, follow_redirects=True)
    return client
