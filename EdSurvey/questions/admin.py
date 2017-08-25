from django.contrib import admin
from .models import Question, Answer, AnswerRB, AnswerCB, AnswerLL


class AnswerAdmin(admin.ModelAdmin):
    # list_display = ('id', 'question', 'score', 'ordernum', 'content')
    model = Answer


class AnswerRBAdmin(admin.TabularInline):
    # list_display = ('id', 'question', 'score', 'ordernum', 'content')
    model = AnswerRB

# admin.site.register(AnswerRB, AnswerRBAdmin)


class AnswerCBAdmin(admin.TabularInline):
    # list_display = ('id', 'question', 'score', 'ordernum', 'content')
    model = AnswerCB

# admin.site.register(AnswerCB, AnswerCBAdmin)


class AnswerLLAdmin(admin.TabularInline):
    # list_display = ('id', 'question', 'score', 'ordernum', 'content', 'linkeditem', 'ordernumitem')
    model = AnswerLL

# admin.site.register(AnswerLL, AnswerLLAdmin)


class QuestionAdmin(admin.ModelAdmin):
    # model = Question
    list_display = ('id', 'name', 'description', 'qtype')
    ordering = ('id',)
    fieldsets = [
        (None, {'fields': ['name', 'description', 'qtype',]}),
        ('Приватность', {'fields': ['division', 'public', 'owner',]}),
    ]
    inlines = [
        AnswerRBAdmin,
        AnswerCBAdmin,
        AnswerLLAdmin,
    ]

admin.site.register(Question, QuestionAdmin)