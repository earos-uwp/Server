"""
__Author__: Nate Braukhoff and Evan Majerus

__Purpose__:
"""
import pandas as pd
import numpy as np
import itertools


class Node:
    def __init__(self, name):
        """
        Create a Node with a name and an option of having a list of children and a grade. If the node has no children
        then _children will be set to none.
        :param name: string
        """

        self._name = name
        self._children = []
        self._state = ''
        self._parents = []

    def get_name(self):
        """
        get_name will return the Node's attribute _name as a string
        :return: string
        """
        return str(self._name)

    def get_children(self):
        """
        get_children will return a list of all of the Nodes children
        :return: list of Nodes
        """
        return self._children

    def get_state(self):
        return self._state

    def set_grade(self, grade):
        self._state = grade

    def get_parents(self):
        return self._parents

    def get_child(self, name_of_child):
        """
        get_child will iterate through the list of children and return the desired child. If a child is not found the
        method will return None. This method will also return None if _children is None
        :param name_of_child: The name of a child (Type: String)
        :return: Node or None
        """
        if len(self._children) != 0:
            for child in self._children:
                if name_of_child == child.get_name():
                    return child
        return None

    def get_parent(self, name_of_parent):
        """
        get_parent searches through the list of parents and returns the parent the user is looking for. If the parent
        does not exist in the list then the method will return None.
        :param name_of_parent: String
        :return: parent of None
        """
        for parent in self._parents:
            if parent.get_name() == name_of_parent:
                return parent
        return None

    def get_parent_names(self):
        names = []
        for parent in self._parents:
            names.append(parent.get_name())
        return names

    def add_child(self, child):
        """
        add_child will add a child to the end of _children. If _children is None then a new list will be created with
        the child in it.
        :param child: child node
        """
        if self._children is None:
            self._children = [child]
        else:
            self._children.append(child)

    def add_parent(self, parent):
        """
        add_parent will add the parent to the end of the parent list if the parents doesn't already exists in _parents.
        :param parent: Node
        """
        self._parents.append(parent)

    def remove_child(self, name_of_child):
        """
        remove_child will remove the node from the node's children's list
        :param name_of_child: String
        """
        for child in self._children:
            if child.get_name() == name_of_child:
                self._children.remove(child)

