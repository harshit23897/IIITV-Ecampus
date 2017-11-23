from django.contrib import admin
from .models import (

    Courses,
    Result,
    Registers,
    Offers,
    FeeReceipt,

)
admin.site.register(Courses)
admin.site.register(Result)
admin.site.register(Registers)
admin.site.register(Offers)
admin.site.register(FeeReceipt)

