# Generated by Django 2.2.3 on 2019-07-25 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dishes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishName', models.CharField(max_length=100)),
                ('join_date', models.DateTimeField(auto_now=True)),
                ('dishImage', models.ImageField(upload_to='dishImage')),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Owner')),
            ],
            options={
                'ordering': ['-join_date'],
            },
        ),
    ]