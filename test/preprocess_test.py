import unittest
from preprocess import Preprocess
import pandas as pd
import pickle

class AppTest(unittest.TestCase):

    def setUp(self):
        self.preprocess = Preprocess()

    def test_remove_stopwords_none(self):
        test_text = ''
        res = ''
        self.assertEqual(res, self.preprocess.preprocess_tweet(test_text))

    def test_remove_stopwords_full(self):
        test_text = "I am falling always man you wanna see. Oh Man I am telling you this is a crazy" \
                    " feelingso high High! SO crazy!"
        res = 'falling always man wanna see. oh man telling crazy feelingso high high! crazy!'
        self.assertEqual(res, self.preprocess.preprocess_tweet(test_text))

    def test_regex_remove_punctuation(self):
        test_text = "I am falling always man you wanna see Oh Man I am telling you this is a" \
                    " crazy feelingso high High! SO crazy!"
        res = 'I am falling always man you wanna see Oh Man I am telling you this is a crazy ' \
              'feelingso high High SO crazy'
        self.assertEqual(res, self.preprocess.clean_with_regex(test_text))

    def test_regex_remove_punctuation_none(self):
        test_text = ''
        res = ''
        self.assertEqual(res, self.preprocess.clean_with_regex(test_text))






