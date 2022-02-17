# Generated by Django 3.2.11 on 2022-02-17 14:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0003_snippet_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='SnipetTracker',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('hostname', models.CharField(max_length=255)),
                ('ip_addr', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('viewed_at', models.DateTimeField(auto_now=True)),
                ('snippet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippet.snippet')),
            ],
        ),
    ]
