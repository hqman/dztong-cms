#encoding=utf-8

from django.http import HttpResponse

from it.ucenter import settings
from it.ucenter.discuz import Discuz
from django.contrib.auth.models import User
from it.core.utils import log


class API(object):
    def __init__(self,request=None):
        self.request=request
    def get_tag(self,id):
        '''应用程序的标签数据传递给ucenter
        
        @param id 标签名称
        '''
        if settings.API_GETTAG:
            return HttpResponse('')
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    def syn_logout(self):
        '''
        同步退出
        @param uid 
        '''
        if settings.API_SYNLOGOUT:
#            from django.contrib.auth import logout
#            logout(self.request)
            resp=HttpResponse()
        
            resp['P3P: CP']='CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR'
            resp.set_cookie(settings.UC_COOKIE_KEY, '',None,None)
            return resp
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    def syn_login(self,uid):
        '''
        同步登录
        @param uid 
        '''
        #检查是否允许

        if settings.API_SYNLOGIN:
            #获取对应用户
            try:
         
                user=User.objects.extra(where=['reference_id=%s'],params=[uid])[0]
                username=user.username
            except:
                username=''
            
                 
#                from django.contrib.auth import login,get_backends
#                backend=get_backends()[0]
#                user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
#                login(self.request,user)
            resp=HttpResponse()
            
            resp['P3P: CP']='CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR'
            value=Discuz.discuzAuthcodeEncode('%s,%s' % (uid,username), settings.API_KEY)
            resp.set_cookie(settings.UC_COOKIE_KEY, value, 86400*365,86400*365)
            return resp
                             
          
            
           
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    def update_pw(self,username,password):
        '''
        更改用户密码
        @param username 用户名
        @param password 密码
        '''
        if settings.API_UPDATEPW:
            try:
                print usernmae,password
                return HttpResponse(settings.API_RETURN_SUCCEED)
            except Exception,e:
                return HttpResponse(settings.API_RETURN_FAILED)
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    def rename_user(self,uid,oldusername,newusername):
        '''
        改名用户
        @param uid 
        @param oldusername
        @param newusername
        @return 改名成功返回 API_RETURN_SUCCESS,失败返回API_RETURN_FAILED,不允许返回API_RETURN_FORBIDDEN
        '''
        if settings.API_RENAMEUSER:
            #改名用户
            try:
                return HttpResponse(settings.API_RETURN_SUCCEED)
            except Exception,e:
                return HttpRespones(settings.API_RETURN_FAILED)
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
            
    def delete_user(self,ids):
        '''
    删除用户,对应action deleteuser
    @params ids 用逗号分隔的用户id
    @return 删除成功则输出 API_RESTURN_SUCCEED
    
    '''
        if settings.API_DELETEUSER:
            #删除用户
            try:
                #删除用户
                return HttpResponse(settings.API_RETURN_SUCCEED)
            except Exception,e:
                #记录日志

                return HttpResponse(settings.API_RETURN_FAILED)
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
