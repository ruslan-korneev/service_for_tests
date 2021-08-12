from django.contrib import admin
from .models import Question, Answer, Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'visible', 'max_points',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'points', 'lock_other',)
    list_filter = ('question',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice',)
    list_filter = ('user',)
