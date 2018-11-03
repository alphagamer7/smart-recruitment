import pandas as pd
from Tweet_Analyser import TweetAnalyser
from preprocess import Preprocess
from Classifier import Classifier



class ML_Facade:
    def ml_process(self, tweets, count):
        store = pd.HDFStore('pretrained/store.h5')
        df = store['df']  # load it
        store.close()

        stweet = ''

        stweet = tweets


        tweet_analyser = TweetAnalyser()
        c_user_mentions_pred, c_url_pred, c_Hash_pred, c_rt_pred, c_exclam_pred, c_question_pred = tweet_analyser.get_count(
            stweet)


        c_user_mentions_pred = c_user_mentions_pred / count
        c_url_pred = c_url_pred / count
        c_Hash_pred = c_Hash_pred / count
        c_rt_pred = c_rt_pred / count
        c_exclam_pred = c_exclam_pred / count
        c_question_pred = c_question_pred / count


        p = Preprocess()

        stweet = p.clean_with_regex(stweet)


        stweet = p.preprocess_tweet(stweet)

        facetList = tweet_analyser.facet_calculation(stweet)

        """Coded fucntion to get from ESSAY dataset releveant stuffs"""

        """End Code stuff to get from ESSAY dataset"""


        print(" ML Essay dataset Function Call")

        classifier = Classifier()



        extro_word_score = classifier.semantic_classification(df['text'], df['y0'], "Extraversion", stweet)
        neuro_word_socre = classifier.semantic_classification(df['text'], df['y1'], "Neuroticism", stweet)
        agree_word_score = classifier.semantic_classification(df['text'], df['y2'], "Agreeableness", stweet)
        consci_word_score = classifier.semantic_classification(df['text'], df['y3'], "Conscientiousness", stweet)
        open_word_score = classifier.semantic_classification(df['text'], df['y4'], "Openness", stweet)
        print("End ML Essay dataset  function Call")

        print("Scores Essay crosscheck: ")
        print("EXTRO-", extro_word_score)
        print("NEURO-", neuro_word_socre)
        print("AGREE-", agree_word_score)
        print("CONSCI-", consci_word_score)
        print("OPEN-", open_word_score)



        pan_df = p.get_pan_dataset_df()


        pan_df = p.get_stat_count(pan_df)



        emotion_list = tweet_analyser.analyse_emotions(stweet)

        extrov_emotion_score = classifier.emotion_analysis_text(pan_df, "Extroverted", emotion_list)
        neuro_emotion_score = classifier.emotion_analysis_text(pan_df, "Neuroticism", emotion_list)
        agree_emotion_score = classifier.emotion_analysis_text(pan_df, "Agreeable", emotion_list)
        consc_emotion_score = classifier.emotion_analysis_text(pan_df, "Conscientious", emotion_list)
        open_emotion_score = classifier.emotion_analysis_text(pan_df, "Openness", emotion_list)

        """code to compute HR_LEAD attribute from empath"""


        """end ccode to compute LIWC"""


        extro_score_stats = classifier.cal_stat_personality(pan_df, "Extroverted", c_user_mentions_pred, c_url_pred,
                                                            c_Hash_pred, c_rt_pred, c_exclam_pred, c_question_pred)
        neuro_score_stats = classifier.cal_stat_personality(pan_df, "Neuroticism", c_user_mentions_pred, c_url_pred,
                                                            c_Hash_pred, c_rt_pred, c_exclam_pred, c_question_pred)
        agree_score_stats = classifier.cal_stat_personality(pan_df, "Agreeable", c_user_mentions_pred, c_url_pred,
                                                            c_Hash_pred,
                                                            c_rt_pred, c_exclam_pred, c_question_pred)
        consc_score_stats = classifier.cal_stat_personality(pan_df, "Conscientious", c_user_mentions_pred, c_url_pred,
                                                            c_Hash_pred, c_rt_pred, c_exclam_pred, c_question_pred)
        open_score_stats = classifier.cal_stat_personality(pan_df, "Openness", c_user_mentions_pred, c_url_pred,
                                                           c_Hash_pred,
                                                           c_rt_pred, c_exclam_pred, c_question_pred)

        print("EXTRO STAT  : ", extro_score_stats)
        print("NEURO STAT  : ", neuro_score_stats)
        print("AGREE STAT  : ", agree_score_stats)
        print("CONSC STAT : ", consc_score_stats)
        print("OPEN STAT  : ", open_score_stats)



        extrovScore = ((0.35 * extro_score_stats[0]) + (0.34 * extrov_emotion_score[0]) + (
                    0.31 * extro_word_score[0])) * 100
        neuroScore = ((0.35 * neuro_score_stats[0]) + (0.34 * neuro_emotion_score[0]) + (
                    0.31 * neuro_word_socre[0])) * 100
        agreeScore = ((0.35 * agree_score_stats[0]) + (0.34 * agree_emotion_score[0]) + (
                    0.31 * agree_word_score[0])) * 100
        conscScore = ((0.35 * consc_score_stats[0]) + (0.34 * consc_emotion_score[0]) + (
                    0.31 * consci_word_score[0])) * 100
        openScore = ((0.35 * open_score_stats[0]) + (0.34 * open_emotion_score[0]) + (0.31 * open_word_score[0])) * 100
        print('Final Score EXTRO ', extrovScore, '%')
        print('Final Score NEURO ', neuroScore, '%')
        print('Final Score AGREE ', agreeScore, '%')
        print('Final Score CONSC ', conscScore, '%')
        print('Final Score OPEN ', openScore, '%')
        stweet = ''
        return extrovScore, neuroScore, agreeScore, conscScore, openScore, facetList