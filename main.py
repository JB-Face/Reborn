'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:30:34
LastEditors: JBFace
LastEditTime: 2023-11-13 21:48:12
'''
try:
    import git
    import PySide6
except  ImportError:
    import pip
    
    pip.main(["install", "--user", 
    "GitPython",
        "pillow",
    "PySide6"
    
    ])
    import git
    import PySide6
import gitcore
import os
from context import Context

Context.draw()







