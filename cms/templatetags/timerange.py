# coding: utf-8
import datetime

from django import template
 

register = template.Library()


@register.filter(name='before')
def before(value):
    return before_now(value)




def before_now(atime):
    now = datetime.datetime.now()
    delta=now-atime
    if delta.days>0:
        if delta.days<30:
            return '%d天前' % delta.days
        else:
            months=delta.days/30
            if months<12:
                return '%d个月前' % months
            else:
                years=months/12
                return '%d年前' % years
                
    if delta.seconds<60:
        return '%d秒前' % delta.seconds
    minits=delta.seconds/60
    hours=minits/60
    if hours!=0:
        return '%d小时前' % hours
    if minits<60:
        return '%d分钟前' % minits
    
if __name__ == "__main__":
    now = datetime.datetime.now()
    d1 = now + datetime.timedelta(hours=-24*30*39)
    d2 = now + datetime.timedelta(seconds=-8)
    print before_now(d2)