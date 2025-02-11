import itertools
from unittest import TestCase
from node import Node
from itertools import combinations
from itertools import combinations_with_replacement
import pandas as pd


class TestNode(TestCase):
    def test_get_name(self):
        a = Node('ClassA', None)
        self.assertEqual('ClassA', a.get_name())

    def test_get_children(self):
        a = Node('ClassA', [Node('B'), Node('C'), Node('D')])
        children = [Node('B'), Node('C'), Node('D')]

        self.assertTrue(children[0].get_name() == a.get_children()[0].get_name()
                        and children[1].get_name() == a.get_children()[1].get_name()
                        and children[2].get_name() == a.get_children()[2].get_name())

        self.assertTrue(3 == len(a.get_children()))

    def test_get_child(self):
        a = Node('ClassA', [Node('B'), Node('C'), Node('D')])
        b = Node('ClassB')

        self.assertTrue('B' == a.get_child('B').get_name())

        self.assertTrue(a.get_child('Z') is None)

        self.assertTrue(b.get_child('A') is None)

    def test_add_child(self):
        a = Node('ClassA', [Node('B'), Node('C'), Node('D')])
        b = Node('ClassB')

        a.add_child(Node('Z'))
        b.add_child(Node('Z'))

        self.assertTrue('Z' == a.get_children()[3].get_name())
        self.assertTrue(4 == len(a.get_children()))

        self.assertTrue('Z' == b.get_children()[0].get_name())
        self.assertTrue(1 == len(b.get_children()))

        b.add_child(Node('X'))

        self.assertTrue('X' == b.get_children()[1].get_name())
        self.assertTrue(2 == len(b.get_children()))

    def test_remove_child(self):
        a = Node('A')
        b = Node('B')
        c = Node('C')

        a.get_child(b)
        a.add_child(c)

        a.remove_child('B')

        self.assertTrue(1 == len(a.get_children()))
        self.assertTrue(c == a.get_children()[0])

    def test_add_parent(self):
        a = Node('A')
        b = Node('B')
        c = Node('C')

        a.add_parent(a)

        self.assertTrue(a == a.get_parents()[0])

