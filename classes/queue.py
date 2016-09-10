from functions import logger, config
import asyncio

class Queue:
    def __init__(self):
        ''' Create a new queue '''
        self.list = []
        self.maxSize = 50
    def full(self):
        ''' Returns true is the queue is full. False if the queue is not full'''
        return (len(self.list)>=self.maxSize)

    async def add(self,object):
        ''' Adds an object to the queue and returns the place in queue
        Returns False if the queue is full'''
        if object is None:
            raise ValueError("The object can't be None")
        if(len(self.list)<self.maxSize):
            self.list.append(object)
            return len(self.list)
        else:
            return False
    def size(self):
        ''' Returns the size of the queue '''
        return len(self.list)

    def empty(self):
        ''' Returns true if the queue is empty. False is not empty'''
        return (len(self.list)==0)
        
    async def remove(self,pos):
        ''' Removes the object in place `pos` from queue '''
        pos = int(pos)-1
        if(len(self.list)>pos):
            self.list.pop(pos)
            return True
        return False

    async def next(self):
        ''' Returns the next object from queue and removes it from queue 
        Returns none if the queue is empty'''
        if(len(self.list)>0):
            object = self.list[0]
            self.list.pop(0)
            return object
        else:
            return None

    async def getNext(self):
        ''' Returns the next object from queue without removing it.
       Returns none is the queue is empty '''
        if(len(self.list)>0):
            return self.list[0]
        else:
            return None

    async def getQueue(self):
        ''' Returns an array of the whole queue '''
        return self.list