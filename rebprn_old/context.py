'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:42
LastEditors: JBFace
LastEditTime: 2022-10-01 17:04:27
'''

import gitcore
import json
import os
import sys
import webbrowser
from git.repo import Repo
from PySide2 import QtCore, QtWidgets,QtGui
from PySide2.QtCore import Qt 
import time
import gui
class context:
    def __init__(self) -> None:
        self.workspacelist = []
        self.thread_1 = None
        self.getsetting()
        self.progressBar = None 
        self.gui = None

        self.log = []

        pass

    def getsetting(self):
        _path = r'setting'
        for root, dirs, files in os.walk(_path):
            for i in files:
                if '.json' in i:
                    with open(os.path.join(root,i),'r') as load_f:
                        j = json.load(load_f)
                        try:
                            icon = os.path.join(root,i).replace('json','png')
                            a = gitlib(url = j["url"],path = j["path"],branch = j['branch'],callback=j['callback'],workspace=j["workspace"],icon = icon)
                            self.workspacelist.append(a)
                        except KeyError:
                            pass




    def draw(self):
        app = QtWidgets.QApplication(sys.argv)
        self.gui = gui.ButtonApp(self)
        self.gui.show()
        sys.exit(app.exec_())




    def test(self):
        self.workspacelist[0].get_commit_list()



    def addlog(self,text):
        text = "[" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) +"]:" + text
        self.log.append(text)
        if self.gui:
            self.gui.update_log()





        
        

class gitlib:
    def __init__(self,url = 'https://github.com/JB-Face/javascript30day.git'
                    ,path =  r'C:\x20\Reborn\test',branch = 'master',callback = None,workspace = 'test1',icon = None) -> None:
        self.url = url
        self.path = path
        self.name = workspace     
        self.branch = branch
        self.callback = callback
        self.workspace = workspace
        self.icon = icon       

        self.repo = gitcore.init_repo(path,url)
        if self.repo:
            self.list = gitcore.get_git(self.repo,self.branch,int = False)
        

    def updata(self,commit):
        gitcore.git_checkout_commit(self.repo,commit)


    def get_commit_list(self,int = False,pro = None, guidict = None,callback = None):
        return gitcore.get_git(self.repo,self.branch,int = int,pro = pro,context = Context,path = self.path,url = self.url,callback = callback)

    def get_active(self):
        return gitcore.get_active(self.repo)

    def init_repo_clone(self,pro = None,callback = None):
        try:
            gitcore.git_clone(self,pro = pro,callback=callback,context = Context)
        except:
            return False

        return True




Context = context()


