from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("appProjectDjango", "0004_alter_contacto_table_alter_cuotas_table_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            # 👇 OJO: usa el nombre REAL de tu tabla. Si tus tablas están con prefijo, deja appProjectDjango_eventos.
            sql='ALTER TABLE "appProjectDjango_eventos" ADD COLUMN "imagen" VARCHAR(100) DEFAULT \'default.png\';',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
