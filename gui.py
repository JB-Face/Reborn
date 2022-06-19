
from PySide2 import QtCore, QtWidgets,QtGui
from PIL import Image, ImageTk
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import time
import webbrowser
import os
import sys
from git.repo import Repo
import _thread
class Worker(QThread):

    progressBarValue = Signal(int)  # 更新进度条

    def __init__(self):
        super(Worker, self).__init__()


    def run(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号



def repo(gitlab,boo):
    res = Repo.clone_from(url=gitlab.url, to_path=gitlab.path)
    boo = False

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
        self.context= context

        self.guidict = {}

        # workspace tab init
        for i in context.workspacelist:
            self.guidict[i.name] = {}
            _tab  = self.tab(i,self.main_widget,self.guidict[i.name])
            self.tabwidget.addTab(_tab,i.name)
            self.tabwidget.setTabEnabled(self.tabwidget.count()-1,False)
        
        


        # setting
        self.tabwidget.currentChanged.connect(self.tabwidget_update)
 


        self.progressBar = QtWidgets.QProgressBar(textVisible=False,)

        # self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 50))
        # 创建并启用子线程
        # self.thread_1 = Worker()
        # self.thread_1.progressBarValue.connect(self.copy_file)
        # self.thread_1.start()
        self.main_layout.addWidget(self.progressBar)
        self.textbox = QLineEdit(self)
        self.textbox.setEnabled(False)
        self.main_layout.addWidget(self.textbox)

        self.setCentralWidget(self.main_widget)
        self.tabwidget_update(0,True)


    def copy_file(self, i):
        self.progressBar.setValue(i)





    def tabwidget_update(self,active,int = True):
        # 初始化相关
        for i in range(self.tabwidget.count()):
            if i != active:
                self.tabwidget.setTabEnabled(i,False)

        if self.context.thread_1:
            if self.context.thread_1._isRunning:
                return 
        activetab =self.guidict[list(self.guidict)[active]]


        self.update_list(gitlab =activetab['gitlab'] ,guidict = activetab,int = int,pro = self.progressBar)



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
        self.context.addlog('更新到' + str(commit))

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
        radioButton = QtWidgets.QCheckBox('run' )  
        guidict['run'] = radioButton
        buttonlayout.addWidget(radioButton) 
        _updata = QtWidgets.QPushButton('updata')
        _updata.clicked.connect(lambda :self.update_list(gitlab,guidict,pro = self.progressBar,int = True))
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
        # self.tableWidget.horizontalHeader().setVisible(False)#垂直方向的表头
        tableWidget.resizeColumnsToContents()
        guidict['tableWidget'] = tableWidget

        tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单，如果不设为CustomContextMenu,无法使用customContextMenuRequested
        tableWidget.customContextMenuRequested.connect(lambda: self.showContextMenu(gitlab,guidict))


        #self.update_list(gitlab,guidict,int = False)
        guidict['gitlab'] = gitlab



        

        res.setLayout(main)

        
        return res


    def update_list(self,gitlab,guidict,int = False,pro = None):
        # 是否需要 初始化
        self.context.addlog('刷新中...')
        if int:
            if gitlab.repo:
                gitlist = gitlab.get_commit_list(int,pro = pro,guidict = guidict,callback =lambda:self.reflistgui(gitlab,guidict))
            else:
                self.context.addlog('初始化库...')
                if gitlab.init_repo_clone(pro = pro,callback =lambda:self.reflistgui(gitlab,guidict)):
                    pass
               
        else:
            if gitlab.repo:
                self.reflistgui(gitlab,guidict)

    def reflistgui(self,gitlab,guidict):
        tableWidget = guidict['tableWidget']
        main = guidict['main']    
        gitlist = gitlab.get_commit_list(False,pro = None,guidict = guidict)

        tableWidget.setRowCount(gitlist.__len__())
        tableWidget.setColumnCount(4)
        tableWidget.setHorizontalHeaderLabels(['commitid','time','auther','des'])

        main.addWidget(tableWidget)

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
        for i in range(self.tabwidget.count()):
                self.tabwidget.setTabEnabled(i,True)


        self.context.addlog('完成刷新')

    def openurl(self,gitlab):
        
        webbrowser.open(gitlab.url)

    def openpath(self,gitlab):
        os.system('start explorer '+ os.path.abspath(gitlab.path))

    def update_all_lab(self):
        for i in self.guidict:
            self.update(i['gitlab'],i,int = True)

    def update_log(self):
        self.textbox.setText(str(self.context.log[-1]))



class init_ui(QWidget):

    def __init__(self):
        super(init_ui, self).__init__()

    def setupUi(self):
        self.setFixedSize(500, 90)
        self.main_widget = QtWidgets.QWidget(self)
        self.progressBar = QtWidgets.QProgressBar(self.main_widget)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 50))
        # 创建并启用子线程
        self.thread_1 = Worker2()
        self.thread_1.progressBarValue.connect(self.copy_file)
        self.thread_1.start()

    def copy_file(self, i):
        self.progressBar.setValue(i)


class Worker2(QThread):

    progressBarValue = Signal(int)  # 更新进度条

    def __init__(self):
        super(Worker2, self).__init__()


    def run(self):
        for i in range(101):
            time.sleep(0.01)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号


# class init_gui():
#     def __init__(self,text,):
#         self.text = text
#         app = QtWidgets.QApplication()
#         self.testIns =init_ui()
#         self.testIns.setupUi()
#         self.testIns.show()





    
