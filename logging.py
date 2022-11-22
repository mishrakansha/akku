# --* logging module*--
from py_console import console

def save(user, word, time, timeBoolean=True, userBoolean=True, wordBoolean=True):
    try:
        fd_log = open('./logs.txt', 'w+')
        if(timeBoolean):
            fd_log.write(time+' ')
        if(userBoolean): # and timeBoolean and wordBoolean):
            fd_log.write(user+' ')
        if(wordBoolean):
            fd_log.write(word+'\n')
        fd_log.close()
    except Exception as e:
        print('[!] File stream error {./log.txt}: ', e)        

