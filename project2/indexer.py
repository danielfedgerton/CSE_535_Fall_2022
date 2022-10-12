'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import numpy as np

from typing import Dict, List, Set
from linkedlist import LinkedList, Node
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.doc_ids:  Set[int] = set()

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index.
        This in turn uses the function add_to_index.
        """
        # Keeping track of stuff we have already added.
        tf_dict: Dict[str, float] = {}

        # Token = term in this function
        for token in tokenized_document:
            # It is important to understand that you only add a term from a document
            # once. For instance, in "Football is love. Football is life.", 'football'
            # is added just the one time.
            # This is to ensure no duplicates exist in the postings list.
            if not token in tf_dict:
                tf_dict[token]: float = self.calculate_tf(
                    token, tokenized_document)

        # Now that we have our set of unique tokens in a document, we
        # `add_to_index`
        for term in tf_dict:
            self.add_to_index(term, doc_id, tf_dict[term])

        # And we add the doc_id to the list of doc_ids
        self.doc_ids.add(doc_id)

    def add_to_index(self, term_, doc_id_, tf):
        if term_ not in self.inverted_index:
            llist = LinkedList()
            llist.insert_at_end(doc_id_, tf)
            self.inverted_index[term_] = llist
            return

        self.inverted_index[term_].insert_at_end(doc_id_, tf)

        return

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for t in self.inverted_index:
            llist = LinkedList()
            llist.insert_at_end(self.inverted_index.get(t))
            llist.add_skip_connections()
            self.inverted_index[t] = llist

    def calculate_tf(self, token: str, tokenized_document: List[str]) -> float:
        """Calculates the normalized (occurances_of_term_in_doc/num_of_terms_in_doc)
        tf for each term in a document.
        """
        count = 0
        for tkn in tokenized_document:
            if tkn == token: count += 1

        return count / len(tokenized_document)

    @classmethod
    def binary_search(cls, node_id: int, term_pplist: List[Node]) -> Node:
        """Searches for a node with the value `node_id`

        Args:
            node (int): The node you were looking for.
        """
        lower_bound: int = 0
        upper_bound: int = len(term_pplist)

        curr_idx = len(term_pplist) // 2

        while(lower_bound <= upper_bound):
            if term_pplist[curr_idx].value == node_id:
                return term_pplist[curr_idx]

            elif term_pplist[curr_idx] > node_id:
                upper_bound = curr_idx - 1
            else: lower_bound = curr_idx + 1

        raise ValueError("Something went wrong with your postings list creation, "\
            "check it out! :)")

    def calculate_tf_idf(self):
        """Calculate tf-idf score for each document in the postings lists of the index.
        To be implemented.
        """
        corpus_vector = np.zeroes((len(self.doc_ids), len(self.inverted_index)))

        # They want a vector for each doc that has the shape 1 X N (N is the number of
        # unique terms in the corpus)
        for doc_idx, doc_id in enumerate(self.doc_ids):
            for term_idx, term in enumerate(self.inverted_index):
                term_pplist = self.inverted_index[term].traverse_list()

                # The number fo documents in which the term appears
                num_of_appear = len()
                # Computing idf
                idf = np.log(len(self.doc_ids)) - np.log(1+num_of_appear)

                # Finding in the traversal (wiz sorted) the node for the `doc_id`
                tf = self.binary_search(doc_id, term_pplist).tf

                corpus_vector[doc_idx, term_idx] = tf * idf

        return