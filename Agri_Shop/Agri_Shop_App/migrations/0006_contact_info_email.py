# Generated by Django 4.2.15 on 2024-09-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Agri_Shop_App", "0005_contact_info"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact_info",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
