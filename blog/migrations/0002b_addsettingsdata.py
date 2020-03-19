from django.db import migrations, models

def forwards_func(apps, schema_editor):
    Setting = apps.get_model('blog', 'BlogSettings')
    db_alias = schema_editor.connection.alias
    Setting.objects.using(db_alias).bulk_create([
        Setting(setting_name='modify_title_on_edit', setting_value='True'),
        Setting(setting_name='register_post_visits', setting_value='True'),
    ])

def reverse_func(apps, schema_editor):
    Setting = apps.get_model('blog', 'BlogSettings')
    db_alias = schema_editor.connection.alias
    Setting.objects.using(db_alias).filter(
        setting_name='modify_title_on_edit',
    ).delete()
    Setting.objects.using(db_alias).filter(
        setting_name='modify_title_on_edit',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogsettings'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
