from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from slugify import slugify
from app.extensions import db
from app.models import (
    Project, ProjectImage, Skill, SkillCategory, Education,
    Certification, ContactMessage, SiteSetting
)
from app.forms import (
    ProjectForm, SkillForm, SkillCategoryForm, EducationForm,
    CertificationForm, SiteSettingsForm
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('main.index'))


@admin_bp.route('/')
def dashboard():
    projects_count = Project.query.count()
    published_projects = Project.query.filter_by(published=True).count()
    skills_count = Skill.query.count()
    certifications_count = Certification.query.count()
    messages_count = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        projects_count=projects_count,
        published_projects=published_projects,
        skills_count=skills_count,
        certifications_count=certifications_count,
        messages_count=messages_count,
        unread_messages=unread_messages,
        recent_messages=recent_messages,
        recent_projects=recent_projects
    )


# ===================== PROJECTS MANAGEMENT =====================

@admin_bp.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.order_num.asc(), Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=all_projects)


@admin_bp.route('/projects/new', methods=['GET', 'POST'])
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.title.data)
        
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while Project.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        project = Project(
            title=form.title.data.strip(),
            slug=slug,
            summary=form.summary.data.strip(),
            description=form.description.data.strip(),
            problem=form.problem.data.strip() if form.problem.data else None,
            approach=form.approach.data.strip() if form.approach.data else None,
            key_features=form.key_features.data.strip() if form.key_features.data else None,
            key_learnings=form.key_learnings.data.strip() if form.key_learnings.data else None,
            challenges=form.challenges.data.strip() if form.challenges.data else None,
            future_improvements=form.future_improvements.data.strip() if form.future_improvements.data else None,
            category=form.category.data,
            technologies=form.technologies.data.strip(),
            github_url=form.github_url.data.strip() if form.github_url.data else None,
            demo_url=form.demo_url.data.strip() if form.demo_url.data else None,
            image_url=form.image_url.data.strip() if form.image_url.data else None,
            featured=form.featured.data,
            published=form.published.data,
            order_num=form.order_num.data or 0
        )
        db.session.add(project)
        db.session.commit()
        flash(f'Project "{project.title}" created successfully!', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', form=form, title='Create New Project')


@admin_bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
def project_edit(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        slug = form.slug.data.strip()
        existing = Project.query.filter(Project.slug == slug, Project.id != project.id).first()
        if existing:
            flash('This slug is already used by another project. Please choose a unique slug.', 'error')
            return render_template('admin/project_form.html', form=form, title=f'Edit Project: {project.title}')

        project.title = form.title.data.strip()
        project.slug = slug
        project.summary = form.summary.data.strip()
        project.description = form.description.data.strip()
        project.problem = form.problem.data.strip() if form.problem.data else None
        project.approach = form.approach.data.strip() if form.approach.data else None
        project.key_features = form.key_features.data.strip() if form.key_features.data else None
        project.key_learnings = form.key_learnings.data.strip() if form.key_learnings.data else None
        project.challenges = form.challenges.data.strip() if form.challenges.data else None
        project.future_improvements = form.future_improvements.data.strip() if form.future_improvements.data else None
        project.category = form.category.data
        project.technologies = form.technologies.data.strip()
        project.github_url = form.github_url.data.strip() if form.github_url.data else None
        project.demo_url = form.demo_url.data.strip() if form.demo_url.data else None
        project.image_url = form.image_url.data.strip() if form.image_url.data else None
        project.featured = form.featured.data
        project.published = form.published.data
        project.order_num = form.order_num.data or 0

        db.session.commit()
        flash(f'Project "{project.title}" updated successfully!', 'success')
        return redirect(url_for('admin.projects'))

    return render_template('admin/project_form.html', form=form, title=f'Edit Project: {project.title}')


@admin_bp.route('/projects/<int:id>/delete', methods=['POST'])
def project_delete(id):
    project = Project.query.get_or_404(id)
    title = project.title
    db.session.delete(project)
    db.session.commit()
    flash(f'Project "{title}" was deleted.', 'info')
    return redirect(url_for('admin.projects'))


@admin_bp.route('/projects/<int:id>/toggle-publish', methods=['POST'])
def project_toggle_publish(id):
    project = Project.query.get_or_404(id)
    project.published = not project.published
    db.session.commit()
    flash(f'Publication status for "{project.title}" updated to {project.published}.', 'success')
    return redirect(url_for('admin.projects'))


@admin_bp.route('/projects/<int:id>/toggle-feature', methods=['POST'])
def project_toggle_feature(id):
    project = Project.query.get_or_404(id)
    project.featured = not project.featured
    db.session.commit()
    flash(f'Featured status for "{project.title}" updated to {project.featured}.', 'success')
    return redirect(url_for('admin.projects'))


# ===================== CERTIFICATIONS MANAGEMENT =====================

@admin_bp.route('/certificates')
def certificates():
    certs = Certification.query.order_by(Certification.order_num.asc()).all()
    return render_template('admin/certificates.html', certificates=certs)


@admin_bp.route('/certificates/new', methods=['GET', 'POST'])
def certificate_new():
    form = CertificationForm()
    if form.validate_on_submit():
        cert = Certification(
            title=form.title.data.strip(),
            issuer=form.issuer.data.strip(),
            issue_date=form.issue_date.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            credential_url=form.credential_url.data.strip() if form.credential_url.data else None,
            image_url=form.image_url.data.strip() if form.image_url.data else None,
            skills_covered=form.skills_covered.data.strip() if form.skills_covered.data else None,
            order_num=form.order_num.data or 0
        )
        db.session.add(cert)
        db.session.commit()
        flash('Certification added successfully!', 'success')
        return redirect(url_for('admin.certificates'))

    return render_template('admin/certificate_form.html', form=form, title='Add Certification')


@admin_bp.route('/certificates/<int:id>/edit', methods=['GET', 'POST'])
def certificate_edit(id):
    cert = Certification.query.get_or_404(id)
    form = CertificationForm(obj=cert)
    if form.validate_on_submit():
        cert.title = form.title.data.strip()
        cert.issuer = form.issuer.data.strip()
        cert.issue_date = form.issue_date.data.strip()
        cert.description = form.description.data.strip() if form.description.data else None
        cert.credential_url = form.credential_url.data.strip() if form.credential_url.data else None
        cert.image_url = form.image_url.data.strip() if form.image_url.data else None
        cert.skills_covered = form.skills_covered.data.strip() if form.skills_covered.data else None
        cert.order_num = form.order_num.data or 0
        db.session.commit()
        flash('Certification updated successfully!', 'success')
        return redirect(url_for('admin.certificates'))

    return render_template('admin/certificate_form.html', form=form, title=f'Edit Certification: {cert.title}')


@admin_bp.route('/certificates/<int:id>/delete', methods=['POST'])
def certificate_delete(id):
    cert = Certification.query.get_or_404(id)
    db.session.delete(cert)
    db.session.commit()
    flash(f'Certification "{cert.title}" deleted.', 'info')
    return redirect(url_for('admin.certificates'))


# ===================== EDUCATION MANAGEMENT =====================

@admin_bp.route('/education')
def education():
    edu_list = Education.query.order_by(Education.order_num.asc()).all()
    return render_template('admin/education.html', education_list=edu_list)


@admin_bp.route('/education/new', methods=['GET', 'POST'])
def education_new():
    form = EducationForm()
    if form.validate_on_submit():
        edu = Education(
            institution=form.institution.data.strip(),
            degree=form.degree.data.strip(),
            location=form.location.data.strip(),
            start_year=form.start_year.data.strip(),
            end_year=form.end_year.data.strip(),
            grade=form.grade.data.strip() if form.grade.data else None,
            highlights=form.highlights.data.strip() if form.highlights.data else None,
            description=form.description.data.strip() if form.description.data else None,
            order_num=form.order_num.data or 0
        )
        db.session.add(edu)
        db.session.commit()
        flash('Education milestone added successfully!', 'success')
        return redirect(url_for('admin.education'))

    return render_template('admin/education_form.html', form=form, title='Add Education Entry')


@admin_bp.route('/education/<int:id>/edit', methods=['GET', 'POST'])
def education_edit(id):
    edu = Education.query.get_or_404(id)
    form = EducationForm(obj=edu)
    if form.validate_on_submit():
        edu.institution = form.institution.data.strip()
        edu.degree = form.degree.data.strip()
        edu.location = form.location.data.strip()
        edu.start_year = form.start_year.data.strip()
        edu.end_year = form.end_year.data.strip()
        edu.grade = form.grade.data.strip() if form.grade.data else None
        edu.highlights = form.highlights.data.strip() if form.highlights.data else None
        edu.description = form.description.data.strip() if form.description.data else None
        edu.order_num = form.order_num.data or 0
        db.session.commit()
        flash('Education milestone updated successfully!', 'success')
        return redirect(url_for('admin.education'))

    return render_template('admin/education_form.html', form=form, title=f'Edit Education: {edu.institution}')


@admin_bp.route('/education/<int:id>/delete', methods=['POST'])
def education_delete(id):
    edu = Education.query.get_or_404(id)
    db.session.delete(edu)
    db.session.commit()
    flash(f'Education entry "{edu.degree}" deleted.', 'info')
    return redirect(url_for('admin.education'))


# ===================== SKILLS MANAGEMENT =====================

@admin_bp.route('/skills')
def skills():
    categories = SkillCategory.query.order_by(SkillCategory.order_num.asc()).all()
    category_form = SkillCategoryForm()
    return render_template('admin/skills.html', categories=categories, category_form=category_form)


@admin_bp.route('/skills/new', methods=['GET', 'POST'])
def skill_new():
    form = SkillForm()
    form.category_id.choices = [(c.id, c.name) for c in SkillCategory.query.order_by(SkillCategory.order_num.asc()).all()]
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data.strip(),
            category_id=form.category_id.data,
            level=form.level.data,
            description=form.description.data.strip() if form.description.data else None,
            order_num=form.order_num.data or 0
        )
        db.session.add(skill)
        db.session.commit()
        flash(f'Skill "{skill.name}" added successfully!', 'success')
        return redirect(url_for('admin.skills'))

    return render_template('admin/skill_form.html', form=form, title='Add New Skill')


@admin_bp.route('/skills/<int:id>/edit', methods=['GET', 'POST'])
def skill_edit(id):
    skill = Skill.query.get_or_404(id)
    form = SkillForm(obj=skill)
    form.category_id.choices = [(c.id, c.name) for c in SkillCategory.query.order_by(SkillCategory.order_num.asc()).all()]
    if form.validate_on_submit():
        skill.name = form.name.data.strip()
        skill.category_id = form.category_id.data
        skill.level = form.level.data
        skill.description = form.description.data.strip() if form.description.data else None
        skill.order_num = form.order_num.data or 0
        db.session.commit()
        flash(f'Skill "{skill.name}" updated successfully!', 'success')
        return redirect(url_for('admin.skills'))

    return render_template('admin/skill_form.html', form=form, title=f'Edit Skill: {skill.name}')


@admin_bp.route('/skills/<int:id>/delete', methods=['POST'])
def skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash(f'Skill "{skill.name}" deleted.', 'info')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/category/new', methods=['POST'])
def category_new():
    form = SkillCategoryForm()
    if form.validate_on_submit():
        cat = SkillCategory(
            name=form.name.data.strip(),
            icon=form.icon.data.strip() or 'code-2',
            order_num=form.order_num.data or 0
        )
        db.session.add(cat)
        db.session.commit()
        flash(f'Category "{cat.name}" added!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/category/<int:id>/delete', methods=['POST'])
def category_delete(id):
    cat = SkillCategory.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash(f'Skill Category "{cat.name}" and its skills deleted.', 'info')
    return redirect(url_for('admin.skills'))


# ===================== MESSAGES MANAGEMENT =====================

@admin_bp.route('/messages')
def messages():
    all_msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_msgs)


