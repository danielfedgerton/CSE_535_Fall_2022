'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math

class Node:
    def __init__(self, value: int, tf: float, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here
        """
        # The value is infact the document_id
        self.value = value
        self.tf = tf
        self.next = next
        self.skip = None

    def __eq__(self, __o: object) -> bool:
        return self.tf == __o.tf

    def __gt__(self, __o: object) -> bool:
        return self.tf > __o.tf


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class.
    """
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = [] #list of nodes
        if self.start_node is None:
            return traversal

        current_node: Node = self.start_node

        while (current_node):
            traversal.append(current_node)
            current_node = current_node.next

        return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return traversal
        
        current_node:Node = self.start_node

        while (current_node):
            if (current_node.skip) and (not current_node.skip in traversal):
                traversal.append(current_node.skip)
            current_node = current_node.skip    

        return traversal

    def add_skip_connections(self):
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented.
        """
        traversal = self.traverse_list()

        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1

        if n_skips <= 0: return
        self.skip_length = round(math.sqrt(self.length))
        position = 0

        while position < self.length:
            skip_target = position + self.skip_length
            if skip_target > (len(traversal)-1): break

            traversal[position].skip = traversal[skip_target]

            position = skip_target

        return
            


    def insert_at_end(self, value: int, tf: float):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """

        traversal = self.traverse_list()
        
        #handle condition where empty
        if not traversal:
            self.start_node = Node(value, tf)
            return

        temp_node = Node(value, tf)
        current_node = self.start_node

        #handling scenario where value of start node is greater than value to be inserted
        if current_node.value > value:
            temp_node.next = current_node
            self.start_node = temp_node
            return

        while (current_node):
            if current_node.value == value: 
                return

            elif (current_node.value < value) and (current_node.next is None):
                current_node.next = temp_node
                self.end_node = temp_node
                return

            elif ((current_node.value < value) and (current_node.next.value > value)):
                temp_node.next = current_node.next
                current_node.next = temp_node
                return

            current_node = current_node.next


        # Increment the length
        self.length += 1

        raise ValueError('element was not inserted')
