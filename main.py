'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:30:34
LastEditors: JBFace
LastEditTime: 2022-05-11 23:30:05
'''
try:
    import git
    import PySide2
except  ImportError:
    import pip
    
    pip.main(["install", "--user", 
    "GitPython",
        "pillow",
    "PySide2"
    
    ])
    import git
    import PySide2
import gitcore
import os
from context import Context

Context.draw()







