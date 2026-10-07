from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from app.extensions import db
from app.models import SkillCategory, Education, Certification, ContactMessage, SiteSetting
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Dynamic settings or sensible defaults
    site_tagline = SiteSetting.get('hero_tagline', 'Engineering Student • Developer • Future Builder')
    site_bio = SiteSetting.get('hero_bio', "Exploring AI, software development, and the future of intelligent applications.")
    status_text = SiteSetting.get('status_text', 'First-Year Engineering Student @ ENP Algiers')
    profile_image = SiteSetting.get('profile_image', 'images/rami_portrait.jpg')

    return render_template(
        'index.html',
        site_tagline=site_tagline,
        site_bio=site_bio,
        status_text=status_text,
        profile_image=profile_image
    )


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/education')
def education():
    education_list = Education.query.order_by(Education.order_num.asc()).all()
    return render_template('education.html', education_list=education_list)


@main_bp.route('/skills')
def skills():
    skill_categories = SkillCategory.query.order_by(SkillCategory.order_num.asc()).all()
    return render_template('skills.html', skill_categories=skill_categories)


@main_bp.route('/learning')
def learning():
    return render_template('learning.html')


@main_bp.route('/vision')
def vision():
    return render_template('vision.html')


@main_bp.route('/certificates')
def certificates():
    certifications = Certification.query.order_by(Certification.order_num.asc()).all()
    return render_template('certificates.html', certifications=certifications)


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
    base_url = request.url_root.rstrip('/')
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    static_routes = [
        ('/', '1.0', 'weekly'),
        ('/about', '0.9', 'monthly'),
        ('/education', '0.9', 'monthly'),
        ('/skills', '0.8', 'monthly'),
        ('/learning', '0.8', 'monthly'),
        ('/vision', '0.8', 'monthly'),
        ('/certificates', '0.8', 'monthly'),
        ('/contact', '0.7', 'monthly'),
    ]
    
    for route, priority, changefreq in static_routes:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{route}</loc>')
        xml.append(f'    <changefreq>{changefreq}</changefreq>')
        xml.append(f'    <priority>{priority}</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    response = make_response('\n'.join(xml))
    response.headers['Content-Type'] = 'application/xml'
    return response
