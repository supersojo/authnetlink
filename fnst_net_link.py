#!/bin/python
# -*- coding: utf-8 -*-
#

#
# auto complete network connection certification
#

import urllib2
import urllib
import cookielib

#
# proxy enable
#


class FnstNetLinkAuth(object):
    '''
    auto complete network connnection auth
    '''
    login_url = 'http://10.167.197.50:90/login'
    refer_url = 'http://10.167.197.50:90/p/30247dd99271a6806206be0598a1cf9e/index.html?aHR0cDovL2JhaWR1LmNvbS8='
    def __init__(self,user=None,passwd=None,debug=None):
        self.user = user
        self.passwd = passwd
        self.debug=debug
        
    def __debug_info(self,str):
        if self.debug:
            print '<FnstNetLinkAuth>',str
            
    def set_proxy(self,proxy=None):
        '''
        proxy ={proxy_type,proxy_address}
        proxy_typ:http or https ot socks?
        proxy_address:url of proxy server
        '''
        if proxy.has_key('http')==False and \
           proxy.has_key('https')==False:
            self.__debug_info('proxy type is not supported!')
            return
        self.proxy = proxy

    def __get_url_opener(self,enable_proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        if enable_proxy==True:
            if self.proxy.has_key('http')==True or \
               self.proxy.has_key('https')==True:
                proxy_handler = urllib2.ProxyHandler(self.proxy)
                opener = urllib2.build_opener(proxy_handler,cookie_support)
            else:
                null_proxy_handler = urllib2.ProxyHandler({})
                opener = urllib2.build_opener(null_proxy_handler,cookie_support)
        else:
            null_proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(null_proxy_handler,cookie_support)
        
        return opener
        
  
    def __mc(self,a):
        '''
        code derived from /script/crypt.js
        '''
        ret=''
        b="0123456789ABCDEF"
        if a==' ':
            ret='+'
        elif ((a<'0' and a!='-' and a!='.') or \
              (a<'A' and a>'9') or \
              (a>'Z' and a<'a' and a!='_') or \
              (a>'z')):
            ret='%'
            ret+=b[ord(a)>>4]
            ret+=b[ord(a)&15]
        else:
            ret=a
        
        return ret
        
    def __m(self,a):
        '''
        code derived from /script/crypt.js
        '''
        return (((a&1)<<7)|((a&(0x2))<<5)|((a&(0x4))<<3)|((a&(0x8))<<1)|((a&(0x10))>>1)|((a&(0x20))>>3)|((a&(0x40))>>5)|((a&(0x80))>>7))
        
    def __md6(self,a):
        '''
        code derived from /script/crypt.js
        '''
        b=''
        for i in range(len(a)):
            c=self.__m(ord(a[i]))^(0x35^(i&0xff))
            #d=c.toString(16);
            b+=self.__mc(chr(c))
     
        return b

    def auth_netlink(self,url=None,enable_Proxy=None):
        '''
        auth user login
        '''
        if url==None:
            return False
        opener = self.__get_url_opener(enable_Proxy)
        #
        # let headers empty
        # so cusume the headers
        req = urllib2.Request(url,headers={})
        req.add_header('Accept','application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, */*')
        req.add_header('Referer',FnstNetLinkAuth.refer_url)
        req.add_header('Accept-Language','zh_CN')
        req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729;Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)')
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        req.add_header('Accept-Encoding','gzip, deflate')
        
        #print req.get_data()
        #print req.get_full_url()
        #print req.get_host()
        #print req.get_method()
        #print req.get_origin_req_host()
        #print req.get_selector()
        #print req.get_type()
        #print req.has_data()
        #print req.has_proxy()
        #print req.header_items()
        magic_pass = self.__md6(self.passwd)
        
        data={'uri':'aHR0cDovL2JhaWR1LmNvbS8=',
              'terminal':'pc',
              'login_type':'login',
              'check_passwd':'0',
              'show_tip':'block',
              'short_message':'none',
              'show_captcha':'none',
              'show_read':'block',
              'show_assure':'none',
              'username':self.user,
              'assure_phone':'',
              'password1':self.passwd,
              'password':magic_pass,
              'new_password':'',
              'retype_newpassword':'',
              'captcha_value':'',
              'read':'1',
        }
        encoded_data = urllib.urlencode(data)
        
        response = opener.open(req,encoded_data).read()
        #print response.decode('utf-8')
        #
        # check data from server
        # find str from response
        ok = '用户认证成功'
        login_already = '已成功登陆'
        ret1 = response.find(ok)
        ret2 = response.find(login_already)
        
        if ret1<0 and ret2<0:
            #
            # not find ok
            #
            return False
        else:
            return True

        
if __name__=='__main__':
    fnst_auth = FnstNetLinkAuth('xxxx','xxxxxx')
    ret = fnst_auth.auth_netlink(FnstNetLinkAuth.login_url)
    if ret:
        print 'ok'
    else:
        print 'error'