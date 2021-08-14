from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User


class Choice(models.Model):
    """
       Модель вариантов ответа
          -название
    """
    title = models.TextField()
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'choices'
        verbose_name = 'Вариант Ответа'
        verbose_name_plural = 'Варианты Ответов'


class Question(models.Model):
    """
        Модель Вопросов
          -название
          -варианты ответов
          -правильные ответы (может быть несколько)
          -баллы за вопрос
    """
    title = models.TextField()
    answer_options = models.ManyToManyField(Choice, related_name='answer_options')
    points = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_correct_answers(self):
        return ' ,'.join([answer.title for answer in self.answer_options.filter(is_right=True).all()])

    class Meta:
        ordering = ['points']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Test(models.Model):
    """
        Модель Тестов
          -название
          -вопросы
          -всего баллов
    """
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """
        Модель Ответа Пользователя
           -ответивший пользователь
           -вопрос из таблицы вопросов
           -ответ(ответы) из таблицы ответов
           -баллы за вопрос - по умолчанию 0,
                 установка после создания объекта
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ManyToManyField(Choice)
    points = models.FloatField(default=0, editable=False)

    def __str__(self):
        choices = self.get_choices_titles()
        if len(choices) > 1:
            reply = f'Вопрос: {self.question.title}\nОтветы:'
            for choice in choices:
                reply += f'\n{choice}'
            return reply
        return f'Вопрос: {self.question.title}\nОтвет: {choices[0].title}'

    def get_choices_titles(self):
        return [choice.title for choice in self.choice.all()]

    class Meta:
        ordering = ['user']
        db_table = 'answers'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    """
        Модель Результата пользователя за все вопросы
            -пользователь
            -всего ответов
            -набранные баллы
            -максимум баллов
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    quantity_of_question = models.IntegerField(editable=False)
    points_earned = models.FloatField(editable=False)
    max_points = models.FloatField(editable=False)

    def __str__(self):
        return f'{self.user} - {self.points_earned}/{self.max_points} - {self.get_in_perc}%'

    def get_in_perc(self):
        return self.points_earned * 100 / self.max_points

    class Meta:
        ordering = ['user']
        db_table = 'results'
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
