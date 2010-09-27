#encoding=utf-8


class  XML(object):
    pass
    
class Discuz(object):
    ENCODE=1
    DECODE=2
    @classmethod
    def cutString(self,s,startIndex,length=0):
        '''
                从字符串的指定位置截取指定长度的子字符串
        @param s 原字符串
        @param startIndex 子字符串的起始位置
        @param length 子字符串的长度
        @returns 子字符串
      '''
        if not length:
            length=len(s)
        
        if startIndex>=0:
            if length<0:
                length=length*-1
                if (startIndex-length)<0:
                    length=startIndex
                    startIndex=0
                else:
                    startIndex=startIndex-length
            if startIndex>len(s):
                return ''
        else:
            if length<0:
                return ''
            else:
                if (length+startIndex)>0:
                    length +=startIndex
                    startIndex=0
                else:
                    return ''
                
      
        if (len(s)-startIndex)<length:
            length=len(s)-startIndex
        return s[startIndex:(startIndex+length)]
       
    
    @classmethod
    def parse_str(self,url):
        '''解析query_string,应该不包含path部分,?后面的部分
        @param url url
        @returns 词典
        '''
        if not url:
            return {}
        urls=url.split('&')
        result={}
        for item in urls:
            items=item.split('=')
            if len(items)>0 :
                result[items[0]]=items[1]
        
        return result
    @classmethod
    def fileExists(self,filename):
        '''检查文件是否存在
        @param filename 文件名 
        @return True或False
        '''
        import os
        return os.path.exists(filename)


    @classmethod
    def MD5(self,s):
        '''md5 '''
        import md5
        import hashlib
        m=md5.new()   
        m.update(s)   
        return m.hexdigest()   

    @classmethod
    def base64Encode(self,s):
        import base64
        return base64.encodestring(s)
    
    @classmethod
    def base64Decode(self,s):
        import base64
        print s
        return base64.decodestring(s)

      
    @classmethod
    def getKey(self,password,keyLength=256):
        '''用于rc4 处理密码
        @param password 密码,字符串,用ord取值
        @param keyLength 密钥长度,一般为256
        @returns 一个列表
        '''
        mBox=[]
        for  i in xrange(keyLength):
            mBox.append(i)
        j=0
        for i in xrange(keyLength):
            j=(j+mBox[i]+ord(password[i % len(password)])) % keyLength
            temp=mBox[i]
            mBox[i]=mBox[j]
            mBox[j]=temp
        return mBox
    @classmethod    
    def randomString(self,lens):
        '''生成随机字符
            @param lens 随机字符长度
            @returns 随机字符
        '''
        
        charArray=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        clens=len(charArray)
        sCode=[]
        import random
        for i in xrange(lens):
            sCode.append(charArray[random.randint(0,clens-1)])
        return ''.join(sCode)
        
    @classmethod
    def discuzAuthcodeEncode(self,source,key,expiry=0):
        '''使用discuz authcode 方法对字符串加密
        @param source 原始字符串
        @param key 密钥
        @param expiry 加密字串有效时间,单位是秒
        @returns 加密结果
        '''
        return self.discuzAuthcode(source,key,Discuz.ENCODE,expiry)
        
    
    @classmethod
    def discuzAuthcodeDecode(self,source,key):
        '''使用discuz authcode 方法对字符串解密
        @param source 原始字符串
        @param key 密钥
        @returns 解密结果
        '''

        return self.discuzAuthcode(source, key, Discuz.DECODE, 0);
    @classmethod
    def unixTimestamp(self):
        '''
        返回自1970.1.1以来的秒数
        '''
        import datetime
        dt_start=datetime.datetime(1970,1,1)
        dt_now=datetime.datetime.now()
        #microsecond为1百万分之一秒,需要转换为tick 每个计时周期表示一百纳秒，即一千万分之一秒
        t=(dt_now-dt_start)
        return t.days*24*60*60+t.seconds
    @classmethod
    def toString(self,a):
        return ''.join([chr(i) for i in a])
    @classmethod
    def discuzAuthcode(self,source,key,operation,expiry=0):
        '''
                    使用 变形的 rc4 编码方法对字符串进行加密或者解密
        @param source 原始字符串
        @param key 密钥
        @param operation 操作 ENCODE,DECODE
        @param expiry 过期时间
        @returns  加密或者是解密后的字符串
        // 随机密钥长度 取值 0-32;
        // 加入随机密钥，可以令密文无任何规律，即便是原文和密钥完全相同，加密结果也会每次不同，增大破解难度。
        // 取值越大，密文变动规律越大，密文变化 = 16 的 $ckey_length 次方
        // 当此值为 0 时，则不产生随机密钥
        '''
        if (not source) or (not key):
            return ''
        
        ckey_length=4
        timestamp=self.unixTimestamp()
        key=self.MD5(key)
        keya=self.MD5(self.cutString(key,0,16))
        keyb=self.MD5(self.cutString(key,16,16))
        if ckey_length:
            if operation==Discuz.DECODE:
                keyc=self.cutString(source,0,ckey_length)
            else:
                keyc=self.randomString(ckey_length)

        
        cryptkey = keya + self.MD5(keya + keyc)
        

        if operation == Discuz.DECODE:
            try:
                temp = self.base64Decode(self.cutString(source, ckey_length))
                
            except:
                # removed 正式版
               
                try:
                    temp = self.base64Decode(self.cutString(source + "=", ckey_length))
                except:
                    # removed 正式版
                
                    try:
                        
                        temp = self.base64Decode(self.cutString(source + "==", ckey_length))
                    except:
                        # removed 正式版
                    
                        return ''
           

            result = self.toString(self.RC4(temp, cryptkey))
            if (self.cutString(result, 10, 16) == self.cutString(self.MD5(self.cutString(result, 26) + keyb), 0, 16)):
           
                return self.cutString(result, 26);
            else:
                return ''
            
        else:
            #编码
            source = "0000000000" + self.cutString(self.MD5(source + keyb), 0, 16) + source;
            temp = self.RC4(source, cryptkey)
         
            return keyc + self.base64Encode(self.toString(temp))

    @classmethod
    def RC4(self,input,password):
        '''
        RC4 原始算法
        @param 原始字串数组
        @param 密钥
        @returns 处理后的字串数组
        '''

        if (not input) or (not password):
            return ''

          

        output = range(len(input))
        mBox = self.getKey(password, 256)

        #加密
        i = 0;
        j = 0;
        for offset in xrange(len(input)):
                
            i = (i + 1) % len(mBox)
            j = (j + mBox[i]) % len(mBox)
            temp = mBox[i];
            mBox[i] = mBox[j];
            mBox[j] = temp;
            a = ord(input[offset])
           
            b = mBox[(mBox[i] + mBox[j]) % len(mBox)]
            output[offset]= a ^ b
        return output
    
    def ascArr2Str(b):
        pass
    
#        public static string AscArr2Str(byte[] b)
#        {
#            return System.Text.UnicodeEncoding.Unicode.GetString(
#             System.Text.ASCIIEncoding.Convert(System.Text.Encoding.ASCII,
#             System.Text.Encoding.Unicode, b)
#             );
#        }

#        public static string UnixTimestamp()
#        {
#            DateTime dtStart = TimeZone.CurrentTimeZone.ToLocalTime(new DateTime(1970, 1, 1));
#            DateTime dtNow = DateTime.Parse(DateTime.Now.ToString());
#            TimeSpan toNow = dtNow.Subtract(dtStart);
#            string timeStamp = toNow.Ticks.ToString();
#            return timeStamp.Substring(0, timeStamp.Length - 7);
#        }





