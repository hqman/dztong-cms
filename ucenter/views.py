#encoding=utf-8

from django.http import HttpResponse

from it.ucenter.discuz import Discuz
from it.ucenter import settings
from  django.conf import settings as project_settings
from django.contrib.auth.models import User
from it.ucenter.api import API
from django.db import transaction
from it.core.utils import log


REGISTER_STATUS={'-1':u'用户名不合法',
                 '-2':u'包含不允许注册的词语',
                 '-3':u'用户名已经存在',
                 '-4':'Email格式有误',
                 '-5':'Email不允许注册',
                 '-6':'该Email已经被注册'}

@transaction.commit_manually
def test(request):
    if request.method=='POST':
        username=request.REQUEST.get('username','')
        password=request.REQUEST.get('password','')
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(u'用户不存在')
            
     
        email=user.email
        from it.ucenter.client import Client
        client=Client(request)
      
        result=client.user_register(username,password,email)
        if not (result in REGISTER_STATUS):
            try:
                result=int(result)
                if result>0:
                    try:
                        from django.db import connection
                        rs=connection.cursor()
                        rs.execute('update auth_user set reference_id=%s where username=%s',[result,username])
                        rs.close()
                    except:
                        transaction.rollback()
                        raise
                    else:
                        transaction.commit()
                    return HttpResponse(u'注册成功  返回 uid %s ' % result)
                return HttpResponse(u'未知错误,返回代码  %s' % result)
            except:
                raise
                return HttpResponse(u'未知错误,返回 %s' % result)
        else:
            return HttpResponse(REGISTER_STATUS[result])
        
        
    else:
        return HttpResponse('''
        <html>
        <head>
        <title>手动同步账号到bbs</title>
        </head>
        <body>
        <form action='.' method='POST'>
        <table>
        <tr><td colspan='2'>输入您在亿脉通中的账号和密码</td></tr>
        <tr>
            <td>用户名</td><td><input type='text' name='username'></td>
        </tr>
        <tr>
        <td>口令</td>
        <td>
        <input type='password' name='password'>
        </td>
        </tr>
      
        </table>
        <center>
        <input type='submit' value='test register'/>
        </center>
        </form>
        </body>
        </html>
        
        ''')

def index(request):
    '''
    接受来自ucenter的调用
    qs 是一个词典,action,time每次均会有,其它的根据实际的情况有不同的参数
    
    通常url参数会有code,time但test action可能没有,下面代码需要重构,等确定那些有那些没有
    '''
    #目前不能处理非gbk编码

    code=request.REQUEST.get('code','').encode('gbk')
    
    try:
        time_t=int(request.REQUEST.get('time',0))
    except:
        time_t=0
        
   
    qs=Discuz.parse_str(Discuz.discuzAuthcode(code, settings.API_KEY,Discuz.DECODE))
    
    log(qs)
    time=int(qs.get('time',0))
    log("time=%s&code=%s" %(time_t,code))
    #timestamp = Discuz.unixTimestamp()
    
    
    if time_t and  (time_t - time> 3600): #3600秒 延迟
        return HttpResponse('Authracation has expiried')
 
    if not qs:
        return HttpResponse('Invalid Request')
  

    action = qs.get('action','')
    if action=='test':
        #测试
        return HttpResponse(settings.API_RETURN_SUCCEED)
    elif action=='deleteuser':
        #删除用户
        return API().delete_user(qs.get('ids',''))
     
    elif action=='renameuser':
        #改名用户
        return API().rename_user(qs.get('uid',0),qs.get('oldusername'),qs.get('newusername'))
    elif action=='updatepw':
        #更新用户密码
        return API().update_pw(qs.get('username',''),qs.get('password',''))
    
    elif action=='gettag':
        #获得tag
        return API().get_tag(qs.get('id',''))
    elif action=='synlogin':
        #同步登录
     
        return API(request).syn_login(qs.get('uid',0))
 
     
    elif action=='synlogout':
        #同步退出
        return API(request).syn_logout()
    elif action=='updatebadwords':
        #更新过滤词
        #return API().update_bad_words()
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='updatehosts':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='updateapps':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='updateclient':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='updatecredit':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='getcreditsettings':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    elif action=='getcredit':
        return HttpResponse(settings.API_RETURN_FORBIDDEN)
    
    
    return HttpResponse(settings.API_RETURN_SUCCEED)

