"""
The Trie data structure keeps a set of words, organized with one node for each letter.
Each node has a branch for each letter that may follow it in the set of words.
"""


class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

    def insert(self, word):
        """
        inserts the given word to the trie node
        :param word: the given word
        :return:
        """
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.word = word
