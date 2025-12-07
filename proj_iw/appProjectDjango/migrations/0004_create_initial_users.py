# Generated migration to create initial users
from django.db import migrations
from django.contrib.auth.hashers import make_password
from decouple import config

def create_initial_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    
    # Crear usuario moderador1
    moderador_user, created = User.objects.get_or_create(
        username='moderador1',
        defaults={
            'password': make_password(config('MODERADOR_PASS')),
            'is_staff': True,
            'is_active': True,
            'email': 'moderador@example.com'
        }
    )
    # Si el usuario ya existía, actualizar su contraseña
    if not created:
        moderador_user.password = make_password(config('MODERADOR_PASS'))
        moderador_user.is_staff = True
        moderador_user.is_active = True
        moderador_user.save()
    
    # Añadir al grupo Moderador
    try:
        moderador_group = Group.objects.get(name='Moderador')
        moderador_user.groups.add(moderador_group)
    except Group.DoesNotExist:
        pass
    
    # Crear usuario gestor1
    gestor_user, created = User.objects.get_or_create(
        username='gestor1',
        defaults={
            'password': make_password(config('GESTOR_PASS')),
            'is_staff': True,
            'is_active': True,
            'email': 'gestor@example.com'
        }
    )
    # Si el usuario ya existía, actualizar su contraseña
    if not created:
        gestor_user.password = make_password(config('GESTOR_PASS'))
        gestor_user.is_staff = True
        gestor_user.is_active = True
        gestor_user.save()
    
    # Añadir al grupo Gestor
    try:
        gestor_group = Group.objects.get(name='Gestor')
        gestor_user.groups.add(gestor_group)
    except Group.DoesNotExist:
        pass

    # Crear superusuario
    super_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'password': make_password('admin'),
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'email': 'admin@example.com'
        }
    )
    if not created:
        super_user.password = make_password('admin')
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.is_active = True
        super_user.save()



class Migration(migrations.Migration):

    dependencies = [
        ('appProjectDjango', '0003_alter_asistenciaevento_fecha_registro_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]
