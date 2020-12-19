from django.contrib import admin
from .models import User, Listing, Bid, Comment_on_listing
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment_on_listing)