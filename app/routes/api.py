from flask import Blueprint, jsonify, request
from app.models import Project, ContactMessage

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/projects')
def get_projects():
    category = request.args.get('category', '').strip()
    query = Project.query.filter_by(published=True)
    if category and category.lower() != 'all':
        query = query.filter(Project.category.ilike(category))
    
    projects = query.order_by(Project.order_num.asc()).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'summary': p.summary,
        'category': p.category,
        'technologies': p.tech_list,
        'github_url': p.github_url,
        'demo_url': p.demo_url,
        'featured': p.featured
    } for p in projects])


@api_bp.route('/messages/unread-count')
def unread_count():
    count = ContactMessage.query.filter_by(is_read=False).count()
    return jsonify({'unread_count': count})
