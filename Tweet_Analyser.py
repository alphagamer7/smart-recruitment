import json
import nltk
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    Features

natural_language_understanding = NaturalLanguageUnderstandingV1(
    username="09785781-0496-4efd-99aa-6963edf76e43",
    password="2ZivE6WMFshH",
    version="2017-02-27")


class TweetAnalyser:

    def analyse_emotions(self, tweet):
        # print('Analysis Text:',tweet)
        response = natural_language_understanding.analyze(
            text=tweet,
            features=[
                Features.Emotion(),
                Features.Sentiment()
            ]
        )

        list_emotion = list(response['emotion']['document']['emotion'].values())
        list_emotion.append(response['sentiment']['document']['score'])
        print('List emotion is : ', list_emotion)
        return list_emotion

    def analyse_sentiment(self, tweet):
        response = natural_language_understanding.analyze(
            text=tweet,
            features=[
                Features.Sentiment()
            ]
        )

        result = response['sentiment']['document']['score']
        return result

    def get_count(self, text_given):
        tokenizer = nltk.tokenize.TweetTokenizer()

        c_user_mentions = 0
        c_url = 0
        c_exclam = 0
        c_Hash = 0
        c_question = 0
        c_rt = 0
        twe = str(text_given)
        tokens = tokenizer.tokenize(str(text_given))
        for word in tokens:
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
        return c_user_mentions, c_url, c_Hash, c_rt, c_exclam, c_question

    def facet_calculation(self, tweets):
        from watson_developer_cloud import PersonalityInsightsV2

        personality_insights = PersonalityInsightsV2(
            username='b20cc9a5-46d5-4a85-926e-dc3913851528',
            password='KdOka6znT2cN')

        obj = (personality_insights.profile(text=tweets))
        # openness
        # adventerous = obj['tree']['children'][0]['children'][0]['children'][0]['children'][0]['percentage']
        # artistic = obj['tree']['children'][0]['children'][0]['children'][0]['children'][1]['percentage']
        emotionality = obj['tree']['children'][0]['children'][0]['children'][0]['children'][2]['percentage']
        # imagination = obj['tree']['children'][0]['children'][0]['children'][0]['children'][3]['percentage']
        intellect = obj['tree']['children'][0]['children'][0]['children'][0]['children'][4]['percentage']
        liberalism = obj['tree']['children'][0]['children'][0]['children'][0]['children'][5]['percentage']
        opennessList = [emotionality, intellect, liberalism]

        # Conscientiousness
        # achievement_striving = obj['tree']['children'][0]['children'][0]['children'][1]['children'][0]['percentage']
        # cautiousness = obj['tree']['children'][0]['children'][0]['children'][1]['children'][1]['percentage']
        dutifulness = obj['tree']['children'][0]['children'][0]['children'][1]['children'][2]['percentage']
        orderliness = obj['tree']['children'][0]['children'][0]['children'][1]['children'][3]['percentage']
        self_discipline = obj['tree']['children'][0]['children'][0]['children'][1]['children'][4]['percentage']
        # self_efficacy = obj['tree']['children'][0]['children'][0]['children'][1]['children'][5]['percentage']
        conscienList = [dutifulness, orderliness, self_discipline]

        # Extraversion
        # activity_level = obj['tree']['children'][0]['children'][0]['children'][2]['children'][0]['percentage']
        # assertiveness = obj['tree']['children'][0]['children'][0]['children'][2]['children'][1]['percentage']
        # cheerfulness = obj['tree']['children'][0]['children'][0]['children'][2]['children'][2]['percentage']
        excitement_seeking = obj['tree']['children'][0]['children'][0]['children'][2]['children'][3]['percentage']
        friendliness = obj['tree']['children'][0]['children'][0]['children'][2]['children'][4]['percentage']
        gregariousness = obj['tree']['children'][0]['children'][0]['children'][2]['children'][5]['percentage']
        extraversionList = [excitement_seeking, friendliness, gregariousness]

        # Agreeableness
        # altruism = obj['tree']['children'][0]['children'][0]['children'][3]['children'][0]['percentage']
        cooperation = obj['tree']['children'][0]['children'][0]['children'][3]['children'][1]['percentage']
        # modesty = obj['tree']['children'][0]['children'][0]['children'][3]['children'][2]['percentage']
        morality = obj['tree']['children'][0]['children'][0]['children'][3]['children'][3]['percentage']
        # sympathy = obj['tree']['children'][0]['children'][0]['children'][3]['children'][4]['percentage']
        trust = obj['tree']['children'][0]['children'][0]['children'][3]['children'][5]['percentage']
        agreeList = [cooperation, morality, trust]

        # Emotional Range
        anger = obj['tree']['children'][0]['children'][0]['children'][4]['children'][0]['percentage']
        # anxiety = obj['tree']['children'][0]['children'][0]['children'][4]['children'][1]['percentage']
        depression = obj['tree']['children'][0]['children'][0]['children'][4]['children'][2]['percentage']
        # immoderation = obj['tree']['children'][0]['children'][0]['children'][4]['children'][3]['percentage']
        # self_consciousness = obj['tree']['children'][0]['children'][0]['children'][4]['children'][4]['percentage']
        vulnerability = obj['tree']['children'][0]['children'][0]['children'][4]['children'][5]['percentage']
        emotionList = [anger, depression, vulnerability]

        facetList = [opennessList, conscienList, extraversionList, agreeList, emotionList]
        return facetList
