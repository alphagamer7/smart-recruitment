import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import bs4
import numpy as np
import nltk
from collections import defaultdict
import csv


class Preprocess:

    def clean_with_regex(self, unregTweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", unregTweet).split())

    def preprocess_tweet(self, tweet):
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        tweet = pattern.sub('', tweet.lower())

        lmtzr = WordNetLemmatizer()
        tweet = lmtzr.lemmatize(tweet)
        return tweet

    def get_pan_dataset(self):
        with open("dataset/truth.txt", "r") as text_file:
            lines = text_file.read().split('\n')

        lines = [line.split(":::") for line in lines]
        del lines[-1]

        tweets = []
        docLen = []
        for w in lines:
            filename = 'dataset/' + w[0] + '.xml'
            from xml.dom.minidom import parseString
            file = open(filename, 'rb')
            data = file.read()
            file.close()
            dom = parseString(data)
            docLen.append((len(dom.getElementsByTagName('document'))))
            doc_el = bs4.BeautifulSoup(open(filename, 'rb'), 'xml')
            tweet = [el.text for el in doc_el.findAll('document')]
            tweets.append(tweet)

        df = pd.DataFrame(lines)
        df['Tweets'] = tweets
        df['DocLen'] = docLen

        # for data visualisation in conda
        df.columns = ['username', 'Gender', 'Age', 'Extroverted', 'Neuroticism', 'Agreeable', 'Conscientious',
                      'Openness',
                      'Tweets', 'DocLen']
        cols = ['Extroverted', 'Neuroticism', 'Agreeable', 'Conscientious', 'Openness']
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)

        df['Extrovert_Score'] = np.where(df['Extroverted'] > 0, 1, 0)
        df['Neuroticism_Score'] = np.where(df['Neuroticism'] > 0, 1, 0)
        df['Agreeable_Score'] = np.where(df['Agreeable'] > 0, 1, 0)
        df['Conscientious_Score'] = np.where(df['Conscientious'] > 0, 1, 0)
        df['Openness_Score'] = np.where(df['Openness'] > 0, 1, 0)
        return df

    def get_pan_dataset_df(self):
        filename = 'pretrained/PANdf.pkl'
        # df.to_pickle(filename)
        df = pd.read_pickle(filename)
        return df

    def get_stat_count(self, df):
        c_user_mentions_L = []
        c_url_L = []
        c_Hash_L = []
        c_exclam_L = []
        c_question_L = []
        c_rt_L = []

        tokenizer = nltk.tokenize.TweetTokenizer()
        stuffs = df['Tweets']
        for w in stuffs:
            c_user_mentions = 0
            c_url = 0
            c_exclam = 0
            c_Hash = 0
            c_question = 0
            c_rt = 0
            tokens = tokenizer.tokenize(str(w))
            for word in tokens:
                #         print(word)
                if word.startswith('@'):
                    c_user_mentions += 1
                if word.startswith('http'):
                    c_url += 1
                if word.startswith('#'):
                    c_Hash += 1
                if word.startswith('RT') or word.startswith('rt'):
                    c_rt += 1
                if word.startswith('!'):
                    c_exclam += 1
                if word.startswith('?'):
                    c_question += 1
            c_user_mentions_L.append(c_user_mentions)
            c_url_L.append(c_url)
            c_Hash_L.append(c_Hash)
            c_exclam_L.append(c_exclam)
            c_question_L.append(c_question)
            c_rt_L.append(c_rt)

        df['User Mentions'] = c_user_mentions_L
        df['No Of URLS '] = c_url_L
        df['Exclamations'] = c_url_L
        df['Hashtags'] = c_Hash_L
        df['Question Marks'] = c_question_L
        df['Retweets'] = c_rt_L

        df['Normalised User Mentions'] = df['User Mentions'] / df['DocLen']
        df['Normalised No Of URLS'] = df['No Of URLS '] / df['DocLen']
        df['Normalised Hashtags'] = df['Hashtags'] / df['DocLen']
        df['Normalised Retweets'] = df['Retweets'] / df['DocLen']
        df['Normalised Exclamations'] = df['Exclamations'] / df['DocLen']
        df['Normalised Question Marks'] = df['Question Marks'] / df['DocLen']
        return df

    def build_data_cv(self, datafile, cv=1, clean_string=True):
        revs = []
        vocab = defaultdict(float)

        with open(datafile, "rt") as csvf:
            csvreader = csv.reader(csvf, delimiter=',', quotechar='"')
            first_line = True
            for line in csvreader:
                if first_line:
                    first_line = False
                    continue
                status = []
                sentences = re.split(r'[.?]', line[1].strip())
                try:
                    sentences.remove('')
                except ValueError:
                    None

                for sent in sentences:
                    if clean_string:
                        orig_rev = self.clean_str(sent.strip())
                        if orig_rev == '':
                            continue
                        words = set(orig_rev.split())
                        splitted = orig_rev.split()
                        if len(splitted) > 150:
                            orig_rev = []
                            splits = int(np.floor(len(splitted) / 20))
                            for index in range(splits):
                                orig_rev.append(' '.join(splitted[index * 20:(index + 1) * 20]))
                            if len(splitted) > splits * 20:
                                orig_rev.append(' '.join(splitted[splits * 20:]))
                            status.extend(orig_rev)
                        else:
                            status.append(orig_rev)
                    else:
                        orig_rev = sent.strip().lower()
                        words = set(orig_rev.split())
                        status.append(orig_rev)

                    for word in words:
                        vocab[word] += 1

                datum = {
                    "y0": 1 if line[2].lower() == 'y' else 0,
                    "y1": 1 if line[3].lower() == 'y' else 0,
                    "y2": 1 if line[4].lower() == 'y' else 0,
                    "y3": 1 if line[5].lower() == 'y' else 0,
                    "y4": 1 if line[6].lower() == 'y' else 0,
                    "text": status,
                    "user": line[0],
                    "num_words": np.max([len(sent.split()) for sent in status]),
                    "split": np.random.randint(0, cv)}
                revs.append(datum)

        return revs, vocab

    def clean_str(self, string, TREC=False):
        string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
        string = re.sub(r"\'s", " \'s ", string)
        string = re.sub(r"\'ve", " have ", string)
        string = re.sub(r"n\'t", " not ", string)
        string = re.sub(r"\'re", " are ", string)
        string = re.sub(r"\'d", " would ", string)
        string = re.sub(r"\'ll", " will ", string)
        string = re.sub(r",", " , ", string)
        string = re.sub(r"!", " ! ", string)
        string = re.sub(r"\(", " ( ", string)
        string = re.sub(r"\)", " ) ", string)
        string = re.sub(r"\?", " \? ", string)
        string = re.sub(r"\s{2,}", " ", string)
        return string.strip() if TREC else string.strip().lower()
