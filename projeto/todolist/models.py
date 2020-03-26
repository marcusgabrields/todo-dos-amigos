from django.db import models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):

    name = models.CharField('nome', max_length=20)

    def __str__(self):
        return self.name


class TodoList(TimeStampedModel):

    LOW = 0
    MEDIUM = 1
    HIGH = 2
    PRIORITY_CHOICES = (
        (LOW, 'Baixa'),
        (MEDIUM, 'Média'),
        (HIGH, 'Alta'),
    )

    title = models.CharField('título', max_length=255)
    content = models.TextField('conteudo')
    date = models.DateTimeField('data')
    priority = models.PositiveIntegerField(
        'prioridade', choices=PRIORITY_CHOICES
    )
    category = models.ManyToManyField(
        Category,
        related_name='todos',
    )

    def __str__(self):
        return self.title