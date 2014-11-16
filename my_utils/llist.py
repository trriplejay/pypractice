import unittest
import random

"""
Contains python implementation of some common linked list operations.
in reality, there is no need for a python linked list, since the list()
structure is essentially the same thing, but this was for practice
includes:
    merge-sort (in place)
    list reversal (iterative)
    cycle-detection

also includes unit tests for all implementations

"""

class node(object):

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class llist(object):

    def __init__(self, head=None):
        # a node representing head of list
        if head is not None:
            self.head = head

            while head is not None:
                head = head.next
            self.tail = head

        else:
            self.head = None
            self.tail = None

    def find_node(self, data):
        # return a node, if it exists, with self.data value of data
        current = self.head
        while current is not None:
            if current.data == data:
                return data
            current = current.next

    def add_node(self, data):
        if self.head is None:
            self.head = node(data)
            self.tail = self.head

        else:
            self.tail.next = node(data)
            self.tail = self.tail.next

    def del_node(self, data):
        curr = self.head
        if curr.data == data:
            self.head = curr.next
        else:
            while curr.next is not None:
                if curr.next.data == data:
                    curr.next = curr.next.next
                    break
                curr = curr.next

    def reverse(self):
        # reverses the current order of the linked list
        prev = None
        curr = self.head

        self.tail = curr
        while curr is not None:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        self.head = prev

    def has_cycle(self):
        """
        detect the existence of an infinite loop within the linked list
        """
        normal = self.head
        fast = self.head

        while normal is not None and fast is not None:
            fast = fast.next
            if normal == fast:
                return True
            if fast is None:
                break
            fast = fast.next
            normal = normal.next
        # if normal never equalled fast, there was no loop
        return False

    def get_size(self, a=None):
        # returns size of the linked list passed in
        if a is None:
            a = self.head
        count = 0
        while a is not None:
            count += 1
            a = a.next
        return count

    def split_list(self, a, size=None):
        # returns a tuple of size 2, each containing the head of a new list
        if size is None:
            size = self.get_size(a)
        temp = a
        count = 0
        if size <= 2:
            b = a.next
            a.next = None
        else:
            while count < size/2:
                count += 1
                temp = temp.next
            b = temp.next
            temp.next = None

        return (a, b)

    def sort(self, method='merge'):

        if method == 'merge':
            # split the list in half (by breaking the 'next' link) and call
            # "merge" on each half
            self.head = self.mergesort(*self.split_list(self.head))
        else:
            pass
            #TODO:
            #   quicksort
            #   bubblesort
            #   insertion sort
            #   bogosort! ok not really... maybe with a forced size limit

    def mergesort(self, a, b):

        sizeA = self.get_size(a)
        sizeB = self.get_size(b)
        #print "size a: " + str(sizeA) + " size b: " + str(sizeB)
        if sizeA > 1:
            a = self.mergesort(*self.split_list(a, sizeA))
        if sizeB > 1:
            b = self.mergesort(*self.split_list(b, sizeB))

        return self.merge(a, b)
        #self.merge(a, b)


    def merge(self, a, b):
        # iterate over a and b, and return a single list in order
        #print "merging ",
        #self.print_list(a)
        #print " and ",
        #self.print_list(b)
        done = False
        final_head = None
        final_index = None
        a_index = a
        b_index = b
        count = 0
        while not done:
            if a_index is None and b_index is None:
                done = True

            elif a_index is None and final_index is not None:
                final_index.next = b_index
                done = True

            elif b_index is None and final_index is not None:
                final_index.next = a_index
                done = True

            elif b_index is None:
                final_head = b_index
                done = True

            elif a_index is None:
                final_head = a_index
                done = True

            elif a_index.data <= b_index.data:
                if final_head is None:
                    final_head = a
                    final_index = a_index
                else:
                    final_index.next = a_index
                    final_index = final_index.next

                a_index = a_index.next

            else:
                if final_head is None:
                    final_head = b
                    final_index = b_index
                else:
                    final_index.next = b_index
                    final_index = final_index.next

                b_index = b_index.next

            count += 1
            #print str(count) + " merge step chose: " + str(final_index.data)

        return final_head

    def print_list(self, curr=None):
        """
        print the list formatted to look like a real python list
        """
        if not self.has_cycle():
            if curr is None:
                curr = self.head
            print "[",
            while curr is not None:
                print str(curr.data) + ",",
                curr = curr.next
            print "]"


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        # create default lists to test/compare llist vs python list
        self.pre = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rev = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.small = [1, 5, 2, 7, 0, 8, 9, 3, 4, 6]
        self.big = [x for x in range(-500, 500)]

    def build_llist(self, a):
        # take in list a, turn it into llist and return it
        thelist = llist()
        for item in a:
            thelist.add_node(item)
        return thelist

    def build_list(self, b):
        # takes a llist and returns a python list
        temp = b.head
        result = list()
        while temp is not None:
            result.append(temp.data)
            temp = temp.next

        return result

    def test_llist_init(self):
        thelist = llist()
        self.assertIsNone(thelist.head)
        self.assertIsNone(thelist.tail)
        thelist.add_node(5)
        self.assertIsNotNone(thelist.head)
        self.assertIsNotNone(thelist.tail)
        self.assertIsInstance(thelist.head, node)
        self.assertIsInstance(thelist.tail, node)
        self.assertEqual(thelist.head, thelist.tail)
        thelist.add_node(0)
        self.assertNotEqual(thelist.head, thelist.tail)

    def test_llist_reversal(self):
        thelist = self.build_llist(self.small)
        self.assertEqual(self.small, self.build_list(thelist))
        thelist.reverse()
        self.assertEqual(list(reversed(self.small)), self.build_list(thelist))

    def test_presort(self):
        # compare presorted list to the result of calling llist sort on
        # the same list. should be equal
        thelist = self.build_llist(self.pre)
        thelist.sort()
        self.assertEqual(self.pre, self.build_list(thelist))
        thelist = self.build_llist(self.pre)
        thelist.sort()
        self.pre.sort()
        self.assertEqual(self.pre, self.build_list(thelist))

    def test_reverse_sort(self):
        thelist = self.build_llist(self.rev)
        thelist.sort()
        self.rev.sort()
        self.assertEqual(self.rev, self.build_list(thelist))

    def test_small_sort(self):
        thelist = self.build_llist(self.small)
        thelist.sort()
        self.small.sort()
        self.assertEqual(self.small, self.build_list(thelist))

    def test_small_randomness(self):
        # randomize the small list several times and sort.
        # make sure default sort does same thing as merge sort
        for i in range(0, 10):
            random.shuffle(self.small)
            thelist = self.build_llist(self.small)
            thelist.sort()
            self.small.sort()
            self.assertEqual(self.small, self.build_list(thelist))

    def test_big_randomness(self):

        for i in range(0, 10):
            random.shuffle(self.big)
            thelist = self.build_llist(self.big)
            thelist.sort()
            self.big.sort()
            self.assertEqual(self.big, self.build_list(thelist))


    def test_cycles(self):

        n1 = node(data=0)
        n2 = node(data=1, next=n1)
        n3 = node(data=2, next=n2)
        n4 = node(data=4, next=n3)
        n5 = node(data=5, next=n4)
        head_node = node(data=6, next=n5)
        thelist = llist(head=head_node)
        self.assertFalse(thelist.has_cycle())
        n1.next = n4 # create a cycle
        self.assertTrue(thelist.has_cycle())



if __name__ == '__main__':

    unittest.main()
