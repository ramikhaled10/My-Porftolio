from app.extensions import db


class Certification(db.Model):
    __tablename__ = 'certifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(120), nullable=False)
    issue_date = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credential_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    skills_covered = db.Column(db.String(255), nullable=True)
    order_num = db.Column(db.Integer, default=0)

    @property
    def skills_list(self):
        if not self.skills_covered:
            return []
        return [s.strip() for s in self.skills_covered.split(',') if s.strip()]

    def __repr__(self):
        return f'<Certification {self.title} from {self.issuer}>'
