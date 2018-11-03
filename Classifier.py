from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import pandas as pd
import numpy as np
import pickle


class Classifier:
    def semantic_classification(self, x, y, classify_name, tweet):
        vect = pickle.load(open('pretrained/'+classify_name+'vect.pkl', "rb"))
        filename = 'pretrained/' + classify_name + 'finalized_model.sav'
        loaded_model = joblib.load(filename)
        return loaded_model.predict(vect.transform([tweet]))

    def emotion_analysis_text(self, df, trait, list_emotions):
        from pre_trained_dataset import send_train_set, send_sentiment_set
        emotionSet = send_train_set()
        emotionDF = pd.DataFrame(emotionSet)
        sentiments = send_sentiment_set()
        emotionDF['Sentiment'] = sentiments
        emotionDF[trait + '_Score'] = np.where(df[trait] > 0.1, 1, 0)

        train_emotions = emotionDF.iloc[0:, 0:-1]
        train_label = emotionDF.iloc[train_emotions.index, -1]

        from sklearn import svm

        X_train, X_test, y0_train, y0_test = train_test_split(train_emotions, train_label, test_size=0.15,
                                                               random_state=42)
        #
        clf = svm.SVC()
        #
        clf.fit(X_train, y0_train)

        predict_emotion = np.array([list_emotions])
        predict_emotion = predict_emotion.reshape(len(predict_emotion), -1)
        prediction_emotion = clf.predict(predict_emotion)
        pred_score = prediction_emotion
        return pred_score

    def cal_stat_personality(self, df, trait, c_user_mentions_pred, c_url_pred, c_Hash_pred, c_rt_pred, c_exclam_pred,
                             c_question_pred):
        Y = pd.DataFrame()
        Y[trait + '_Score'] = np.where(df[trait] > 0.1, 1, 0)
        trainingData = df[
            ["Normalised User Mentions", "Normalised No Of URLS", "Normalised Hashtags", "Normalised Retweets",
             "Normalised Exclamations", "Normalised Question Marks"]].copy()
        trainingData[trait + '_Score'] = Y[trait + '_Score']

        from sklearn.model_selection import train_test_split

        train, test = train_test_split(trainingData, test_size=0.15, random_state=42)

        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=5, max_leaf_nodes=10)
        clf = clf.fit(train[["Normalised User Mentions", "Normalised No Of URLS", "Normalised Hashtags",
                             "Normalised Retweets", "Normalised Exclamations", "Normalised Question Marks"]],
                      train[trait + "_Score"])

        stat_predict = clf.predict(
            [[c_user_mentions_pred, c_url_pred, c_Hash_pred, c_rt_pred, c_exclam_pred, c_question_pred]])
        return stat_predict
