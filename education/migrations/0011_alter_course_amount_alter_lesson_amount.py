# Generated by Django 4.2.5 on 2023-10-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_alter_course_amount_alter_lesson_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='цена'),
        ),
    ]
