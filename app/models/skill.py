from app.extensions import db


class SkillCategory(db.Model):
    __tablename__ = 'skill_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    icon = db.Column(db.String(64), default='code-2')
    order_num = db.Column(db.Integer, default=0)

    skills = db.relationship(
        'Skill',
        backref='category',
        cascade='all, delete-orphan',
        order_by='Skill.order_num',
        lazy='joined'
    )

    def __repr__(self):
        return f'<SkillCategory {self.name}>'


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_categories.id', ondelete='CASCADE'), nullable=False)
    # Levels: "Comfortable", "Familiar", "Developing", "Exploring"
    level = db.Column(db.String(32), nullable=False, default='Familiar')
    description = db.Column(db.String(255), nullable=True)
    order_num = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Skill {self.name} ({self.level})>'
