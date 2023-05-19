# Generated by Django 4.2 on 2023-05-13 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('NewsPortal', '0024_remove_subscription_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySubscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribe',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.category'),
        ),
        migrations.AddField(
            model_name='postcategory',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NewsPortal.post'),
        ),
        migrations.AddField(
            model_name='categorysubscribe',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='NewsPortal.category'),
        ),
        migrations.AddField(
            model_name='categorysubscribe',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
