from django.db import models
POST_TYPES_DIC={'news':1,'wiki':2,'video':3}

class CategoriesManager (models.Manager):
    def getAll(self):
        return self.all()


class PostManager (models.Manager):
    def all_by_type(self,path):
        #path1=path.split("/")[1]
        if len(path)<3 :
	     	path='news'
        return self.get_query_set().filter(post_type=POST_TYPES_DIC[path])


