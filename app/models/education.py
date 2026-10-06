from app.extensions import db


class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False, default='Algeria')
    start_year = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(60), nullable=True)
    highlights = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    order_num = db.Column(db.Integer, default=0)

    @property
    def highlights_list(self):
        if not self.highlights:
            return []
        return [h.strip() for h in self.highlights.split('|') if h.strip()]

    def __repr__(self):
        return f'<Education {self.degree} @ {self.institution}>'
