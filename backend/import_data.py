import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'joby_api.settings')
django.setup()

from django.core import serializers
from django.db import transaction

def import_data():
    """Importa datos desde backup_data.json manejando duplicados"""
    
    with open('backup_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Agrupar por modelo
    models_data = {}
    for obj in data:
        model = obj['model']
        if model not in models_data:
            models_data[model] = []
        models_data[model].append(obj)
    
    # Para JobAlertPreference, mantener solo el primero por user_id
    if 'users.jobalertpreference' in models_data:
        seen_users = set()
        filtered = []
        for obj in models_data['users.jobalertpreference']:
            user_id = obj['fields']['user']
            if user_id not in seen_users:
                seen_users.add(user_id)
                filtered.append(obj)
            else:
                print(f"⚠️  Saltando JobAlertPreference duplicada para user {user_id}")
        models_data['users.jobalertpreference'] = filtered
        print(f"✓ JobAlertPreference: {len(filtered)} registros únicos")
    
    # Reconstruir la lista de objetos
    filtered_data = []
    for model_list in models_data.values():
        filtered_data.extend(model_list)
    
    # Importar con Django
    print(f"\n📥 Importando {len(filtered_data)} registros...")
    
    imported = 0
    skipped = 0
    
    for obj in serializers.deserialize('json', json.dumps(filtered_data)):
        try:
            with transaction.atomic():
                obj.save()
                imported += 1
        except Exception as e:
            skipped += 1
            print(f"⚠️  Saltado {obj.object.__class__.__name__} (ya existe)")
    
    print(f"\n✅ Importación completada!")
    print(f"   📝 Importados: {imported}")
    print(f"   ⏭️  Saltados: {skipped}")
    
    # Verificar
    from apps.users.models import User
    print(f"\n📊 Verificación:")
    print(f"   Usuarios: {User.objects.count()}")
    test_user = User.objects.filter(email='test@test.com').first()
    if test_user:
        print(f"   Test user points: {test_user.points}")
        if hasattr(test_user, 'referral_code'):
            print(f"   Test user code: {test_user.referral_code.code}")

if __name__ == '__main__':
    import_data()
