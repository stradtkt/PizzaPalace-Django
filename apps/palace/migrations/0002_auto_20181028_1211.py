# Generated by Django 2.1.2 on 2018-10-28 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('palace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.RemoveField(
            model_name='item',
            name='name',
        ),
        migrations.AddField(
            model_name='item',
            name='content_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Content Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='qty',
            field=models.PositiveIntegerField(verbose_name='quantity'),
        ),
    ]