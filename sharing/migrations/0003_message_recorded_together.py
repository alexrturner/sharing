# Generated by Django 4.2.7 on 2023-11-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sharing", "0002_remove_message_message_message_audio_message_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="recorded_together",
            field=models.BooleanField(default=False),
        ),
    ]
