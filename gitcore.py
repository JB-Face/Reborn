'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:15
LastEditors: JBFace
LastEditTime: 2022-06-11 17:25:17
'''
from git.repo import Repo
import os
from PySide2.QtCore import Qt 
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import time
import _thread
import threading
PRO =None
thread_1 = None





class Worker(QThread):

    progressBarValue = Signal(int)  # 更新进度条

    def __init__(self,add = 0,pro = None):
        super(Worker, self).__init__()
        self.add = add
        self.pro = pro


    def run(self):
        self._isRunning = True
        for i in range(100):
            time.sleep(0.01)
            self.progressBarValue.emit(i)


    def stop(self):
        self._isRunning = False
        self.progressBarValue.emit(0)

        

     

def git_init(path:str,url:str):
    print('----------------------------居然没有 初始化，等我初始化----------------------------------')
    return (Repo.clone_from(url=url, to_path=path))
    
def get_active(repo):
    return repo.head.object.hexsha


def copy_file(i):
    PRO.setValue(i)

def get_git(repo,branch,max = 50,pro = None,callback = None,int = False,context = None,path = None,url = None,):

    if pro :
        global PRO
        PRO = pro
        pro.setMaximum(0)        
        context.thread_1 = Worker(add=1,pro=pro)
        context.thread_1.progressBarValue.connect(copy_file)
        context.thread_1.start()

    if int and path:
        
        _thread.start_new_thread( internetupdata, (path,pro,context,callback ) )



    branch = 'origin/' + branch
    print('upodata ' + str(repo))
    fifty_first_commits = list(repo.iter_commits(branch  , max_count=max))



    # commit_log = repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}', max_count=50,
    #                         date='format:%Y-%m-%d %H:%M')
    # log_list = commit_log.split("\n")
    # real_log_list = [eval(item) for item in log_list]
    return fifty_first_commits

def internetupdata(path,pro,context,callback = None):
    _repo = init_repo(path,'')
    _repo.remotes.origin.fetch()
    if pro:
        context.thread_1.stop()
        PRO.setMaximum(99) 
        print('over') 
    if callback:
        callback()
        #PRO.setValue(0)



def print_time( threadName, delay,pro):
    count = 0
    for i in range(100):
        time.sleep(0.01)
        pro.setValue(i)

def fetch(a):
    time.sleep(1)
    print(10000000)
    time.sleep(1)
    print(10000000)
    print(a)

def git_checkout_commit(repo,commit):

    
    c = repo.commit(commit)
    repo.head.reference = c
    repo.index.checkout(force=True,)


    #repo.index.checkout(commit,force=True)

def git_reset_head(repo):
    repo.head.reset(index=True, working_tree=True)

def clean_local(repo):
    repo.index.checkout(force=True,)

def get_commit_by_index(repo,index):
    _list = get_git(repo)
    if index >= _list.__len__():
        index = -1
    return _list[index]


def is_git(path:str):
    gitpath  = os.path.join(path,'.git')
    return os.path.exists(gitpath)

def init_repo(path:str,url:str):
    if is_git(path):
        
        return Repo(path)
    else:
        return git_init(path,url)

def update(repo,commit = None):
    git_checkout(repo)
    if commit == None:
        repo.git.pull()

    pass

