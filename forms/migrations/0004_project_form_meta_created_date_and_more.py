# Generated by Django 4.1 on 2023-08-06 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0003_alter_project_form_meta_form_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_form_meta',
            name='created_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='project_form_meta',
            name='updated_date',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='Project_Form',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=80)),
                ('field_description', models.CharField(max_length=160)),
                ('field_type', models.CharField(max_length=160)),
                ('field_size', models.IntegerField(max_length=160)),
                ('created_date', models.DateField()),
                ('updated_date', models.DateField()),
                ('form_meta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms.project_form_meta')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
