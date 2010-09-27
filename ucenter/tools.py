#encoding=utf-8
import sys
sys.path.append('e:\\works\\it\\src')

import os
os.environ['DJANGO_SETTINGS_MODULE']='it.settings'
from it.ucenter.discuz  import Discuz
from it.ucenter.client import Client,MockRequest
from it.ucenter import settings
from django.contrib.auth.models import User
from django.db import transaction

def import_user():
    '''导入亿脉通所有用户'''
    users=User.objects.all()
    from django.db import connection
    client=Client(MockRequest())
    for user in users:
        print 'import %s '  % user.username
        username=user.username
      
        id= client.user_register(username,'123456',user.email)
        
        if int(id)>0:
            rs=connection.cursor()
            rs.execute('update auth_user set reference_id=%s where id=%s',[id,user.id])
            rs.close()

@transaction.commit_manually            
def import_user_by_name(username,password):
    '''导入亿脉通所有用户'''
    user=User.objects.get(username=username)
    from django.db import connection
    client=Client(MockRequest())
   
    print 'import %s '  % username
   
    s= client.user_register(username,password,user.email)
    print s
    return
    
    if int(id)>0:
        try:
            rs=connection.cursor()
            rs.execute('update auth_user set reference_id=%s where id=%s',[id,user.id])
            rs.close()
        except:
            transaction.rollback()
            raise   
        else:
            transaction.commit()
                      
@transaction.commit_manually           
def update_reference_id():
    users=User.objects.all()
    from django.db import connection
    client=Client(MockRequest())
    for user in users:
        results=client.user_get_user(user.username)
        if results and int(results[0])>0:
            rs=connection.cursor()
            rs.execute('update auth_user set reference_id=%s where id=%s',[results[0],user.id])
@transaction.commit_manually   
def update_user_reference_id(username):
    users=User.objects.all()
    from django.db import connection
    client=Client(MockRequest())

    results=client.user_get_user(username)
    print results
    id= int(results[0])
    if results and id>0:
        print 'test'
        try:
            rs=connection.cursor()
            rs.execute('update auth_user set reference_id=%s where username=%s',[id,username])
            
            
        except:
            transaction.rollback()
            raise
        else:
            transaction.commit()
            
        
        
        
        rs.close()
def delete_all():
    users=User.objects.all()
    client=Client(MockRequest())
    for user in users:
        results=client.user_get_user(user.username)
        if results and int(results[0])>0:
            client.user_delete(results[0])
        
if __name__=='__main__':
    #delete_all()
    #import_user()
    import_user_by_name('jiangjianxiao','123456')
   