# Generated by Django 3.2.8 on 2021-11-04 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='imageUrl',
        ),
        migrations.AddField(
            model_name='listings',
            name='bid_price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.CharField(choices=[('Fashion', 'Fashion'), ('Toy', 'Toy'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('other', 'other')], default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listings',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='listings',
            name='user',
            field=models.CharField(default='user', max_length=64),
            preserve_default=False,
        ),
    ]
