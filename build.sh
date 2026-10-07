#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Applying database migrations..."
flask db upgrade || echo "Migrations skipped or already applied."

echo "==> Seeding database..."
python seed.py

echo "==> Build complete!"
