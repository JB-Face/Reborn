'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-16 23:04:19
LastEditors: JBFace
LastEditTime: 2022-05-17 00:02:58
'''
import sys
import time
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class test(QWidget):

    def __init__(self):
        super(test, self).__init__()

    def setupUi(self):
        self.setFixedSize(500, 90)
        self.main_widget = QtWidgets.QWidget(self)
        self.progressBar = QtWidgets.QProgressBar(self.main_widget)
        self.progressBar.setGeometry(QtCore.QRect(20, 20, 450, 50))
        # 创建并启用子线程
        self.thread_1 = Worker()
        self.thread_1.progressBarValue.connect(self.copy_file)
        self.thread_1.start()

    def copy_file(self, i):
        self.progressBar.setValue(i)


class Worker(QThread):

    progressBarValue = Signal(int)  # 更新进度条

    def __init__(self):
        super(Worker, self).__init__()


    def run(self):
        for i in range(101):
            time.sleep(0.01)
            self.progressBarValue.emit(i)  # 发送进度条的值 信号


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    testIns = test()
    testIns.setupUi()
    testIns.show()
    sys.exit(app.exec_())