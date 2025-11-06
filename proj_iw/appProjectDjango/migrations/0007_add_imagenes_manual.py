from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("appProjectDjango", "0006_rename_manual_tables_to_default"),
    ]

    operations = [
        migrations.RunSQL(
            # 👇 Usa el nombre REAL de tu tabla de merchandising
            sql='ALTER TABLE "appProjectDjango_merchandising" ADD COLUMN "imagen2" VARCHAR(200) NULL;',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
