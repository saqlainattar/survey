from django.contrib import admin
from .models import Question, Choice, Answer, Survey, Response


class ChoiceInline(admin.TabularInline):

    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):

    model = Question
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on')
    inlines = (QuestionInline, )


class QuestionAdmin(admin.ModelAdmin):
    list_display_links = ('display_link', )
    list_display = ('display_link', 'survey', 'question_text', 'serial_number')
    list_editable = ('question_text', 'survey', 'serial_number')
    inlines = (ChoiceInline, )

    list_filter = ('survey', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'choice')
    list_filter = ('response', 'question', 'choice')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey')
    list_filter = ('user', 'survey')


class ChoiceAdmin(admin.ModelAdmin):
    list_filter = ('question', 'possitive_count')
    list_display = ('question', 'choice_text', 'serial_number', 'possitive_count')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Response, ResponseAdmin)
