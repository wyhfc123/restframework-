# Generated by Django 2.0.6 on 2020-05-12 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_department_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment',
            field=models.IntegerField(blank=True, choices=[(1, '三好员工'), (2, '优秀员工'), (1, '一般员工')], null=True),
        ),
    ]
