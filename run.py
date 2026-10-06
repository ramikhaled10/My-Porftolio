import os
from app import create_app
from app.extensions import db
from app.models import (
    User, Project, Skill, SkillCategory, Education,
    Certification, ContactMessage, SiteSetting
)

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Project': Project,
        'Skill': Skill,
        'SkillCategory': SkillCategory,
        'Education': Education,
        'Certification': Certification,
        'ContactMessage': ContactMessage,
        'SiteSetting': SiteSetting
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
