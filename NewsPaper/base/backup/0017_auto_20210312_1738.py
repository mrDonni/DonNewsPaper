# Generated by Django 3.1.6 on 2021-03-12 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0016_auto_20210312_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscriber',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
