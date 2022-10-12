'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from typing import Dict, List
from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

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
            # Assertion fails if a false is returned
            assert self.add_to_index(term, tf_dict[term])

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

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""

        raise NotImplementedError
