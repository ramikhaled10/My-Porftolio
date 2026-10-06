from app.extensions import db


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(255), nullable=True)

    @classmethod
    def get(cls, key: str, default: str = '') -> str:
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting and setting.value else default

    @classmethod
    def set(cls, key: str, value: str, description: str = ''):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()

    def __repr__(self):
        return f'<SiteSetting {self.key}>'
