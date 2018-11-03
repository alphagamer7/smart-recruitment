import unittest
from  app import app
import unittest
from preprocess import Preprocess
import pandas as pd
import pickle
import unittest
from Tweet_Analyser import TweetAnalyser


class CombinedTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        self.preprocess = Preprocess()
        self.tweet_analyser = TweetAnalyser()

    def test_add_view(self):
        tester=app.test_client(self)
        response = tester.get('/add', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_analyse_view(self):
        response = self.tester.get('/analyse', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_compares_view(self):
        response = self.tester.get('/compare', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_route(self):
        response = self.tester.get('/add', content_type='html/text')
        self.assertTrue(b'Enter Twitter Handle' in response.data)

    def test_analyse_route(self):
        response = self.tester.get('/analyse', content_type='html/text')
        self.assertTrue(b'Enter Twitter Username' in response.data)

    def test_index_route(self):
        response = self.tester.get('/index', content_type='html/text')
        self.assertTrue(b'Personality Score' in response.data)

    def test_compare_route(self):
        response = self.tester.get('/compare', content_type='html/text')
        self.assertTrue(b'Personality Rec' in response.data)

    def test_index_view(self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_remove_stopwords_none(self):
        test_text = ''
        res = ''
        self.assertEqual(res, self.preprocess.preprocess_tweet(test_text))

    def test_remove_stopwords_full(self):
        test_text = "I am falling always man you wanna see. Oh Man I am telling you this is a crazy feelingso high High! SO crazy!"
        res = 'falling always man wanna see. oh man telling crazy feelingso high high! crazy!'
        self.assertEqual(res, self.preprocess.preprocess_tweet(test_text))

    def test_regex_remove_punctuation(self):
        test_text = "I am falling always man you wanna see Oh Man I am telling you this is a crazy feelingso high High! SO crazy!"
        res = 'I am falling always man you wanna see Oh Man I am telling you this is a crazy feelingso high High SO crazy'
        self.assertEqual(res, self.preprocess.clean_with_regex(test_text))

    def test_regex_remove_punctuation_none(self):
        test_text = ''
        res = ''
        self.assertEqual(res, self.preprocess.clean_with_regex(test_text))
    def test_analyse_sentiment(self):
        test_text = "Doesn't seem like that long ago that @hmason & I published this on this date w/ @mikeloukides's help. Even more relevant today. And still free for you to read & share #DataScience #BigData RT "
        res = 0.279558
        self.assertEqual(res, self.tweet_analyser.analyse_sentiment(test_text))

    def test_analyse_emotion(self):
        test_text = "Doesn't seem like that long ago that @hmason & I published this on this date w/ @mikeloukides's help. Even more relevant today. And still free for you to read & share #DataScience #BigData RT "
        res = [0.555572, 0.255764, 0.066807, 0.114113, 0.024902, 0.279558]
        self.assertEqual(res, self.tweet_analyser.analyse_emotions(test_text))

    def test_getcount(self):
        test_text = "Doesn't seem like that long ago that @hmason & I published this on this date w/ @mikeloukides's help. Even more relevant today. And still free for you to read & share #DataScience #BigData RT "
        res = (2, 0, 2, 1, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_zero(self):
        test_text = ''
        res = (0, 0, 0, 0, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_usermention(self):
        test_text = '@usermention'
        res = (1, 0, 0, 0, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_link(self):
        test_text = 'http://test.com'
        res = (0, 1, 0, 0, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_hash(self):
        test_text = '#metoo'
        res = (0, 0, 1, 0, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_rt(self):
        test_text = 'rt'
        res = (0, 0, 0, 1, 0, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_exclaimation(self):
        test_text = '!'
        res = (0, 0, 0, 0, 1, 0)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))

    def test_getcount_questionmark(self):
        test_text = '?'
        res = (0, 0, 0, 0, 0, 1)
        self.assertEqual(res, self.tweet_analyser.get_count(test_text))