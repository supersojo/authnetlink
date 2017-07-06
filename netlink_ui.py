#!/bin/python
# -*- coding: utf-8 -*-

# for wx package
import wx

# for international
import gettext

# for custom event
import event_util

# for multi-threading
import threading

# for sleep
from time import ctime,sleep

# for task proxy
import task_util

# for net link auth
import fnst_net_link

import traceback

class LayoutWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE | wx.MINIMIZE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.__add_components()
        self.Bind(event_util.EVT_NOTIFY_EVENT,self.onNotifyEvent)
        self.Bind(wx.EVT_CLOSE,self.onCloseEvent)
        self.ok.Bind(wx.EVT_LEFT_DOWN,self.onOk)
        self.task_proxy = task_util.TaskProxy()
        self.task_proxy.start_proxy()
        self.timeout_map = set()
        
    def onCloseEvent(self, event):
        self.task_proxy.quitrun()
        event.Skip()
        
    def onNotifyEvent(self, event):
        data = event.GetData()
        #
        # get Data from event , check data then update ui
        #
        #print event
        timeout = False
        for id in self.timeout_map:
            if id==data['id']:
                print 'already timeout'
                timeout = True
                break
        if timeout:
            self.timeout_map.remove(id)
            self.edit.SetLabelText(self.edit.GetLabelText()+'net link timeout\r\n')
        else:
            if data['ret']:
                self.edit.SetLabelText(self.edit.GetLabelText()+'net link ok\r\n')
            else:
                self.edit.SetLabelText(self.edit.GetLabelText()+'net link error\r\n')
        self.ok.Enable(True)
        
    def net_link_config(self,*args,**kwargs):
        # use your username and password
        fnst_auth = fnst_net_link.FnstNetLinkAuth('xxxx','xxxx')
        ret = fnst_auth.auth_netlink(fnst_net_link.FnstNetLinkAuth.login_url)
        evtOut = event_util.NotifyEvent(event_util.wxNotifyEvent,self.GetId())
        evtOut.SetData({'ret':ret,'msg':'','id':1234})
        self.QueueEvent(evtOut.Clone())
       
    def callback_timeout(self,*args):
        # record timeout task
        self.timeout_map.add(args[0])

    def onOk(self, event):
        self.task_proxy.submit_task({'id':1234,'run':self.net_link_config,'args':(1,2,'haha'),'timeout':3,'callback_timeout':self.callback_timeout,'callback_args':1234})
        self.ok.Enable(False)
        
    def __add_components(self):
        self.panel = wx.Panel(self,-1)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.ok = wx.Button(self.panel,wx.ID_ANY,_("Auth"))
        self.edit = wx.TextCtrl(self.panel,wx.ID_ANY,_(""),wx.DefaultPosition,wx.DefaultSize,wx.TE_MULTILINE)
        self.edit.SetEditable(False)
        # must add some to hbox1, or else it ocupy no space
        self.hbox1.Add(self.edit,1,wx.EXPAND)
        self.hbox2.Add(self.ok)
        
        
        self.vbox.Add(self.hbox1,1,wx.EXPAND)
        self.vbox.Add(self.hbox2,0,wx.ALIGN_CENTER|wx.RIGHT|wx.BOTTOM,5)
        self.panel.SetSizer(self.vbox)
        
class LayoutApp(wx.App):
    def OnInit(self):
        frame = LayoutWindow(None, wx.ID_ANY, "LayoutExample")
        frame.Show(True)
        return True

if __name__ == "__main__":
    gettext.install("FnstTool") # replace with the appropriate catalog name
    layout = LayoutApp(0)
    layout.MainLoop()