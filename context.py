'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:42
LastEditors: JBFace
LastEditTime: 2022-05-11 01:31:30
'''

import gitcore
import json
import os
import sys
from PySide2 import QtCore, QtWidgets,QtGui
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from PySide2.QtCore import Qt 

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
        
        # workspace tab
        for i in context.workspacelist:
            self.guidict[i.name] = {}
            _tab  = self.tab(i,self.main_widget,self.guidict[i.name])
            self.tabwidget.addTab(_tab,i.name)

        # setting


        self.setCentralWidget(self.main_widget)

    def tab(self,gitlab,parent,guidict):
        res=QtWidgets.QWidget()

        main =  QtWidgets.QVBoxLayout()

        hand_layout = QtWidgets.QHBoxLayout()
        guidict['main'] = main


        pixmap = QtGui.QPixmap(r'C:\\Users\\57376\\Pictures\\redbull.png')
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
        buttonlayout.addWidget(radioButton) 
        _updata = QtWidgets.QPushButton('updata')
        _updata.clicked.connect(lambda :self.update_list(gitlab,guidict))
        buttonlayout.addWidget(_updata)
        _path = QtWidgets.QPushButton('path')
        buttonlayout.addWidget(_path)
        _url = QtWidgets.QPushButton('url')
        buttonlayout.addWidget(_url)
        _start = QtWidgets.QPushButton('start')
        buttonlayout.addWidget(_start) 



        msmlayout.addItem(buttonlayout)          

        main.addItem(hand_layout )
### list

        


        tableWidget = QtWidgets.QTableWidget()
        
        tableWidget.setShowGrid(False)
        tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tableWidget.verticalHeader().setVisible(False)#水平方向的表头
        # self.tableWidget.horizontalHeader().setVisible(False)#垂直方向的表头
        tableWidget.resizeColumnsToContents()
        guidict['tableWidget'] = tableWidget
        self.update_list(gitlab,guidict)


        

        res.setLayout(main)

        
        return res


    def update_list(self,gitlab,guidict):
        tableWidget = guidict['tableWidget']
        main = guidict['main']

        gitlist = gitlab.get_commit_list()
        tableWidget.setRowCount(gitlist.__len__())
        tableWidget.setColumnCount(4)
        tableWidget.setHorizontalHeaderLabels(['commitid','time','auther','des'])

        main.addWidget(tableWidget)



                #将第一列的单元格宽度设置为150
        #tableWidget.setColumnWidth(0,)
        sha = gitlab.get_active()
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


    def callback(self,gitdict):
        pass


class context:
    def __init__(self) -> None:
        self.workspacelist = []
        self.getsetting()

        pass

    def getsetting(self):
        _path = r'setting'
        for root, dirs, files in os.walk(_path):
            for i in files:
                if '.json' in i:
                    with open(os.path.join(root,i),'r') as load_f:
                        j = json.load(load_f)
                        try:
                            a = gitlib(url = j["url"],path = j["path"],branch = j['branch'],callback=j['callback'],workspace=j["workspace"])
                            self.workspacelist.append(a)
                        except KeyError:
                            pass


                    
        pass

    def fillworkspace(self):
        pass


    def draw(self):
        app = QtWidgets.QApplication(sys.argv)
        gui = ButtonApp(self)
        gui.show()
        sys.exit(app.exec_())




    def test(self):
        self.workspacelist[0].get_commit_list()



        
        

class gitlib:
    def __init__(self,url = 'https://github.com/JB-Face/javascript30day.git'
                    ,path =  r'C:\x20\Reborn\test',branch = 'master',callback = None,workspace = 'test1') -> None:
        self.url = url
        self.path = path
        self.name = workspace     
        self.branch = branch
        self.callback = callback
        self.workspace = workspace

        

        self.repo = gitcore.init_repo(path,url)
        self.list = gitcore.get_git(self.repo,self.branch)
        

    def updata(self,commit):
        gitcore.git_checkout_commit(self.repo,commit)


    def get_commit_list(self):
        return gitcore.get_git(self.repo,self.branch)

    def get_active(self):
        return gitcore.get_active(self.repo)



Context = context()


