import unittest


from Tweet_Analyser import TweetAnalyser


class AnalyserTest(unittest.TestCase):
    def setUp(self):
        self.tweet_analyser = TweetAnalyser()

    def test_analyse_sentiment(self):
        test_text = "Doesn't seem like that long ago that @hmason & I published this on this date" \
                    " w/ @mikeloukides's help. Even more relevant today. And still free fo" \
                    "r you to read & share #DataScience #BigData RT "
        res = 0.279558
        self.assertEqual(res, self.tweet_analyser.analyse_sentiment(test_text))

    def test_analyse_emotion(self):
        test_text = "Doesn't seem like that long ago that @hmason & I published t" \
                    "his on this date w/ @mikeloukides's help. Even more relevant toda" \
                    "y. And still free for you to read & share #DataScience #BigData RT "
        res = [0.555572, 0.255764, 0.066807, 0.114113, 0.024902, 0.279558]
        self.assertEqual(res, self.tweet_analyser.analyse_emotions(test_text))

    def test_getcount(self):
        test_text = "Doesn't seem like that long ago that @hmason" \
                    " & I published this on this date w/ @mikeloukides's help. Even more relevant today. And still free for you to read & share #DataScience #BigData RT "
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