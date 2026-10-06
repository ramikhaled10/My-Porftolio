from datetime import datetime, timezone
from app.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(350), nullable=False)
    description = db.Column(db.Text, nullable=False)
    problem = db.Column(db.Text, nullable=True)
    approach = db.Column(db.Text, nullable=True)
    key_features = db.Column(db.Text, nullable=True)
    key_learnings = db.Column(db.Text, nullable=True)
    challenges = db.Column(db.Text, nullable=True)
    future_improvements = db.Column(db.Text, nullable=True)
    
    category = db.Column(db.String(50), nullable=False, default='Python', index=True)
    technologies = db.Column(db.String(255), nullable=False, default='Python')
    
    github_url = db.Column(db.String(255), nullable=True)
    demo_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    
    featured = db.Column(db.Boolean, default=False, index=True)
    published = db.Column(db.Boolean, default=True, index=True)
    order_num = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    images = db.relationship('ProjectImage', backref='project', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    @property
    def features_list(self):
        if not self.key_features:
            return []
        return [line.strip('- ').strip() for line in self.key_features.splitlines() if line.strip()]

    def __repr__(self):
        return f'<Project {self.title}>'


class ProjectImage(db.Model):
    __tablename__ = 'project_images'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    order_num = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ProjectImage {self.image_url} (Project #{self.project_id})>'
