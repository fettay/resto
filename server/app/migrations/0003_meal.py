# Generated by Django 3.0.3 on 2020-06-12 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20200612_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.CharField(max_length=150)),
                ('category', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('provider', models.CharField(max_length=50)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('owner_id', 'title', 'date', 'provider')},
            },
        ),
    ]