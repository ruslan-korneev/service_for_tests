from django.contrib import admin
from apps.polls.models import Answer, Choice, Question, Result, RightChoice


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__', 'points',)
    list_filter = ('points',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_correct_answers', 'points',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('points_earned',)


@admin.register(RightChoice)
class RightChoiceAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
