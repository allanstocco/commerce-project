# Generated by Django 3.2.6 on 2021-12-28 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'price',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('pictureURL', models.CharField(blank=True, max_length=2048, null=True)),
                ('pictureUpload', models.FileField(blank=True, null=True, upload_to='images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('category', models.CharField(blank=True, choices=[('HOME', 'Home & Garden'), ('BOOKS', 'Books'), ('TECH', 'Eletronic & Computers'), ('ENTERTAIN', 'Films, Music & Games'), ('BEAUTY', 'Health & Beauty'), ('FASHION', 'Clothes, Shoes, Jewellery and Accessories'), ('BABY', 'Toys, Children & Baby'), ('SPORTS', 'Sports & Outdoors'), ('MOTORS', 'Car & Motorbike'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('bid_timer', models.DateTimeField(blank=True, null=True)),
                ('higherBid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='higherBid', to='auctions.bid')),
                ('user_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchlist', models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=2048)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.products'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
