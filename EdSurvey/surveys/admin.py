from django.contrib import admin
from .models import Anketa
# from .models import Result, ResultRB, ResultCB, ResultLL

# В проде не будет админки, так как это будет приложение для пользователей


class AnketaAdmin(admin.ModelAdmin):
    model = Anketa

admin.site.register(Anketa, AnketaAdmin)
