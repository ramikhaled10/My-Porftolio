"""Initial portfolio migration

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-10-06 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. projects
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=150), nullable=False),
        sa.Column('summary', sa.String(length=350), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('problem', sa.Text(), nullable=True),
        sa.Column('approach', sa.Text(), nullable=True),
        sa.Column('key_features', sa.Text(), nullable=True),
        sa.Column('key_learnings', sa.Text(), nullable=True),
        sa.Column('challenges', sa.Text(), nullable=True),
        sa.Column('future_improvements', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('technologies', sa.String(length=255), nullable=False),
        sa.Column('github_url', sa.String(length=255), nullable=True),
        sa.Column('demo_url', sa.String(length=255), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('featured', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('published', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_slug'), 'projects', ['slug'], unique=True)
    op.create_index(op.f('ix_projects_category'), 'projects', ['category'], unique=False)

    # 3. project_images
    op.create_table(
        'project_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=255), nullable=False),
        sa.Column('caption', sa.String(length=200), nullable=True),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. skill_categories
    op.create_table(
        'skill_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('icon', sa.String(length=64), nullable=True),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # 5. skills
    op.create_table(
        'skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('level', sa.String(length=32), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.ForeignKeyConstraint(['category_id'], ['skill_categories.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 6. education
    op.create_table(
        'education',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('institution', sa.String(length=150), nullable=False),
        sa.Column('degree', sa.String(length=150), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=False),
        sa.Column('start_year', sa.String(length=20), nullable=False),
        sa.Column('end_year', sa.String(length=20), nullable=False),
        sa.Column('grade', sa.String(length=60), nullable=True),
        sa.Column('highlights', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id')
    )

    # 7. certifications
    op.create_table(
        'certifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('issuer', sa.String(length=120), nullable=False),
        sa.Column('issue_date', sa.String(length=60), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('credential_url', sa.String(length=255), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('skills_covered', sa.String(length=255), nullable=True),
        sa.Column('order_num', sa.Integer(), nullable=True, server_default='0'),
        sa.PrimaryKeyConstraint('id')
    )

    # 8. contact_messages
    op.create_table(
        'contact_messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 9. site_settings
    op.create_table(
        'site_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=64), nullable=False),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_site_settings_key'), 'site_settings', ['key'], unique=True)


def downgrade():
    op.drop_table('site_settings')
    op.drop_table('contact_messages')
    op.drop_table('certifications')
    op.drop_table('education')
    op.drop_table('skills')
    op.drop_table('skill_categories')
    op.drop_table('project_images')
    op.drop_table('projects')
    op.drop_table('users')
