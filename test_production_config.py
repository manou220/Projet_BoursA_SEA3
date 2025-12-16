#!/usr/bin/env python3
"""Test rapide de la configuration de production."""
from app import create_app

app = create_app('production')
print("[OK] Application demarree en production")
print(f"SESSION_COOKIE_SECURE: {app.config['SESSION_COOKIE_SECURE']}")
print(f"DEBUG: {app.config['DEBUG']}")
print(f"FLASK_ENV: {app.config.get('FLASK_ENV', 'N/A')}")

