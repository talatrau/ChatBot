# Generated by Django 3.2.5 on 2021-08-24 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_auto_20210824_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='fashiondetail',
            name='fashionid',
            field=models.ForeignKey(blank=True, db_column='fashionid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='chatbot.fashion'),
        ),
        migrations.AlterField(
            model_name='fashiondetail',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='fashiondetail',
            name='size',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]