# Generated by Django 5.0.4 on 2024-04-30 09:26

import django.db.models.deletion
import logistics.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, verbose_name='카테고리명')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30, verbose_name='상품명')),
                ('product_description', models.TextField(verbose_name='상품 설명')),
                ('product_price', models.IntegerField(verbose_name='가격')),
                ('product_date', models.DateField(auto_now_add=True, verbose_name='등록일')),
                ('product_inventory', models.IntegerField(verbose_name='재고')),
                ('product_img', logistics.fields.ThumbnailImageField(upload_to='photo/%Y/%m', verbose_name='이미지')),
                ('product_sale', models.IntegerField(default=0, verbose_name='할인율')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.category')),
            ],
            options={
                'ordering': ('-product_date',),
            },
        ),
    ]
