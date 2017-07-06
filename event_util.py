#!/bin/python
# -*- coding: utf-8 -*-

#
# this module is used for custom event
#

import wx

# ------------------------------------- #
# Custom EventType
# ------------------------------------- #
wxNotifyEvent = wx.NewEventType()

# ------------------------------------- #
# Custom Python Event Binder
# ------------------------------------- #
EVT_NOTIFY_EVENT = wx.PyEventBinder(wxNotifyEvent,1)

# 
# ------------------------------------- #
# Class NotifyEvent
# ------------------------------------- #
class NotifyEvent(wx.PyCommandEvent):
    '''
    custom notify event
    data: save some private info
    '''
    def __init__(self, evtType, id = -1):
        wx.PyCommandEvent.__init__(self,evtType,id)
        self.data = None
        #self._eventType = evtType
    def SetData(self,data=None):
        if data!=None:
            self.data = data
    def GetData(self):
        return self.data
# ------------------------------------- #
# Custom event example 
# ------------------------------------- #
#
# evt = NotifyEvent(wxNotifyEvent,xxx.GetId())
# Bind(EVT_NOTIFY_EVENT,handle_function)

if __name__=='__main__':
    evt = NotifyEvent(wxNotifyEvent,-1)
    print evt.GetEventType()
    print evt.GetId()
    print evt.GetEventObject()



    


