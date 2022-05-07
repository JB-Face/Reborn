'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:30:34
LastEditors: JBFace
LastEditTime: 2022-05-07 00:34:20
'''
try:
    import git
except  ImportError:
    import pip
    pip.main(["install", "--user", 
    "GitPython",
        "pillow",
    "colorama",
    "rich",
    
    ])
    import git
import gitcore
import os



path = r'C:\x20\Reborn\test'
url = 'https://github.com/JB-Face/javascript30day.git'
#gitcore.git_init(path,url)
a = gitcore.init_repo(path,url)
gitcore.get_git(a)
gitcore.git_checkout(a)

