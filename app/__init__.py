import os
from flask import Flask, render_template
from config import config_by_name
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    from app.routes import main_bp, auth_bp, admin_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    # Global template context processor
    @app.context_processor
    def inject_global_context():
        from app.models import ContactMessage, SiteSetting
        from flask_login import current_user
        
        unread_count = 0
        if current_user.is_authenticated:
            try:
                unread_count = ContactMessage.query.filter_by(is_read=False).count()
            except Exception:
                unread_count = 0

        return {
            'site_author': 'Rami Khaled',
            'author_age': 18,
            'current_year': 2026,
            'current_location': 'Souk El Tennine & Algiers, Algeria',
            'current_institution': "École Nationale Polytechnique d'Alger (ENP)",
            'unread_messages_count': unread_count,
            'github_url': SiteSetting.get('github_url', ''),
            'linkedin_url': SiteSetting.get('linkedin_url', ''),
            'instagram_url': SiteSetting.get('instagram_url', 'https://www.instagram.com/ramikld10/'),
            'contact_email': SiteSetting.get('contact_email', 'ramikld01@gmail.com'),
            'profile_image': SiteSetting.get('profile_image', 'images/rami_portrait.jpg')
        }

    return app


def __getattr__(name):
    if name == 'app':
        return create_app(os.getenv('FLASK_ENV', 'production'))
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
