from django.contrib import admin
from .models import Anketa
# from .models import Result, ResultRB, ResultCB, ResultLL

# В проде не будет админки, так как это будет приложение для пользователей


class AnketaAdmin(admin.ModelAdmin):
    model = Anketa

admin.site.register(Anketa, AnketaAdmin)


# class ResultRBAdmin(admin.TabularInline):
#     model = ResultRB
#
#
# class ResultCBAdmin(admin.TabularInline):
#     model = ResultCB
#
#
# class ResultLLAdmin(admin.TabularInline):
#     model = ResultLL
#
#
# class ResultAdmin(admin.ModelAdmin):
#     model = Result
#     inlines = [
#         ResultRBAdmin,
#         ResultCBAdmin,
#         ResultLLAdmin,
#     ]
#
# admin.site.register(Result, ResultAdmin)
