from django.contrib import admin
from .models import *
# Register your models here.
# Inline Admin for Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Number of empty forms to display
    min_num = 4  # Ensure at least 4 options are present
    max_num = 4  # Allow at most 4 options


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    min_num = 1
    max_num = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'title',
                    'description', 'created_at', 'updated_at'
                    ]


# Admin for Question
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question_text']
    search_fields = ['question_text', 'quiz__title']
    list_filter = ['quiz']
    inlines = [OptionInline, AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer_text']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'option_text']
    list_filter = ['question']
    search_fields = ['option_text', 'question__text']
    list_select_related = ['question']  # Optimize related object queries

    def question(self, obj):
        return obj.question.text

    question.admin_order_field = 'question__text'  # Allow sorting by question text
    question.short_description = 'Question'  # Column header name


# student progress
@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz', 'question']


# @admin.register(OverallProgress)
# class OverallProgressAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'score']
