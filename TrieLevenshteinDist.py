#!/usr/bin/python
#By Steve Hanov, 2011. Released to the public domain
import time
from post_process.trie_levenshtein.TrieNode import TrieNode
import utils.general_utils as gen_util


class TrieLevenshteinDist:
    # TODO : The following list should be completed in future
    similar_chars = ['اإأآآِاٌاَاُاِ', 'یبئنپتث', 'جچحخ', 'دذ', 'روزژ', 'سشصض', 'عغ', 'فق', 'کگ', 'طظ']

    def make(self, dict_path):
        """
        makes trie structure based on the dict. given to it
        :param dict_path: path of word dictionary
        :return: trie structure
        """
        # read dictionary file into a trie
        trie = TrieNode()
        for word in open(dict_path, encoding="utf8").read().split():
            # WordCount += 1
            trie.insert(word)
        return trie

    def index_of_array_elements(self, array, sub_element):
        """
        finds index of element of array contains the sub_element
        For example if the array = ['lor', 'pcg', 'itu', 'dsa'] and sub_element = 'a' then the returned value is 3
        :param array: the input array that the sub_element is searched in it.
        :param sub_element: the sub_element that is searched in array.
        :return: index of sub_element in array.
        """
        index = -1
        for element in array:
            index = index + 1
            if element.__contains__(sub_element):
                return index
        return index

    def is_new_word_acceptable(self, main_word, new_word):
        """
        Checks that the new word obtained from dictionary search is acceptable or not. The decision is based on similar
        words in persian language
        :param main_word: the main_word that the dict. is searched for finding nearest words to it
        :param new_word: the new word that is similar to main word
        :return: is acceptable or not
        """
        # length of two words must be the same
        if main_word.__len__() != new_word.__len__():
            return False
        # checking similar chars in two words
        for i in range(0, main_word.__len__()):
            main_letter = main_word[i]
            new_letter = new_word[i]
            # letter 'ی' in end of word should not be replaced by 'یبئنپتث'
            if (new_letter == 'ی' or main_letter == 'ی') and i == main_word.__len__() - 1:
                return False

            if main_letter == new_letter:
                continue
            #Check that the replaced character in new_word is one of similar letters in its group in similar_chars array
            index = self.index_of_array_elements(self.similar_chars, main_letter)
            if not(index > -1 and self.similar_chars[index].__contains__(new_letter)):
                return False
        return True

    def search_recursive(self, node, letter, word, previous_row, result_list, max_cost):
        """
        Is used by the find_nearest_words function . It assumes that the previousRow has been filled in already.
        :param node:
        :param letter:
        :param word:
        :param previous_row:
        :param result_list:
        :param max_cost:
        :return:
        """
        columns = len(word) + 1
        current_row = [previous_row[0] + 1]

        # Build one row for the letter, with a column for each letter in the target
        # word, plus one for the empty string at column 0
        for column in range(1, columns):

            insert_cost = current_row[column - 1] + 1
            delete_cost = previous_row[column] + 1

            if word[column - 1] != letter:
                replace_cost = previous_row[column - 1] + 1
            else:
                replace_cost = previous_row[column - 1]

            current_row.append(min(insert_cost, delete_cost, replace_cost))
            # current_row.append(replace_cost)

        # if the last entry in the row indicates the optimal cost is less than the
        # maximum cost, and there is a word in this trie node, then add it.
        if current_row[-1] <= max_cost and node.word != None and self.is_new_word_acceptable(word, node.word):
            result_list.append(node.word) #((node.word, current_row[-1]))

        # if any entries in the row are less than the maximum cost, then
        # recursively search each branch of the trie
        if min(current_row) <= max_cost:
            for letter in node.children:
                self.search_recursive(node.children[letter], letter, word, current_row,
                                      result_list, max_cost)

    def find_nearest_words(self, trie, word, max_dist):
        """
        finds a list of all words that are less than the given maximum distance from the target word
        :param trie: trie object holding dictionary
        :param word: word to find nearest words to it
        :param max_dist: maximum levenshtein distance that the words in the result have to the target word
        :return: list of all words that are less than the given maximum distance from the target word
        """
        # build first row
        current_row = range(len(word) + 1)
        result_list = []
        # recursively search each branch of the trie
        for letter in trie.children:
            self.search_recursive(trie.children[letter], letter, word, current_row,
                                  result_list, max_dist)
        # result_list.append(word)
        return str(result_list).replace(",", "|").replace("| ", "|").replace("'", "")

    def save(self, trie_obj, trie_file_path):
        """
        saves the trie in pkl format in path specified
        :param trie_obj: dictionary trie
        :param trie_file_path: path to save the trie
        :return:
        """
        gen_util.write_array_to_pickle_file(trie_file_path, trie_obj)

    def load(self, trie_file_path):
        """
        loads the trie from the pkl file path specified
        :param trie_file_path: grah file path
        :return: saved trie
        """
        trie_obj = gen_util.read_array_from_pickle_file(trie_file_path)
        return trie_obj


if __name__ == '__main__':
    dict_path = "../rsc/dict/allwords_1615.dict"
    trie_file_path = "../rsc/dict/trie_allwords_1615.pkl"
    word = 'قالی'
    max_cost = 2
    tld = TrieLevenshteinDist()
    start = time.time()
    trie_obj = tld.make(dict_path)
    print("Making trie took {0} s".format(time.time() - start))
    start = time.time()
    tld.save(trie_obj, trie_file_path)
    print("Saving trie took {0} s".format(time.time() - start))
    start = time.time()
    trie_obj = tld.load(trie_file_path)
    print("Loading trie took {0} s".format(time.time() - start))
    start = time.time()
    results = tld.find_nearest_words(trie_obj, word, max_cost)
    print("Search in trie took {0} s".format(time.time() - start))
    print(results)
