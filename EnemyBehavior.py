#Create 3 dufferent types of Nodes: Tasks, Composites, Decorators
#Enemy Object needs to be able to access Nodes, and functions in the nodes
#Create a Behavior Tree that interacts with the Enemy Object directly and uses the Nodes to use the obejct's functions
import pygame, enemy,player,random,UI
from enemy import Enemy
from player import Player

class Behavioral_Node:

    def __init__(self,right = None, left = None):
        self.parent = None
        self.right_child = right
        self.left_child = left
        self.right_sibling = None

class Task_Node(Behavioral_Node):

    def __init__(self,object= None, right = None, left = None,right_sibling = None,):
        super().__init__(right,left)
        self.Object = object
        self.condition = None
        self.function = None
        self.right_sibling = right_sibling
    
    def set_task_node(self,condition,function):
        self.condition = condition
        self.function = function

    def run_node(self):
        if self.condition:
            if self.Object == None:
                self.function()
            else:
                self.function(self.Object)
            if self.right_sibling != None:
                self.right_sibling.run_node()
            return True
        else:
            return False

    
    def set_sibling(self, node):
        self.right_sibling = node
        

class Selector_Node(Behavioral_Node):

    def __init__(self,right = None,left = None):
        super().__init__(right,left)
    
    def run_node(self):
        if  self.left_child.run_node() and (self.right_child == None or isinstance(self.right_child,Decorator_Node)):
            return True
        if self.left_child.run_node():
            if self.right_child.run_node() and not isinstance(self.right_child,Decorator_Node):
                return True
            else:
                return False
        else:
            if isinstance(self.right_child,Decorator_Node):
                self.right_child.run_node()
                return True
        return False
    
    def set_right_child(self,node):
        self.right_child = node
    
    def set_left_child(self, node):
        self.left_child = node

class Decorator_Node(Selector_Node):
    def __init__(self,right = None, left = None):
        super().__init__(right,left)

class Behavioral_Tree:
    
    def __init__(self,enemy,object = None):
        self.root = Selector_Node()
        self.task = Task_Node(object)
        self.task.set_task_node(enemy.in_aoe_range(object),enemy.chase_player_sprinting)
        self.root.set_left_child(self.task)
        self.stop_command = Decorator_Node()
        self.stop_task = Task_Node(object)
        self.stop_task.set_task_node(True,enemy.chase_player)
        self.stop_command.set_left_child(self.stop_task)
        self.root.set_right_child(self.stop_command)

    def print_hello(self,text):
        print(text)
    
    def condition(self, bool):
        return bool

    def run_tree(self):
       self.root.run_node()
           