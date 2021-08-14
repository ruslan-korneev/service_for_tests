from django.contrib import admin
from apps.polls.models import (
    Answer,
    Choice,
    Question,
    Result,
    Test,
)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__', 'points',)
    list_filter = ('points',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_correct_answers', 'points',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('points_earned',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
#     inlines = [QuestionInline,]
