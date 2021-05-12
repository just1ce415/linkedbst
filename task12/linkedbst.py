"""
Laboratory 13.1
"""

from math import log
import sys
from time import time
from random import choice, randint
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_out = ""
            if node != None:
                str_out += recurse(node.right, level + 1)
                str_out += "| " * level
                str_out += str(node.data) + "\n"
                str_out += recurse(node.left, level + 1)
            return str_out

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_inleft_subtree_totop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None and not current_node.right == None:
            lift_max_inleft_subtree_totop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top: BSTNode
            :return: int
            """
            if top is None:
                return 0
            return 1 + max(height1(top.left), height1(top.right))

        h_out = height1(self._root)
        if not self.isEmpty():
            h_out -= 1
        return h_out

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return: bool
        """
        return self.height() < (2 * log(len(self) + 1, 2) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low: int, str ...
        :param high: int, str ...
        :return: list
        '''
        return list(filter(lambda item: low <= item <= high, self.inorder()))

    def rebalance(self):
        """
        Rebalances the tree.
        :return: None
        """

        def rebl_helper(data, first, last):
            if first <= last:
                if (first + last) % 2 != 0:
                    mid = ((first + last) // 2) + 1
                else:
                    mid = (first + last) // 2
                self.add(data[mid])
                rebl_helper(data, first, mid - 1)
                rebl_helper(data, mid + 1, last)

        if not self.is_balanced():
            data = list(self.inorder())
            self.clear()
            rebl_helper(data, 0, len(data) - 1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item: BSTNode.data
        :type item: int, str ...
        :return: int, str ...
        :rtype:
        """
        larger_items = list(filter(lambda x: x > item, self))
        if len(larger_items) > 0:
            return min(larger_items)
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item: BSTNode.data
        :type item: int, str...
        :return: int, str...
        :rtype:
        """
        smaller_items = list(filter(lambda x: x < item, self))
        if len(smaller_items) > 0:
            return max(smaller_items)
        return None

    def custom_add(self, elements):
        """
        Adds to the empty tree the list of elements.
        :param elements: list
        :rerurn: None
        """
        self.clear()
        self._root = BSTNode(elements[0])
        elements.pop(0)
        ptr = self._root
        for element in elements:
            if element < ptr.data:
                ptr.left = BSTNode(element)
                ptr = ptr.left
            else:
                ptr.right = BSTNode(element)
                ptr = ptr.right
            self._size += 1

    @classmethod
    def demo_bst(cls, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_lst = []
        with open(path, "r", encoding="utf-8") as fptr:
            for line in fptr:
                words_lst.append(line[:-1])
        # 1ST TEST
        random_words = []
        for _ in range(10000):
            rword = choice(words_lst)
            while rword in random_words:
                rword = choice(words_lst)
            random_words.append(rword)

        start = time()
        for word in random_words:
            word in words_lst
        finish = time()
        print("Liniar ('in') search time in the list: {} sec.".format(finish - start))

        # 2ND TEST
        tree = cls()
        tree.custom_add(words_lst)

        start = time()
        for word in random_words:
            word in tree
        finish = time()
        print(
            "Binary tree search based on sorted dictionary: {} sec.".format(
                finish - start
            )
        )

        # 3RD TEST
        tree.clear()
        length = len(words_lst)
        while length != 0:
            rword = words_lst.pop(randint(0, length - 1))
            length -= 1
            tree.add(rword)

        start = time()
        for word in random_words:
            word in tree
        finish = time()
        print(
            "Binary tree search based on randomized order: {} sec.".format(
                finish - start
            )
        )

        # 4TH TEST
        tree.rebalance()
        start = time()
        for word in random_words:
            word in tree
        finish = time()
        print("Rebalanced binary tree search: {} sec.".format(finish - start))


if __name__ == "__main__":
    LinkedBST.demo_bst("words.txt")
