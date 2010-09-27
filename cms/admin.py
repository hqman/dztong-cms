from django.contrib import admin
from models import Categories,Post,Profile


"""admin register"""

class CategoriesAdmin (admin.ModelAdmin):
        pass

admin.site.register(Categories,CategoriesAdmin)



class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/jquery-1.4.2.min.js','/static/js/tiny_mce/tiny_mce.js',
                '/static/js/tiny_mce/textareas.js',)




admin.site.register(Post,PostAdmin)

class ProfileAdmin (admin.ModelAdmin):
        pass

admin.site.register(Profile,ProfileAdmin)

