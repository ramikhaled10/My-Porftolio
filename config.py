import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent
load_dotenv(os.path.join(basedir, '.env'))


def get_database_url():
    url = os.getenv('DATABASE_URL')
    if not url:
        return f"sqlite:///{basedir / 'rami_portfolio.db'}"
    # Standardize legacy postgres:// to postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'rami-portfolio-dev-secret-key-2026-enp')
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf'}
    
    # CSRF & Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Portfolio metadata defaults
    SITE_NAME = "Rami Khaled | Engineering Student & Developer"
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'rami.khaled@example.dz')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'rami')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'AdminRami2026!')


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
