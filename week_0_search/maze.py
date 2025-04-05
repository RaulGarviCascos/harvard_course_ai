from collections import deque
import sys
class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = deque()

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self,state):
        return any(state == node.state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty(): 
            raise Exception("Empty frontier")
        return self.frontier.pop()
    
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty(): 
            raise Exception("Empty frontier")
        return self.frontier.popleft()

    