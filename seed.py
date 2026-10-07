import os
import sys

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from app import create_app
from app.extensions import db
from app.models import (
    User, Skill, SkillCategory, Education,
    Certification, SiteSetting
)

app = create_app(os.getenv('FLASK_ENV', 'development'))


def seed_database():
    with app.app_context():
        print("Starting database seeding...")
        db.create_all()

        admin_username = os.getenv('ADMIN_USERNAME', 'rami')
        admin_email = os.getenv('ADMIN_EMAIL', 'rami.khaled@example.dz')
        admin_password = os.getenv('ADMIN_PASSWORD', 'AdminRami2026!')

        user = User.query.filter_by(username=admin_username).first()
        if not user:
            user = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            user.set_password(admin_password)
            db.session.add(user)
            print(f"Created admin user: {admin_username} ({admin_email})")
        else:
            print(f"Admin user '{admin_username}' already exists.")

        settings_data = [
            ('hero_tagline', 'First-Year Engineering Student @ ENP Algiers • Learning Software & AI', 'Main hero tagline'),
            (
                'hero_bio',
                'I am an 18-year-old engineering student at ENP Algiers. I started with Python to build solid fundamentals in programming, and now I am learning mobile development and exploring AI to eventually build useful products.',
                'Hero introductory bio'
            ),
            ('status_text', 'First-Year Engineering Student @ ENP Algiers', 'Current status badge text'),
            ('github_url', '', 'GitHub Profile URL'),
            ('linkedin_url', '', 'LinkedIn Profile URL'),
            ('instagram_url', 'https://www.instagram.com/ramikld10/', 'Instagram Profile URL'),
            ('contact_email', 'ramikld01@gmail.com', 'Primary contact email'),
            ('profile_image', 'images/rami_portrait.jpg', 'Hero profile portrait image path')
        ]
        for key, val, desc in settings_data:
            existing = SiteSetting.query.filter_by(key=key).first()
            if not existing:
                db.session.add(SiteSetting(key=key, value=val, description=desc))
            else:
                existing.value = val
                existing.description = desc
        print("Seeded site settings.")

        # Clear and re-populate Education to guarantee clean text and exact grades
        Education.query.delete()
        education_data = [
            Education(
                institution="École Nationale Polytechnique d'Alger (ENP)",
                degree="First-Year Engineering Student",
                location="Algiers, Algeria",
                start_year="2026",
                end_year="Present",
                grade="First-Year Engineering",
                highlights="Math | Physics | Algorithms & Programming | Engineering Basics",
                description="Currently in my first year at ENP Algiers, focusing on engineering math and physics while learning software and mobile development on the side.",
                order_num=1
            ),
            Education(
                institution="High School (Lycée Souk El Tennine)",
                degree="Baccalaureate 2026 — Technique Mathématiques / Génie Électrique",
                location="Souk El Tennine, Algeria",
                start_year="High school",
                end_year="2026",
                grade="17.80 / 20",
                highlights="Math: 18 / 20 | Physics: 19.5 / 20 | Electrical Engineering: 19.5 / 20",
                description="High school in Souk El Tennine in the electrical engineering track. This is also when I started taking programming seriously and learned Python.",
                order_num=2
            ),
            Education(
                institution="Middle School (CEM Souk El Tennine)",
                degree="Brevet d'Enseignement Moyen (BEM)",
                location="Souk El Tennine, Algeria",
                start_year="Middle school",
                end_year="",
                grade="17.43 / 20",
                highlights="Math: 20 / 20 | Science: 19 / 20 | Physics: 18 / 20",
                description="Middle school in Souk El Tennine, where I developed a strong interest in math and science.",
                order_num=3
            ),
            Education(
                institution="Primary School (École Primaire Souk El Tennine)",
                degree="Primary Education",
                location="Souk El Tennine, Algeria",
                start_year="Primary school",
                end_year="",
                grade=None,
                highlights="",
                description="Where I grew up and started school in Souk El Tennine, and where I first became curious about how things work.",
                order_num=4
            )
        ]
        db.session.add_all(education_data)
        print("Seeded academic milestones.")

        if SkillCategory.query.count() == 0:
            cat_prog = SkillCategory(name="Programming", icon="code-2", order_num=1)
            cat_back = SkillCategory(name="Backend", icon="database", order_num=2)
            cat_mobile = SkillCategory(name="Mobile", icon="smartphone", order_num=3)
            cat_eco = SkillCategory(name="Python ecosystem", icon="cpu", order_num=4)
            cat_concepts = SkillCategory(name="Concepts", icon="layers", order_num=5)

            db.session.add_all([cat_prog, cat_back, cat_mobile, cat_eco, cat_concepts])
            db.session.flush()

            skills_data = [
                Skill(name="Python", category_id=cat_prog.id, level="Foundation", description="The language I used to build programming fundamentals.", order_num=1),
                Skill(name="Dart", category_id=cat_prog.id, level="Developing", description="Currently learning alongside Flutter.", order_num=2),
                Skill(name="JavaScript", category_id=cat_prog.id, level="Exploring", description="Used for interactive front-end behavior.", order_num=3),
                Skill(name="HTML", category_id=cat_prog.id, level="Familiar", description="Structure of web pages.", order_num=4),
                Skill(name="CSS", category_id=cat_prog.id, level="Familiar", description="Layout, typography, and visual identity.", order_num=5),
                Skill(name="SQL", category_id=cat_prog.id, level="Familiar", description="Querying and thinking in relational data.", order_num=6),

                Skill(name="Flask", category_id=cat_back.id, level="Familiar", description="Python web framework used in this portfolio and earlier web work.", order_num=1),
                Skill(name="REST APIs", category_id=cat_back.id, level="Familiar", description="Designing and consuming HTTP APIs.", order_num=2),
                Skill(name="PostgreSQL", category_id=cat_back.id, level="Familiar", description="Relational database used for dynamic site data.", order_num=3),
                Skill(name="SQLAlchemy", category_id=cat_back.id, level="Familiar", description="ORM for models, relationships, and queries.", order_num=4),

                Skill(name="Flutter", category_id=cat_mobile.id, level="Developing", description="Currently learning for mobile application development.", order_num=1),
                Skill(name="Dart", category_id=cat_mobile.id, level="Developing", description="Language behind Flutter UIs.", order_num=2),

                Skill(name="Requests", category_id=cat_eco.id, level="Familiar", description="HTTP clients and talking to external services.", order_num=1),
                Skill(name="BeautifulSoup", category_id=cat_eco.id, level="Familiar", description="HTML parsing explored during the Python foundation.", order_num=2),
                Skill(name="Selenium", category_id=cat_eco.id, level="Exploring", description="Browser automation encountered during 100 Days of Code.", order_num=3),
                Skill(name="Tkinter", category_id=cat_eco.id, level="Exploring", description="Desktop GUIs as part of the Python foundation.", order_num=4),
                Skill(name="Pandas", category_id=cat_eco.id, level="Exploring", description="Data processing introduced during the Python course.", order_num=5),
                Skill(name="NumPy", category_id=cat_eco.id, level="Exploring", description="Numerical computing at an introductory level.", order_num=6),
                Skill(name="Matplotlib", category_id=cat_eco.id, level="Exploring", description="Data visualization encountered during the foundation.", order_num=7),

                Skill(name="Object-Oriented Programming", category_id=cat_concepts.id, level="Foundation", description="Classes, objects, and structured program design.", order_num=1),
                Skill(name="APIs", category_id=cat_concepts.id, level="Familiar", description="Connecting programs to data and services.", order_num=2),
                Skill(name="Databases", category_id=cat_concepts.id, level="Familiar", description="Storing and retrieving structured information.", order_num=3),
                Skill(name="Web Development", category_id=cat_concepts.id, level="Familiar", description="How browsers, servers, and templates fit together.", order_num=4),
                Skill(name="Automation", category_id=cat_concepts.id, level="Familiar", description="Scripts that take repetitive work off a person's plate.", order_num=5),
                Skill(name="Data Processing", category_id=cat_concepts.id, level="Exploring", description="Cleaning and transforming data before it becomes useful.", order_num=6),
            ]
            db.session.add_all(skills_data)
            print("Seeded skill categories and skills.")

        # Clear and re-populate Certifications
        Certification.query.delete()
        cert_data = [
            Certification(
                title="100 Days of Code: The Complete Python Pro Bootcamp",
                issuer="Udemy / Dr. Angela Yu",
                issue_date="Completed",
                description="A complete Python course where I learned programming basics, OOP, APIs, automation, Flask, databases, Selenium, GUI apps, and data processing. I took it to build a strong foundation before jumping into AI.",
                credential_url=None,
                image_url=None,
                skills_covered="Python, OOP, APIs, Automation, Flask, SQL, Selenium, GUI, Data Processing, Visualization",
                order_num=1
            ),
            Certification(
                title="Flutter & Dart Mobile Development",
                issuer="Coursera / IBM",
                issue_date="Coursework",
                description="A hands-on mobile development course covering Flutter widgets, Dart principles, and how to build apps for phones.",
                credential_url=None,
                image_url=None,
                skills_covered="Flutter, Dart, Mobile UI, Cross-Platform Development",
                order_num=2
            ),
            Certification(
                title="Coursework in Progress",
                issuer="EDUCBA through Coursera",
                issue_date="In Progress",
                description="Currently taking coursework from EDUCBA through Coursera to keep improving my technical and software skills alongside university.",
                credential_url=None,
                image_url=None,
                skills_covered="Software Development, Applied Coursework",
                order_num=3
            )
        ]
        db.session.add_all(cert_data)
        print("Seeded certifications.")

        db.session.commit()
        print("Database seeding finished.")


if __name__ == '__main__':
    seed_database()
