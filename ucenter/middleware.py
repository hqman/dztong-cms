#encoding=utf-8
from dztong.ucenter import settings
from dztong.ucenter.discuz import Discuz
from django.contrib.auth.models import AnonymousUser,User

import urllib

def set_user(request):
    if settings.UC_COOKIE_KEY in request.COOKIES:
        value=request.COOKIES[settings.UC_COOKIE_KEY]
        value=urllib.unquote(value)
        #如果有cookie但值为null或无法解析,则默认为退出
        if not value:
            request.user= AnonymousUser()
            return
        #解密
        value_s=Discuz.discuzAuthcodeDecode(value,settings.API_KEY)
        if not value_s:
            request.user=AnonymousUser() #退出
            print 'get no cookie'
            return
        username,uid=value_s.split(',')
        print "get cookie username %s uid %s",username ,uid
        #todo 创建一个需要激活的用户
        if uid and username:
        #           存在uid和username
            try:
                request.user=User.objects.get(username=username)
            except User.DoesNotExist:
                print "DoesNotExist"
                newUser=User(username=username)
                newUser.save()
                request.user=newUser
                #request.user=AnonymousUser()


class AuthenticationMiddleware(object):
    def process_request(self, request):
        #assert hasattr(request, 'user'), u"The it authentication middleware requires django authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'."
        if request.path.startswith('/static') or request.path.startswith('/__debug') or request.path=='/accouent/login':
            return None
        print request.path

        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
            set_user(request)
        if not  request.user.is_authenticated():
            set_user(request)
        return None

