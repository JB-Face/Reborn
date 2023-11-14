'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:42
LastEditors: JBFace
LastEditTime: 2023-11-14 19:44:54
'''

import gitcore
import json
import os
import sys
import time
import webbrowser
from PySide6 import QtCore, QtWidgets,QtGui
from PySide6.QtCore import Qt ,QThread
import _thread
import threading


class Listener(threading.Thread):
    def __init__(self, context,callback):
        threading.Thread.__init__(self)
        self.context = context
        self.callback = callback
    def run(self):
        while 1:
            time.sleep(1)
            for i in self.context.workspacelist:
                self.get_info(i)
            if self.context.init_title <1 : self.context.init_title = 1
            self.callback()

    def get_info(slef,gitlib):
        gitlib.repo = gitcore.init_repo(gitlib.path,gitlib.url)
        gitlib.list = gitcore.get_git(gitlib.repo,gitlib.branch)    



class Update_Thread(QtCore.QThread):

    finishSignal = QtCore.Signal(list)
    def __init__(self, context,parent=None):
        super(Update_Thread, self).__init__(parent)
        self.context = context
    def run(self):
        while 1  :
            for i in self.context.workspacelist:
                self.get_info(i)
            if self.context.init_title <1 : self.context.init_title = 1
            self.finishSignal.emit(['hello,','world','!'])
            time.sleep(1)
    def get_info(self,gitlib):
        gitlib.repo = gitcore.init_repo(gitlib.path,gitlib.url)
        gitlib.list = gitcore.get_git(gitlib.repo,gitlib.branch)
        gitlib.get_commit_list()    


class ButtonApp(QtWidgets.QMainWindow):
    def __init__(self,context):
        super().__init__()
        self.setWindowTitle("Reborn")
        self.setFixedSize(1000,800) # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.tabwidget = QtWidgets.QTabWidget()
        self.main_layout.addWidget(self.tabwidget)
        self.guidict = {}        
        self.setCentralWidget(self.main_widget)
        self.context = context 


        self.update_Thread = Update_Thread(self.context)
        #连接子进程的信号和槽函数
        self.update_Thread.finishSignal.connect(self.update)
        #开始执行 run() 函数里的内容
        self.update_Thread.start()

        pass

        #self.update_title()
        #self.update_list()
    def update(self,ls):
        if self.context.init_title == 1:
            self.update_title()
        self.update_all_list()


    def callback(self,gitlab):
        if gitlab.callback:
            callbackpath =os.path.join(gitlab.path,gitlab.callback)

            os.startfile(callbackpath)
        pass

    def actionHandler(self,guidict,gitlab):
        widget = guidict['tableWidget']
        commit = widget.currentRow()
        commit  = widget.item(commit,0).text()
        gitlab.updata(commit)
        self.update_list(gitlab,guidict)

        if guidict['run'].isChecked():
            self.callback(gitlab)



    def showContextMenu(self, gitlab,guidict):  # 创建右键菜单


        contextMenu = QtWidgets.QMenu(self)
        actionA = contextMenu.addAction(u'更新')
        actionA.triggered.connect(lambda: self.actionHandler(guidict,gitlab))
        # self.actionA = self.view.contextMenu.exec_(self.mapToGlobal(pos))  # 1
        contextMenu.popup(QtGui.QCursor.pos())  # 2菜单显示的位置

        # self.view.contextMenu.move(self.pos() + pos)  # 3
        contextMenu.show()

    def tab(self,gitlab,parent,guidict):
        res=QtWidgets.QWidget()

        main =  QtWidgets.QVBoxLayout()

        hand_layout = QtWidgets.QHBoxLayout()
        guidict['main'] = main


        pixmap = QtGui.QPixmap(gitlab.icon)
        icon= QtWidgets.QLabel()
        icon.setPixmap(pixmap)
        icon.setMaximumSize(125,125)
        hand_layout.addWidget(icon, 0 , Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        msmlayout = QtWidgets.QVBoxLayout()
        # msmlayout.SetMinimumSize(300,100)

        
        _path = QtWidgets.QLabel(text = str('路径：')+str(gitlab.path))
        msmlayout.addWidget(_path, 0 , Qt.AlignLeft|QtCore.Qt.AlignTop)
        _url = QtWidgets.QLabel(text = str('网址：')+str(gitlab.url))
        msmlayout.addWidget(_url, 0 , Qt.AlignLeft|QtCore.Qt.AlignTop)
        _name = QtWidgets.QLabel(text = str('项目名：')+str(gitlab.name))
        msmlayout.addWidget(_name, 0 , Qt.AlignLeft|QtCore.Qt.AlignTop)


        hand_layout.addItem(msmlayout)



        buttonlayout = QtWidgets.QHBoxLayout()
        radioButton = QtWidgets.QRadioButton('run' )  
        guidict['run'] = radioButton
        buttonlayout.addWidget(radioButton) 
        _updata = QtWidgets.QPushButton('updata')
        _updata.clicked.connect(lambda :self.update_list(gitlab,guidict))
        buttonlayout.addWidget(_updata)
        _path = QtWidgets.QPushButton('path')
        buttonlayout.addWidget(_path)
        _path.clicked.connect(lambda :self.openpath(gitlab))
        _url = QtWidgets.QPushButton('url')
        buttonlayout.addWidget(_url)
        _url.clicked.connect(lambda :self.openurl(gitlab))
        _start = QtWidgets.QPushButton('start')
        buttonlayout.addWidget(_start) 
        _start.clicked.connect(lambda :self.callback(gitlab))



        msmlayout.addItem(buttonlayout)          

        main.addItem(hand_layout )
### list

        


        tableWidget = QtWidgets.QTableWidget()
        
        tableWidget.setShowGrid(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tableWidget.verticalHeader().setVisible(False)#水平方向的表头
        tableWidget.resizeColumnsToContents()
        guidict['tableWidget'] = tableWidget

        tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        tableWidget.customContextMenuRequested.connect(lambda: self.showContextMenu(gitlab,guidict))


       #self.update_list(gitlab,guidict)       

        res.setLayout(main)

        
        return res
    

    def update_title(self):
        for i in self.context.workspacelist:
            if i and self.context.init_title:
                self.guidict[i.name] = {}
                _tab  = self.tab(i,self.main_widget,self.guidict[i.name])
                self.tabwidget.addTab(_tab,i.name)
                self.context.init_title = 2
        


    def update_list(self,gitlib,guidict):
        tableWidget = guidict['tableWidget']
        main = guidict['main']
        gitlist = gitlib.commit_list
        tableWidget.setRowCount(gitlist.__len__())
        tableWidget.setColumnCount(4)
        tableWidget.setHorizontalHeaderLabels(['commitid','time','auther','des'])
        main.addWidget(tableWidget)
                #将第一列的单元格宽度设置为150
        #tableWidget.setColumnWidth(0,)
        sha = gitlib.get_active()
        back = QtGui.QBrush(QtGui.QColor(255,0,0))

        for i,v in enumerate(gitlist):
            active = False
            if sha == v.hexsha:
                active = True
            newItem = QtWidgets.QTableWidgetItem(v.hexsha[:6])
            if active:
                newItem.setForeground(back)

            tableWidget.setItem(i, 0, newItem)

            timestr = v.committed_datetime
            timestr = str(timestr.month) + '-' + str(timestr.day) + ' ' +str(timestr.hour) + ':'+str(timestr.minute)

            newItem = QtWidgets.QTableWidgetItem(timestr )
            if active:
                newItem.setForeground(back)
            tableWidget.setItem(i, 1, newItem)

            newItem = QtWidgets.QTableWidgetItem(v.author.name)
            if active:
                newItem.setForeground(back)
            tableWidget.setItem(i, 2, newItem)

            newItem = QtWidgets.QTableWidgetItem(v.message)
            if active:
                newItem.setForeground(back)
            tableWidget.setItem(i, 3, newItem)
        pass

    def openurl(self,gitlab):
        
        webbrowser.open(gitlab.url)

    def openpath(self,gitlab):
        os.system('start explorer '+ os.path.abspath(gitlab.path))

    def update_all_list(self):        
        for i in self.context.workspacelist:
            if i and i.name in self.guidict:
                self.update_list(i,self.guidict[i.name])
        pass

class gitlib:
    def __init__(self,url = 'https://github.com/JB-Face/javascript30day.git'
                    ,path =  r'.\test',branch = 'master',callback = None,workspace = 'test1',icon = None) -> None:
        self.url = url
        self.path = path
        self.name = workspace     
        self.branch = branch
        self.callback = callback
        self.workspace = workspace
        self.icon = icon  
        self.commit_list =None      

        # self.repo = gitcore.init_repo(path,url)
        # self.list = gitcore.get_git(self.repo,self.branch)        

    def updata(self,commit):
        #_thread.start_new_thread(gitcore.git_checkout_commit,(self.repo,commit))
        gitcore.git_checkout_commit(self.repo,commit)

    def get_commit_list(self):
        self.commit_list = gitcore.get_git(self.repo,self.branch)
        return self.commit_list
    def get_active(self):
        return gitcore.get_active(self.repo)


class context:
    def __init__(self) -> None:
        self.v = 2.0 # 新的context 以支持多线程等功

        self.workspacelist = []
        self.active = None
        self.init_title = 0

        self.set_setting()

    def set_setting(self):
        '''
        获取基本设置，但是不初始化，也不进行操作
        '''
        _path = r'setting'
        for root, dirs, files in os.walk(_path):
            for i in files:
                if '.json' in i:
                    with open(os.path.join(root,i),'r') as load_f:
                        j = json.load(load_f)
                        try:
                            icon = os.path.join(root,i).replace('json','png')
                            lib = gitlib(url = j["url"],path = j["path"],branch = j['branch'],callback=j['callback'],workspace=j["workspace"],icon = icon)
                            self.workspacelist.append(lib)
                        except KeyError:
                            pass

    def draw(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.gui = ButtonApp(self)
        self.gui.show()
        sys.exit(self.app.exec_())

        pass

    def update_active(self):
        if self.active == None:
            self.active = self.workspacelist[0]

        # 更新对应的数据

        pass

#         self.a = None
#         self.gui = None
#         self.workspacelist = []
#         self.getsetting()

#         pass

#     def getsetting(self):
#         _path = r'setting'
#         for root, dirs, files in os.walk(_path):
#             for i in files:
#                 if '.json' in i:
#                     with open(os.path.join(root,i),'r') as load_f:
#                         j = json.load(load_f)
#                         try:
#                             icon = os.path.join(root,i).replace('json','png')
#                             # a = gitlib(url = j["url"],path = j["path"],branch = j['branch'],callback=j['callback'],workspace=j["workspace"],icon = icon)
#                             _thread.start_new_thread(self._gitlib,(j,icon,self.a))
#                             self.workspacelist.append(self.a)
#                         except KeyError:
#                             pass


                    
#         pass


#     def _gitlib(self,j,icon = None,cl = None,callback = None):
#         cl = gitlib(url = j["url"],path = j["path"],branch = j['branch'],callback=j['callback'],workspace=j["workspace"],icon = icon)
#         callback()



#     def fillworkspace(self):
#         pass

#     def draw(self):
#         app = QtWidgets.QApplication(sys.argv)
#         self.gui = ButtonApp(self)
#         self.gui.show()
#         sys.exit(app.exec_())


#     def test(self):
#         self.workspacelist[0].get_commit_list()        
        




Context = context()


