'''
Created on 2011-11-22

@author: Jinghao
'''

class DexError(Exception):
    '''
    Dex Error class
    '''


    def __init__(self, message):
        Exception.__init__(self, message)