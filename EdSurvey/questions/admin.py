from django.contrib import admin
from .models import Question, Answer, AnswerLL

# настройки для админки приложения


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('description', 'qtype')

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'content', 'ordernum', 'score')

admin.site.register(Answer, AnswerAdmin)


class AnswerLLAdmin(admin.ModelAdmin):
    list_display = ('question', 'content1', 'content2', 'ordernum1', 'ordernum2', 'score')

admin.site.register(AnswerLL, AnswerLLAdmin)
