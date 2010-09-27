#encoding=utf-8
from it.ucenter import settings
from it.ucenter.discuz import Discuz

class MockRequest(object):
    def __init__(self):
        self.META={'HTTP_USER_AGENT':'Mozilla/4.0 (compatible; MSIE 6.0;Windows NT 5.0)'}
        
def uc_unserialize(s):
    import xml.dom.minidom
    doc=xml.dom.minidom.parseString(s) 
    results=[]
    for node in doc.documentElement.childNodes:
        if not  node.nodeName or not node.nodeName.startswith('item'):
            continue
        if len(node.childNodes)>0:
            results.append(node.childNodes[0].nodeValue)
        else:
            results.append(node.nodeValue)
    return results       
class Client(object):
    
    def __init__(self,request):
        self.request=request
    def app_ls(self):
        '''获取应用列表
        @return  <?xml version="1.0" encoding="ISO-8859-1"?><root> <item_1> <appid><![CDATA[1]]></appid> <type><![CDATA[DISCUZ]]></type> <name><![CDATA[亿脉通]]></name> <url><![CDATA[http://www.51ymt.com/bbs]]></url> <tagtemplates> <item> <0_attr> <id><![CDATA[template]]></id> </0_attr> <item_0><![CDATA[<a href="{url}?sid=" target="_blank">{subject}</a>]]></item_0> <1_attr> <id><![CDATA[fields]]></id> </1_attr> <item_1> <item> <0_attr> <id><![CDATA[subject]]></id> </0_attr> <item_0><![CDATA[标题]]></item_0> <1_attr> <id><![CDATA[uid]]></id> </1_attr> <item_1><![CDATA[用户 ID]]></item_1> <2_attr> <id><![CDATA[username]]></id> </2_attr> <item_2><![CDATA[发帖者]]></item_2> <3_attr> <id><![CDATA[dateline]]></id> </3_attr> <item_3><![CDATA[日期]]></item_3> <4_attr> <id><![CDATA[url]]></id> </4_attr> <item_4><![CDATA[主题地址]]></item_4> </item> </item_1> </item> </tagtemplates> <viewprourl><![CDATA[]]></viewprourl> <synlogin><![CDATA[1]]></synlogin> </item_1> <item_2> <appid><![CDATA[2]]></appid> <type><![CDATA[OTHER]]></type> <name><![CDATA[YMT]]></name> <url><![CDATA[http://www.51ymt.com]]></url> <tagtemplates> <item><![CDATA[]]></item> <item_0> <id><![CDATA[template]]></id> </item_0> </tagtemplates> <viewprourl><![CDATA[]]></viewprourl> <synlogin><![CDATA[1]]></synlogin> </item_2></root>
        '''
        return self.uc_api_post('app','ls',{})
    
    
    def user_addprotected(self,username, admin=''):
        return uc_api_post( 'user', 'addprotected', {'username':username, 'admin':admin});

    def user_deleteprotected(self,username):
        return uc_api_post( 'user', 'deleteprotected', {'username':username})

    def user_getprotected(self):
        '''
        得到受保护的用户名列表
        @return array 
        '''
        return uc_unserialize(self.uc_api_post( 'user', 'getprotected', {'1':1}))


    def user_get_user(self,username, isuid=0):
        '''
        @return list 用户id,用户名,电子邮件 
        
        用户不存在返回[0],否则返回list
        '''
        result=self.uc_api_post('user', 'get_user', {'username':username, 'isuid':isuid})
        if result=='0':
            return [result]
        return uc_unserialize(result)
    

    def user_merge(self,oldusername, newusername, uid, password, email):
        '''把重名用户合并到 UCenter
        @param oldusername
        @param newusername
        @param uid
        @param password
        @param email
        @return 大于 0:返回用户 ID，表示用户注册成功
-1:用户名不合法
-2:包含不允许注册的词语
-3:用户名已经存在'''
        return self.uc_api_post('user', 'merge', {'oldusername':oldusername, 'newusername':newusername, 'uid':uid, 'password':password, 'email':email})

    def user_merge_remove(self,username):
        '''
        移除重名用户记录
        @param username 用户名
        '''
        return self.uc_api_post( 'user', 'merge_remove',{'username':username})


    def user_getcredit(appid, uid, credit):
        '''
        获取指定应用的指定用户积分
        @param appid 应用id integer
        @param uid 用户id integer
        @param credit 积分编号   integer
        @return 积分 integer
        '''
        return self.uc_api_post( 'user', 'getcredit', {'appid':appid, 'uid':uid, 'credit':credit})
    def user_synlogin(self,uid):
        '''
        同步登录,返回同步登录的html代码,类似
        <script type="text/javascript" src="http://localhost:3333/api/uc.php?time=1231999701&code=6e3bAW%2F5Ab1EqHIqnn6OGiCJjJbzNiqNW7tDyXnjv%2FE9aOxQyuf1CorIOyJ80G%2B9QrI4Lvu5DqIjgOvCRtB6H5W3SJjOvclK%2F8zej%2FOy2QF3fmTRBww5nD8aoimqQULLHvK0gxcKmn4xiWnXMlyylDTCEwVUmEzqItmJQbNBs%2F4t23k" reload="1"></script>
        
        
        '''
        return self.uc_api_post('user','synlogin',{'uid':uid})

 
    def user_synlogout(self):
        '''同步退出
      
        '''
      
        return self.uc_api_post("user", "synlogout", {});

    def user_edit( username,  oldpw,  newpw,  email,  ignoreoldpw):
        '''
        更新用户资料
        @param username 用户名
        @param oldpw 旧密码
        @param newpw 新密码,如不修改为空
        @param email email 如不修改为空
        @param ignoreoldpw  是否忽略旧密码 1:忽略，更改资料不需要验证密码 0:(默认值) 不忽略，更改资料需要验证密码
        @return    /// 1:更新成功
    /// 0:没有做任何修改
    /// -1:旧密码不正确
    /// -4:Email 格式有误
    /// -5:Email 不允许注册
    /// -6:该 Email 已经被注册
    /// -7:没有做任何修改
    /// -8:该用户受保护无权限更改
        '''
        
        postData={'uesrname':username,'oldpw':oldpw,'newpw':newpw,'email':email,'ignoreoldpw':ignoreoldpw}
  
        return self.uc_api_post("user", "edit", postData)
         
 

    def  user_deleteavatar(uid):
        '''删除用户头像
        @param uid 用户名
        '''
        uc_api_post('user', 'deleteavatar', {'uid':uid});

    def user_check_username(self,username):
        '''检查用户名
        @param username
        @return 
        1:成功
-1:用户名不合法
-2:包含要允许注册的词语
-3:用户名已经存在

        '''
        
        postData={'username':username}
        return self.uc_api_post('user','check_username',postData)

    def user_delete(self,uid):
        '''
        删除用户
        @param uid user id 文档有误
        @return 1 成功,0 失败'''
        return self.uc_api_post('user','delete',{'uid':uid})
    def user_register(self,username,password,email,questionid='',answer=''):
        '''
        用户注册
        @param username 用户名
        @param password 密码
        @param email 电子邮件
        @param questionid 问id 可选
        @param answer 回答 可选
        @return  integer 
                大于0 返回用户id,表示用户注册成功,其它
        ///-1:用户名不合法
        ///-2:包含不允许注册的词语
        ///-3:用户名已经存在
        ///-4:Email 格式有误
        ///-5:Email 不允许注册
        ///-6:该 Email 已经被注册
         
        '''
        postData={'username':username,'password':password,'email':email,'questionid':questionid,'answer':answer}
        
  

        return self.uc_api_post("user", "register", postData);
    def user_check_email(self,email):
        '''检查email
        @param email 电子邮件 
        @return 1:成功
-4:Email 格式有误
-5:Email 不允许注册
-6:该 Email 已经被注册 注意后台可能允许重复注册,此时重复邮件也会被返回合法
'''
        return self.uc_api_post('user','check_email',{'email':email})
    
   
    def user_login(self,username,password,isuid=0,checkques = 0, questionid = '', answer = ''):
        '''
        用户登录
        @param username 用户名
        @param password 口令
        @param isuid 是否用uid登录 ,0
        @return dict
        ''' 

                        
        postData ={'username':username,'password':password,'isuid':isuid,'checkques':checkques,'questionid':questionid,'answer':answer}

        return  uc_unserialize(self.uc_api_post( "user", "login",  postData))
        
   
    def uc_api_post(self,module,action,postDataInfo={}):

        import urllib
        postdata = self.uc_api_requestdata(module, action, urllib.urlencode(postDataInfo))
        #需要加上/
        return self.get(settings.UC_URL ,  postdata,userAgent=self.request.META["HTTP_USER_AGENT"])
    def uc_api_requestdata(self,momodule, action,  requestdata):
        input = self.uc_api_input(requestdata)
        
        return {'m':momodule,
                'a':action,
                'inajax':2,
                'input':input,
                'appid':settings.APP_ID}
    def uc_api_input(self,data):
    
     
        postdata =("%s&agent=%s&time=%s" % (data, Discuz.MD5(self.request.META["HTTP_USER_AGENT"]), Discuz.unixTimestamp()))
        postdata = Discuz.discuzAuthcodeEncode(postdata, settings.API_KEY);

        return postdata
                      
    def get(self,url,postData, timeout=3000,userAgent="Mozilla/4.0 (compatible; MSIE 6.0;Windows NT 5.0)",method='GET'):
        import urllib
        import httplib

        headers = {'Accept-Language':'zh-cn','Accept-Encoding': 'gzip, deflate','User-Agent': userAgent,'Connection':' Keep-Alive',
        }
       

        conn = httplib.HTTPConnection(settings.UC_IP,settings.UC_PORT)
        import urllib
        t="%s?%s" %( url, urllib.urlencode(postData))
   
        conn.request(method,t,'',headers=headers)
        res = conn.getresponse()
        data = res.read()
        
          
        return data;
          