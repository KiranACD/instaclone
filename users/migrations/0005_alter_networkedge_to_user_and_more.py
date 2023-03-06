# Generated by Django 4.1.7 on 2023-02-24 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_profile_pic_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkedge',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='users.userprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='networkedge',
            unique_together={('from_user', 'to_user')},
        ),
    ]