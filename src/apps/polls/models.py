from django.db import models
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

    @property
    def max_points(self):
        return sum(question.points for question in self.questions.all())

    def __str__(self):
        return f'{self.title} - {self.max_points} баллов'

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Answer(models.Model):
    """
        Модель Ответа Пользователя
           -ответивший пользователь
           -вопрос из таблицы вопросов
           -ответ(ответы) из таблицы ответов
           -баллы за вопрос - по умолчанию 0,
                 установка после создания объекта
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ManyToManyField(Choice)

    def __str__(self):
        # choices = self.get_choices_titles()
        # return f'Вопрос: {self.question.title}\nОтвет: {choices[0]}'
        return f'{self.question} | {self.get_choice_title()}'

    def get_choice_title(self):
        return self.choice.all()[0].title

    @property
    def points(self):
        if [choice.is_right for choice in self.choice.all()][0]:
            return self.question.points
        else:
            return 0.0

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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    test = models.ManyToManyField(Test)

    def answers(self):
         test = self.test.all()[0]  # NOQA[E111, E117]
         return [
             answer
             for answer in Answer.objects.filter(
                 user=self.user, question__in=[  # NOQA[E111]
                     question for question in test.questions.all()])]

    @property
    def points_earned(self):
        earned_points = sum(answer.points for answer in self.answers())
        return round(earned_points, 2)

    @property
    def max_points(self):
        return round(sum(test.max_points for test in self.test.all()), 2)

    def __str__(self):
        return f'{self.user} | {self.get_test()}  | {self.points_earned}/{self.max_points} | {self.get_in_perc()}%'

    def get_in_perc(self):
        return round((self.points_earned * 100 / self.max_points), 2)

    def get_test(self):
        return self.test.all()[0].title

    class Meta:
        ordering = ['user']
        db_table = 'results'
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
