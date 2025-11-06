"""
Script to export all data from SQLite to JSON for migration
Run: python export_data.py
"""
import os
import django
import json
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from django.apps import apps

# Get all models
all_models = apps.get_models()

# Export data
data = []
for model in all_models:
    # Skip certain models
    if model._meta.app_label in ['contenttypes', 'auth', 'sessions', 'admin']:
        continue
    
    model_data = serializers.serialize('json', model.objects.all())
    if model_data != '[]':
        data.extend(json.loads(model_data))
        print(f"✓ Exportando {model._meta.model_name}: {model.objects.count()} registros")

# Save to file
with open('backup_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Exportados {len(data)} registros a backup_data.json")
print("📁 Archivo creado en: backend/backup_data.json")
