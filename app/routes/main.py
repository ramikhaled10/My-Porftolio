from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from app.extensions import db
from app.models import Project, SkillCategory, Education, Certification, ContactMessage, SiteSetting
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            subject=form.subject.data.strip(),
            message=form.message.data.strip()
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you for reaching out! Your message has been received.', 'success')
        return redirect(url_for('main.index', _anchor='contact'))

    # Load content for homepage
    featured_projects = Project.query.filter_by(published=True).order_by(
        Project.featured.desc(),
        Project.order_num.asc(),
        Project.created_at.desc()
    ).all()
    
    skill_categories = SkillCategory.query.order_by(SkillCategory.order_num.asc()).all()
    education_list = Education.query.order_by(Education.order_num.asc()).all()
    certifications = Certification.query.order_by(Certification.order_num.asc()).all()
    
    # Dynamic settings or sensible defaults
    site_tagline = SiteSetting.get('hero_tagline', 'Engineer in progress. Developer by curiosity. Builder by ambition.')
    site_bio = SiteSetting.get('hero_bio', "First-year engineering student at École Nationale Polytechnique d'Alger (ENP). Exploring the intersection of software, backend systems, and AI-driven mobile development.")
    status_text = SiteSetting.get('status_text', 'First-year Engineering Student at ENP')
    github_url = SiteSetting.get('github_url', 'https://github.com/ramikhaled')
    linkedin_url = SiteSetting.get('linkedin_url', 'https://linkedin.com/in/rami-khaled')

    # Distinct categories for filtering
    all_categories = sorted(list(set(p.category for p in featured_projects if p.category)))

    return render_template(
        'index.html',
        form=form,
        projects=featured_projects,
        categories=all_categories,
        skill_categories=skill_categories,
        education_list=education_list,
        certifications=certifications,
        site_tagline=site_tagline,
        site_bio=site_bio,
        status_text=status_text,
        github_url=github_url,
        linkedin_url=linkedin_url
    )


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            subject=form.subject.data.strip(),
            message=form.message.data.strip()
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you for reaching out! Your message has been received.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)


@main_bp.route('/robots.txt')
def robots():
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /auth/\n\nSitemap: " + request.url_root.rstrip('/') + "/sitemap.xml\n"
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    return response


@main_bp.route('/sitemap.xml')
def sitemap():
    projects = Project.query.filter_by(published=True).all()
    base_url = request.url_root.rstrip('/')
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    static_routes = [
        ('/', '1.0', 'weekly'),
        ('/projects', '0.9', 'weekly'),
        ('/contact', '0.8', 'monthly'),
    ]
    
    for route, priority, changefreq in static_routes:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{route}</loc>')
        xml.append(f'    <changefreq>{changefreq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
        
    for p in projects:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}/projects/{p.slug}</loc>')
        xml.append('    <changefreq>monthly</changefreq>')
        xml.append('    <priority>0.8</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    response = make_response('\n'.join(xml))
    response.headers['Content-Type'] = 'application/xml'
    return response
