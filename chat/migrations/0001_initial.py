# Generated by Django 3.1.1 on 2020-12-18 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(unique=True)),
                ('p1', models.CharField(blank=True, max_length=50, null=True)),
                ('p2', models.CharField(blank=True, max_length=50, null=True)),
                ('p1_code', models.CharField(blank=True, max_length=255, null=True)),
                ('p2_code', models.CharField(blank=True, max_length=255, null=True)),
                ('p1_uid', models.IntegerField(blank=True, null=True)),
                ('p2_uid', models.IntegerField(blank=True, null=True)),
                ('p1_ready', models.BooleanField(default=False)),
                ('p2_ready', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('next_move', models.CharField(default='p1', max_length=2)),
                ('first_move', models.CharField(default='p1', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('won', models.IntegerField()),
                ('total', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=2)),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.room')),
            ],
            options={
                'unique_together': {('room', 'row', 'col')},
            },
        ),
    ]
