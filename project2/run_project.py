'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import heapq
import queue

from typing import Dict, List, Tuple
from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList, Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, t1_pplist: List[Node],
               t2_pplist: List[Node]) -> Tuple[int, List[Node]]:
        """ Implement the merge algorithm to merge 2 postings list at a time.
        Use appropriate parameters & return types.
        While merging 2 postings list, preserve the maximum tf-idf value of a document.
        """
        merged_pplist: List[Node] = []
        # Comparison counts
        comp_cnt = 0

        l1_index = 0
        l2_index = 0

        while (l1_index < len(t1_pplist) and l2_index < len(t1_pplist)):
            if t1_pplist[l1_index].value == t2_pplist[l2_index].value:
                # Adding up the term frequencies and consider it to be the score.
                merged_pplist.append(
                    Node(t1_pplist[l1_index].value,
                         t1_pplist[l1_index].tf + t2_pplist[l2_index].tf))

                l1_index += 1
                l2_index += 1

            # Increment indices accordingly
            elif t1_pplist[l1_index].value > t2_pplist[l2_index].value:
                l2_index += 1

            else:
                l1_index += 1

            comp_cnt += 1

        return comp_cnt, merged_pplist

    def _daat_and(self,
                  query_terms: List[str],
                  enable_skips: bool = False,
                  topn: int = 10) -> Tuple[int, List[int]]:
        """Implement the DAAT AND algorithm, which merges the postings list of
        N query terms. Use appropriate parameters & return types.
        """
        overall_comparisons = 0
        inverted_lists: List[List[Node]] = []
        for term in query_terms:
            inverted_lists.append(self._get_postings(term, enable_skips))

        current_merged_list = inverted_lists[0]
        for in_list in inverted_lists[1:]:
            comp_cnt, current_merged_list = self._merge(
                current_merged_list, in_list)
            overall_comparisons += comp_cnt

        return overall_comparisons, [
            node.value for node in heapq.nlargest(topn, current_merged_list)
        ]

    def _get_postings(self,
                      term: str,
                      enable_skips: bool = False) -> List[Node]:
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        if enable_skips:
            return self.indexer.inverted_index[term].traverse_skips()

        return self.indexer.inverted_index[term].traverse_list()

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r', encoding='utf-8') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document: List[str] = self.preprocessor.tokenizer(
                    document)
                self.indexer.generate_inverted_index(doc_id,
                                                     tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        # self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {
            "index_type": str(type(index)),
            "indexer_type": str(type(self.indexer)),
            "post_mem": str(index[kw]),
            "post_type": str(type(index[kw])),
            "node_mem": str(index[kw].start_node),
            "node_type": str(type(index[kw].start_node)),
            "node_value": str(index[kw].start_node.value),
            "command_result": eval(command) if "." in command else ""
        }

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {
            'postingsList': {},
            'postingsListSkip': {},
            'daatAnd': {},
            'daatAndSkip': {},
            'daatAndTfIdf': {},
            'daatAndSkipTfIdf': {},
            'sanity': self.sanity_checker(random_command)
        }

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = self.preprocessor.tokenizer(query)  # Tokenized query. To be implemented.

            for term in input_term_arr:
                postings, skip_postings = self._get_postings(term, enable_skips=False),\
                    self._get_postings(term, enable_skips=True)
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = [i.value for i in postings]
                output_dict['postingsListSkip'][term] = [i.value for i in skip_postings]

            and_op_no_skip_sorted, and_op_skip_sorted =None, None
            and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None

            and_comparisons_no_skip, and_op_no_skip = self._daat_and(input_term_arr, enable_skips=False)
            and_comparisons_skip, and_op_skip = self._daat_and(input_term_arr, enable_skips=True)

            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(
                and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(
                and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(
                and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(
                and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][
                query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][
                query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][
                query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][
                query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][
                query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][
                query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][
                query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][
                query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip(
            )]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][
                query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][
                query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][
                query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]
    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)
    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus",
                        type=str,
                        help="Corpus File name, with path.")
    parser.add_argument("--output_location",
                        type=str,
                        help="Output file name.",
                        default=output_location)
    parser.add_argument(
        "--username",
        type=str,
        help=
        "Your UB username. It's the part of your UB email id before the @buffalo.edu. "
        "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()
    """ Initialize the project runner"""
    runner = ProjectRunner()
    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
