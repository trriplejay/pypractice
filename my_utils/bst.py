import unittest
import random
import copy

class node(object):

    def __init__(self, data=None, depth=0, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.depth = depth


class bst(object):
    """
    currently not a balanced bst implementation, so order of insertion
    matters
    """

    def __init__(self, data=None, arglist=None):
        if data is not None:
            self.root = node(data=data)
        else:
            self.root = None
        if arglist is not None:
            self.build_tree(arglist)

    def build_tree(self, arglist):
        # takes in a list of sortable values
        # builds a btree from the list
        if self.root is None:
            self.root = node(data=arglist.pop(0))
        for value in arglist:
            self.insert_sorted(value)

    def insert_sorted(self, val, curr=None):

        # base case: we are a child of "curr"
        if curr is None:
            curr = self.root

        if val >= curr.data and curr.right is None:
            curr.right = node(data=val, depth=curr.depth+1)
        elif val < curr.data and curr.left is None:
            curr.left = node(data=val, depth=curr.depth+1)
        else:
            if val < curr.data:
                self.insert_sorted(val, curr=curr.left)
            if val >= curr.data:
                self.insert_sorted(val, curr=curr.right)

    def find_node(self, val, curr=None, rep=True):
        if curr is None and rep is True:
            curr = self.root
        elif curr is None and rep is False:
            return False

        if curr.data == val:
            return True

        if val < curr.data:
            return self.find_node(val, curr=curr.left, rep=False)
        if val > curr.data:
            return self.find_node(val, curr=curr.right, rep=False)

    def get_size(self, curr=None):

        return len(list(self.return_in_order()))

    def print_in_order(self, curr=None, order=None):

        print '[',

        if order is None:
            for item in self.return_in_order():
                print str(item.data) + ",",

        elif order == 'pre':
            for item in self.return_pre_order():
                print str(item.data) + ",",
        elif order == 'post':
            for item in self.return_post_order():
                print str(item.data) + ",",
        else:
            print "bad order provided",


        print "]"

    def return_in_order(self, curr=None):
        """
        i dunno about this for-loop in recursive yield...
        it's the only way to use yield recursively in python 2.7, but
        i'm not sure if it will cause excessive traversal... maybe gets
        optimized under the hood...
        """
        if curr is None:
            curr = self.root
        if curr.left is not None:
            for my_node in self.return_in_order(curr=curr.left):
                yield my_node

        yield curr

        if curr.right is not None:
            for my_node in self.return_in_order(curr=curr.right):
                yield my_node

        """ NOTE:
        in python 3.3 or later, you can successfully yield in recursion
        by doing a "yield from... ", so it would look like this:

        if curr is None:
            curr = self.root
        if curr.left is not None:
            yield from self.return_in_order(curr=curr.left)

        yield str(curr.data)

        if curr.right is not None:
            yield from self.return_in_order(curr=curr.right)

        but this was written in python 2.7, so im changing the implementation
        """

    def return_pre_order(self, curr=None):

        if curr is None:
            curr = self.root

        yield curr

        if curr.left is not None:
            for value in self.return_in_order(curr=curr.left):
                yield value

        if curr.right is not None:
            for value in self.return_in_order(curr=curr.right):
                yield value

    def return_post_order(self, curr=None):

        if curr is None:
            curr = self.root

        if curr.left is not None:
            for value in self.return_in_order(curr=curr.left):
                yield value

        if curr.right is not None:
            for value in self.return_in_order(curr=curr.right):
                yield value

        yield curr

    def get_depth(self):
        # returns highest depth of the tree from pre-order travesal
        depth = 0
        for item in self.return_in_order():
            if item.depth > depth:
                depth = item.depth

        return depth


class TestBST(unittest.TestCase):

    def setUp(self):
        self.t1_args = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.t1 = bst(arglist=[1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.t2_args = [5, 2, 8, 3, 4, 9, 7, 1, 6]
        self.t2 = bst(arglist=[5, 2, 8, 3, 4, 9, 7, 1, 6])

    def test_auto_build(self):
        self.assertEqual(self.t1.root.data, self.t1_args[0])

        ordered_tree = list()
        for item in self.t1.return_in_order():
            ordered_tree.append(item.data)

        ordered_list = sorted(self.t1_args)

        self.assertEqual(ordered_list, ordered_tree)
        self.assertEqual(self.t1.get_size(), 9)

        ordered_tree = list()
        for item in self.t1.return_in_order():
            ordered_tree.append(item.data)
        temp_tree = bst(arglist=copy.deepcopy(ordered_tree))
        newlist = list()
        for item in temp_tree.return_in_order():
            newlist.append(item.data)
        self.assertEqual(ordered_list, newlist)



    def test_mixed_build(self):
        self.assertEqual(self.t2.root.data, self.t2_args[0])

        ordered_tree = list()
        for item in self.t2.return_in_order():
            ordered_tree.append(item.data)

        ordered_list = sorted(self.t2_args)

        self.assertEqual(ordered_list, ordered_tree)
        self.assertEqual(self.t2.get_size(), 9)

        ordered_tree = list()
        for item in self.t2.return_in_order():
            ordered_tree.append(item.data)
        temp_tree = bst(arglist=copy.deepcopy(ordered_tree))
        newlist = list()
        for item in temp_tree.return_in_order():
            newlist.append(item.data)
        self.assertEqual(ordered_list, newlist)


    def test_find_node(self):

        for i in range(1, 9):
            self.assertTrue(self.t1.find_node(i))
            self.assertTrue(self.t2.find_node(i))
            self.assertFalse(self.t1.find_node(-i))
            self.assertFalse(self.t2.find_node(-i))

    def test_depth(self):
        print "depth of t1: " + str(self.t1.get_depth())
        print "depth of t2: " + str(self.t2.get_depth())

    def test_debug(self):
        print "t1 in order: ",
        self.t1.print_in_order()
        print "t1 pre order: ",
        self.t1.print_in_order(order='pre')
        print "t1 post order: ",
        self.t1.print_in_order(order='post')
        print "t2 in order: ",
        self.t2.print_in_order()
        print "t2 pre order: ",
        self.t2.print_in_order(order='pre')
        print "t2 post order: ",
        self.t2.print_in_order(order='post')


if __name__ == '__main__':

    unittest.main()
