# Generated by Django 5.0.2 on 2024-03-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_course_pay_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость'),
        ),
    ]
