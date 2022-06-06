# Generated by Django 3.2.13 on 2022-06-04 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_remove_message_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='web.message'),
        ),
    ]