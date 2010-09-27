from django.db import models
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

class DZCommentManager(models.Manager):
     def in_public(self):
        return self.get_query_set().filter(is_public = True, is_removed = False).order_by('-date')