#encoding=utf-8
import sys
sys.path.append('c:\\works\\xx\\src')

import unittest
import os
os.environ['DJANGO_SETTINGS_MODULE']='xx.settings'
from it.ucenter.discuz  import Discuz
from it.ucenter.client import Client,MockRequest
from it.ucenter import settings
from it.ucenter.api import API

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        request=MockRequest()
        self.client=Client(request)
#    def testUserRegister(self):
#        print self.client.user_register('ggl','123456','ucenter@gmail.com')
    def testAPPLs(self):
        print self.client.app_ls()
    def testSynLogin(self):
        uid=self.client.user_login('ucenter','123456')[0]
        self.assertTrue(int(uid)>0)
        print self.client.user_synlogin(uid)
        
    def testCheckEmail(self):
        self.assertEquals(int(self.client.user_check_email('ucenter@gmail.com')),1) #已经存在,但后台允许重复注册的情况下
    def testGetUser(self):
        print self.client.user_get_user('ucenter')
    def testUserLogin(self):

        self.assertTrue( int(self.client.user_login('admin','123456')[0])>0)
        print self.client.user_login('ucenter','12345678')
        self.assertEquals( int(self.client.user_login('ucenter','12345678')[0]),-2) #密码错
        self.assertEquals( int(self.client.user_login('ucednter','12345678')[0]),-1) #用户不存在,或者被删除
    def testCheckUserName(self):
        self.assertTrue(int( self.client.user_check_username('ucenter'))==-3) #用户名已经存在
        self.assertTrue(int( self.client.user_check_username(u'蒋建校'.encode('gbk')))==1) #合法
#    def testGet(self):
#        settings.UC_IP='121.9.205.179'
#        settings.UC_PORT='80'
#        self.client.get('/',{})
#    def testPOST(self):
#        settings.UC_IP='121.9.205.179'
#        settings.UC_PORT='80'
#        self.client.get('/login/',{'username':'ucenter','password':'123456'},method='POST') 
    
    
        
class DiscuzTestCase(unittest.TestCase):
    '''测试discuz.py '''
    def setUp(self):
        pass
    def testCutString(self):
        self.assertEqual(Discuz.cutString('abc',0),'abc')
   
    def testParseStr(self):
        result=Discuz.parse_str("a=1&b=2")
        self.assertEqual(len(result),2)
        self.assertTrue('a' in result)
        self.assertTrue('b' in result)
        self.assertTrue(result['a']=='1')
        self.assertTrue(result['b']=='2')
    def testFileExist(self):
        self.assertTrue(Discuz.fileExists(r'c:/dt.bak'))
    def testMD5(self):
        self.assertTrue( Discuz.MD5('123456')=='e10adc3949ba59abbe56e057f20f883e')
    def testBase64(self):
        s= Discuz.base64Encode('123456')
        self.assertTrue('123456'==Discuz.base64Decode(s))
    def testGetKey(self):
        self.assertTrue( len(Discuz.getKey('1234567890'))==256)
    def testRandomStr(self):
        self.assertTrue(len( Discuz.randomString(256))==256) 
    def testRC4(self):
        self.assertTrue( Discuz.RC4('123456','123456')==[49, 202, 77, 83, 17, 5])
    def testUnixTimestamp(self):
        print Discuz.unixTimestamp()
    def testDiscuzAuthcode(self):
        s= Discuz.discuzAuthcode("123456", "123456", Discuz.ENCODE, 1000)
        print s
        self.assertTrue( Discuz.discuzAuthcode(s, '123456', Discuz.DECODE,1000)=="123456")
        s= Discuz.discuzAuthcode("中文", "中文密码", Discuz.ENCODE, 1000)
        self.assertTrue( Discuz.discuzAuthcode(s, '中文密码', Discuz.DECODE,1000)=="中文")
        s= Discuz.discuzAuthcode(u"中文".encode('utf-8'), u"中文密码".encode('utf-8'), Discuz.ENCODE, 1000)
        self.assertTrue( Discuz.discuzAuthcode(s, u'中文密码'.encode('utf-8'), Discuz.DECODE,1000)==u"中文".encode('utf-8'))
     
        

class APITestCase(unittest.TestCase):
    def setUp(self):
        pass
    def testSynLogout(self):
        API().syn_logout()
    def testLogin(self):
        API().syn_login(258) #ucenter
    def testParse(self):

        print     Discuz.parse_str(Discuz.discuzAuthcode('9949DdD0eUd4j+HIq8SIR4zDxr02OKaqn2+0D8X0+XDuZNs17mpg7K5xXdTe/qHLBul0p25SD+Q', settings.API_KEY,Discuz.DECODE))
    
