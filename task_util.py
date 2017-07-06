#!/bin/python
# -*- coding: utf-8 -*-

# for mutex lock, timer
import threading

# for storage
import Queue

import sys
from time import ctime,sleep

#
# Note:
#      Each task has associate a timer when the task thread run error for some reason, the ui will not receive any message
#

#
# The done flag maybe have multi-threading safe problem, use mutex lock for safe
#
class TaskWrapper(object):
    
    def __init__(self,task):
        '''
        task is a dict.
        keys:
            'run'            *
            'args'           *
            'timeout'        
            'callback_timeout'
            'callback_args'
        '''
        #
        # timer also use thread implementation
        #
        if task.has_key('timeout'):
            self.timer = threading.Timer(task['timeout'],self.timer_expired)
        else:
            self.timer = threading.Timer(5,self.timer_expired)
        self.task = task
        self.mutex = threading.Lock()
        self.done = False
 
    def run(self):
        '''
        execute task
        '''
        self.timer.start()
        self.task['run'](self.task['args'])
        
        #
        # task complete
        #
        self.timer.cancel()
        
        self.mutex.acquire()
        self.done = True
        self.mutex.release()
        
    def timer_expired(self):
        '''
        task execute timeout
        so it's result isnot reliable.
        if callback_timeout give. call it, else do nothing.
        '''
        self.mutex.acquire()
        if self.done == False:
            self.mutex.release()
            self.timer.cancel()
            if self.task.has_key('callback_timeout') == False or \
               self.task.has_key('callback_args') == False:
               return
            if self.task['callback_timeout']!=None:
                self.task['callback_timeout'](self.task['callback_args'])
            return
        self.mutex.release()
#
# task proxy for ui purpose
# submit task is the most important method
#
class TaskProxy(object):
    '''
    singleton class
    '''
    instance = None
    mutex = threading.Lock()
    
    def __init__(self):
        self.taskq = Queue.Queue(maxsize=10)
        self.thread = threading.Thread(target=self.run_queue,args=())
        self.thread.setDaemon(True)
        self.quit = False
        
    def start_proxy(self):
        '''
        start proxy task schedule
        '''
        self.thread.start()
        
    def submit_task(self,task):
        '''
        submit task for run
        '''
        self.taskq.put(task)
        
    def quitrun(self):
        '''
        exit task schedule
        '''
        self.quit = True

    def run_task(self,*arg,**kwargs):
        '''
        create a thread to run a task
        arg[0] is a TaskWrapper
        '''
        tw = arg[0]
        tw.run()
        
    def run_queue(self,*arg,**kwargs):
        '''
        task schedule main loop
        '''
        task = None
        while True:
            if self.quit:
                break
            try:
                task = self.taskq.get(block=True,timeout=1)
            except  Exception,e:
                #print sys.exc_info()
                task = None
            #
            # assign a new thread to run the task
            #
            if task == None:
                continue
            tw = TaskWrapper(task)
            t = threading.Thread(target=self.run_task,args=(tw,))
            t.setDaemon(True)
            t.start()
            #loop next task
        # clean 
        del self.taskq
        
    @staticmethod
    def GetInstance():
        '''
        use two step check method for the instance create
        '''
        if TaskProxy.instance == None:
            TaskProxy.mutex.acquire()
            if TaskProxy.instance == None:
                TaskProxy.instance = TaskProxy()
            TaskProxy.mutex.release()
        return TaskProxy.instance

def task1(*args,**kwargs):
    print 'task1'
if __name__=='__main__':
    proxy = TaskProxy.GetInstance()
    proxy.start_proxy()
    task = {'run':task1,'args':()}
    proxy.submit_task(task)
    sleep(10)
    proxy.quitrun()

    