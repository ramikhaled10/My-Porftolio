from flask import Blueprint, render_template, abort, request
from app.models import Project

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')


@projects_bp.route('', methods=['GET'])
@projects_bp.route('/', methods=['GET'])
def list_projects():
    category = request.args.get('category', '').strip()
    query = request.args.get('q', '').strip()
    
    projects_query = Project.query.filter_by(published=True)
    
    if category and category.lower() != 'all':
        projects_query = projects_query.filter(Project.category.ilike(category))
        
    if query:
        projects_query = projects_query.filter(
            (Project.title.ilike(f'%{query}%')) |
            (Project.summary.ilike(f'%{query}%')) |
            (Project.technologies.ilike(f'%{query}%'))
        )
        
    projects = projects_query.order_by(
        Project.featured.desc(),
        Project.order_num.asc(),
        Project.created_at.desc()
    ).all()
    
    # All distinct categories
    all_categories = sorted(list(set(
        p.category for p in Project.query.filter_by(published=True).all() if p.category
    )))
    
    return render_template(
        'projects/index.html',
        projects=projects,
        categories=all_categories,
        current_category=category or 'all',
        query=query
    )


@projects_bp.route('/<slug>')
def detail(slug):
    project = Project.query.filter_by(slug=slug, published=True).first_or_404()
    
    # Related projects in the same category or other featured projects
    related_projects = Project.query.filter(
        Project.published.is_(True),
        Project.id != project.id
    ).order_by(
        (Project.category == project.category).desc(),
        Project.featured.desc()
    ).limit(3).all()
    
    return render_template(
        'projects/detail.html',
        project=project,
        related_projects=related_projects
    )
