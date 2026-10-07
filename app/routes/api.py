from flask import Blueprint, jsonify
from app.models import ContactMessage

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/messages/unread-count')
def unread_count():
    count = ContactMessage.query.filter_by(is_read=False).count()
    return jsonify({'unread_count': count})
