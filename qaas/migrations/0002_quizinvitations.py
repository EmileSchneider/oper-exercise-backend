# Generated by Django 3.2.11 on 2022-01-20 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qaas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizInvitations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('accepted', models.BooleanField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qaas.quiz')),
            ],
        ),
    ]
