import pytest
from app import create_app
from app.extensions import db
from app.models import User, Project, SkillCategory, Skill, Education, Certification


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()

        # Seed test admin user
        admin = User(username='testadmin', email='admin@test.com', is_admin=True)
        admin.set_password('Password123!')
        db.session.add(admin)

        # Seed sample project
        project = Project(
            title='Morse Code Audio & Text Converter',
            slug='morse-code-converter',
            summary='Bidirectional converter in Python.',
            description='Detailed description of the morse code audio project.',
            problem='Translating between arbitrary text and Morse code ITU standards.',
            approach='Dictionary lookup tables and timing state intervals.',
            key_features='• Bidirectional translation\n• Audio beep synthesis',
            key_learnings='Dictionary inverted lookups and audio timing synchronization.',
            challenges='Audio latency across platforms.',
            future_improvements='Real-time audio decoding with FFT.',
            category='Python',
            technologies='Python, Audio, CLI',
            published=True,
            featured=True,
            order_num=1
        )
        db.session.add(project)

        # Seed test category and skill
        cat = SkillCategory(name='Programming Languages', icon='code-2', order_num=1)
        db.session.add(cat)
        db.session.flush()

        skill = Skill(name='Python', category_id=cat.id, level='Comfortable', description='Backend and automation', order_num=1)
        db.session.add(skill)

        # Seed test education
        edu = Education(
            institution="École Nationale Polytechnique d'Alger (ENP)",
            degree='First-Year Engineering Student',
            location='Algiers, Algeria',
            start_year='2026',
            end_year='Present',
            grade='First-Year',
            highlights='Math 18 | Physics 19.5',
            order_num=1
        )
        db.session.add(edu)

        # Seed test certification
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
    # Log in as test admin
    client.post('/auth/login', data={
        'username': 'testadmin',
        'password': 'Password123!'
    }, follow_redirects=True)
    return client
