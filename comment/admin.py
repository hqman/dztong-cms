from django.conf import settings
from django.contrib import admin

from dztong.comment.models import DZComment

class DZCommentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(DZComment, DZCommentsAdmin)