@admin_bp.route('/messages/<int:id>/toggle-read', methods=['POST'])
def message_toggle_read(id):
    msg = ContactMessage.query.get_or_404(id)
    msg.is_read = not msg.is_read
    db.session.commit()
    flash('Message status updated.', 'success')
    return redirect(url_for('admin.messages'))


@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
def message_delete(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'info')
    return redirect(url_for('admin.messages'))


# ===================== SETTINGS MANAGEMENT =====================

@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SiteSettingsForm()
    if request.method == 'GET':
        form.hero_tagline.data = SiteSetting.get('hero_tagline', 'Engineer in progress. Developer by curiosity. Builder by ambition.')
        form.hero_bio.data = SiteSetting.get('hero_bio', "First-year engineering student at École Nationale Polytechnique d'Alger (ENP). Exploring the intersection of software, backend systems, and AI-driven mobile development.")
        form.status_text.data = SiteSetting.get('status_text', 'First-year Engineering Student at ENP')
        form.github_url.data = SiteSetting.get('github_url', 'https://github.com/ramikhaled')
        form.linkedin_url.data = SiteSetting.get('linkedin_url', 'https://linkedin.com/in/rami-khaled')
        form.contact_email.data = SiteSetting.get('contact_email', 'rami.khaled@example.dz')

    if form.validate_on_submit():
        SiteSetting.set('hero_tagline', form.hero_tagline.data.strip(), 'Homepage hero tagline')
        SiteSetting.set('hero_bio', form.hero_bio.data.strip(), 'Homepage hero bio')
        SiteSetting.set('status_text', form.status_text.data.strip(), 'Current status badge text')
        SiteSetting.set('github_url', form.github_url.data.strip(), 'GitHub profile URL')
        SiteSetting.set('linkedin_url', form.linkedin_url.data.strip(), 'LinkedIn profile URL')
        SiteSetting.set('contact_email', form.contact_email.data.strip(), 'Contact email address')
        flash('Portfolio site settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', form=form)
