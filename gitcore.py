'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:15
LastEditors: JBFace
LastEditTime: 2022-05-07 00:48:35
'''
from git.repo import Repo
import os
def git_init(path:str,url:str):
    return (Repo.clone_from(url=url, to_path=path))
    

def get_git(repo):
    commit_log = repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}', max_count=50,
                            date='format:%Y-%m-%d %H:%M')
    log_list = commit_log.split("\n")
    real_log_list = [eval(item) for item in log_list]
    print(real_log_list)
    pass


def git_checkout(repo):
    repo.index.checkout(force=True,)
    repo.index.reset('d1e14f9')
    pass



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