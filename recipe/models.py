from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=300)
    dimension = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="recipes")
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    text = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, )
    # tag
    # time
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name
