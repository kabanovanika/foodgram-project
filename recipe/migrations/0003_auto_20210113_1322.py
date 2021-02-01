# Generated by Django 3.1.4 on 2021-01-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_auto_20210113_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipe.RecipeIngredient',
                                         to='recipe.Ingredient'),
        ),
    ]
