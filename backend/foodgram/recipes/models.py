from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Введите единицы измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название',
        help_text='Укажите название тега'
    )
    color = ColorField(
        max_length=7,
        verbose_name='Цвет в HEX',
        help_text='Укажите HEX-код цвета тега'
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Уникальный слаг',
        help_text='Укажите уникальный слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список тегов',
        help_text='Укажите теги'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.CASCADE,
        help_text='Укажите автора рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        help_text='Добавьте нужные ингридиенты',
        through='IngredientList',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Укажите название рецепта',
    )
    image = models.ImageField(
        verbose_name='Ссылка на картинку на сайте',
        upload_to='media/images/',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Добавьте описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Укажите время приготовления',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 минуты'
        )]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientList(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Название ингредиента',
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Название рецепта',
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        help_text='Введите количество ингредиента',
        validators=[MinValueValidator(
            1, 'Количество ингредиента не может быть меньше 1'
        )]
    )

    class Meta:
        verbose_name = 'Список ингрединтов'
        verbose_name_plural = 'Списки ингрединтов'

    def __str__(self):
        return f'{self.ingredient}: {self.amount}'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite_recipe'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'author'),
                name='unique_favorite_recipe'
            ),
        )


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_list'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_list'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_shopping_list'
            ),
        )
