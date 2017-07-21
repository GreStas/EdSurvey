from django.contrib import admin
from .models import Question, Answer, AnswerLL


# class AnswerAdmin(admin.StackedInline):
class AnswerAdmin(admin.TabularInline):
    # list_display = ('content', 'ordernum', 'score')
    model = Answer


# class AnswerLLAdmin(admin.StackedInline):
class AnswerLLAdmin(admin.TabularInline):
    # list_display = ('content1', 'content2', 'ordernum1', 'ordernum2', 'score')
    model = AnswerLL


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'qtype')
    fieldsets = [
        (None,               {'fields': ['description', 'qtype']}),
        # ('Date information', {'fields': ['id'], 'classes': ['collapse']}),
    ]
    inlines = [
        AnswerAdmin,
        AnswerLLAdmin,
    ]


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description', 'qtype')


# @admin.register(Question)
# class AnswerLLAdmin(admin.StackedInline):
#     list_display = ('question', 'content1', 'content2', 'ordernum1', 'ordernum2', 'score')
#     model = AnswerLL

# admin.site.register(AnswerLL, AnswerLLAdmin)
