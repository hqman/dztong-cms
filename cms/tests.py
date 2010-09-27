# -*- coding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from manager import CategoriesManager
from django.test import TestCase
from models import Categories
from ucenter.discuz  import Discuz

import urllib

 


#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.failUnlessEqual(1 + 1, 2)
#
#class CateTests (TestCase):
#    def test_get_all(self):
#        c=Categories()
#        c.name='c'
#        c.save()
#        rs=Categories.objects.getAll()
#        for i in rs:
#            print i.id
#        self.failUnlessEqual(len(rs), 1)
        
class CookieTest (TestCase):
    def test_basic_addition(self):
        authstr="9615Nda1T2WXeZqWRhPo8PeljcehjwH8wyvUyBmV63G%2FL2F2EAnHiaa5BfEcqM%2Fpb77Qa9NVoB6PZGGrmhl%2F"
        #print authstr
        #s= Discuz.discuzAuthcode("123456", "123456", Discuz.ENCODE, 1000)
        
        #self.assertTrue( Discuz.discuzAuthcode(s, u'中文密码'.encode('utf-8'), Discuz.DECODE,1000)==u"中文".encode('utf-8'))
         #解密
        print "解密-------------"
        str="c941zYjA6U%2F42iiaTKrdOiv0Nv7GmlKyqmVlrtxOuxHLIrNZC%2FQu8ZD6WNDQv1%2BPYHply48DN21sS9ND8PSrSw"

        value_s=Discuz.discuzAuthcode(urllib.unquote(str),"Fd13T2p5a6L4VfacV4j0Vdr3yf32Z9Ccj1nc38c0d289B0C8m0K4p5L9h6Z3R2fa",Discuz.DECODE)
        print value_s
        

 
    
    



__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

 




