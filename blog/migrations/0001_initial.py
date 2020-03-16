# Generated by Django 2.2.9 on 2020-02-16 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import django_lifecycle.mixins
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', martor.models.MartorField(default='')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='title', unique=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('content_edited', models.DateTimeField(null=True)),
                ('num_views', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['-added'],
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PostViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_views', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
    ]
