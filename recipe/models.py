from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=300)
    dimension = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)
    color = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="user_recipes")
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredient',
        through='RecipeIngredient'
    )
    tag = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(null=True)
    slug = models.SlugField(unique=True, null=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.ingredient

class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        unique_together = ('user', 'author')
