from django.contrib import admin

from .models import REVIEWS
from .models import URL

# Register your models here.
admin.site.register(URL)
admin.site.register(REVIEWS)
admin.site.site_header = 'PhishRod administration'
