'''
Descripttion: 
version: 
Author: JBFace
Date: 2022-05-06 22:51:15
LastEditors: JBFace
LastEditTime: 2022-05-11 01:20:05
'''
from git.repo import Repo
import os
def git_init(path:str,url:str):
    print('----------------------------居然没有 初始化，等我初始化----------------------------------')
    return (Repo.clone_from(url=url, to_path=path))
    
def get_active(repo):
    return repo.head.object.hexsha

    
def get_git(repo,branch,max = 50):
    
    #a = repo.remotes.origin.fetch()
    branch = 'origin/' + branch
    print('----------------------------网络链接 更新ing----------------------------------')
    fifty_first_commits = list(repo.iter_commits(branch  , max_count=max))


    # commit_log = repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}', max_count=50,
    #                         date='format:%Y-%m-%d %H:%M')
    # log_list = commit_log.split("\n")
    # real_log_list = [eval(item) for item in log_list]
    return fifty_first_commits


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