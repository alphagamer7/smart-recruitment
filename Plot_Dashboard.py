import jsonlines
import pandas as pd

class Dashboard:

    def plot_graph_view(self,extrovScore, neuroScore, agreeScore, conscScore, openScore, facetList,username,count):
        import matplotlib.pyplot as plt
        labels = 'Extraversion', 'Neuroticism', 'Agreeable', 'Conscientious', 'Open'
        sizes = [72, 72, 72, 72, 72]
        sizes[0] = sizes[0] * (extrovScore / 100)
        sizes[1] = sizes[1] * (neuroScore / 100)
        sizes[2] = sizes[2] * (agreeScore / 100)
        sizes[3] = sizes[3] * (conscScore / 100)
        sizes[4] = sizes[4] * (openScore / 100)
        colors = ['navajowhite', 'green', 'lightgreen', 'orange', 'lightskyblue']
        explode = (0, 0, 0, 0, 0)  # explode a slice if required

        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True)

        # draw a circle at the center of pie to make it look like a donut
        centre_circle = plt.Circle((0, 0), 0.75, color='black', fc='white', linewidth=1.25)
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        fig.suptitle('Personality Scores', fontsize=20)
        fig.savefig('static/Visual/graph.png')
        plt.axis('equal')
        fig.clf()
        plt.close()

        print('Came to this function:')
        import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots()
        ax.axis('equal')
        width = 0.3

        cm = plt.get_cmap("tab20b")
        cout = cm(np.arange(5) * 4)
        sizes = [72, 72, 72, 72, 72]

        sizes[0] = sizes[0] * (openScore / 100)
        sizes[1] = sizes[1] * (conscScore / 100)
        sizes[2] = sizes[2] * (extrovScore / 100)
        sizes[3] = sizes[3] * (agreeScore / 100)
        sizes[4] = sizes[4] * (neuroScore / 100)

        ftotal=sizes[0]+sizes[1]+sizes[2]+sizes[3]+sizes[4]

        openS =  sizes[0] / ftotal * 100
        conscS = sizes[1] / ftotal * 100
        extroS = sizes[2] / ftotal * 100
        agreeS = sizes[3] / ftotal * 100
        neuroS = sizes[4] / ftotal * 100

        print("SIZE", sizes)

        oTotal = facetList[0][0] + facetList[0][1] + facetList[0][2]
        cTotal = facetList[1][0] + facetList[1][1] + facetList[1][2]
        eTotal = facetList[2][0] + facetList[2][1] + facetList[2][2]
        aTotal = facetList[3][0] + facetList[3][1] + facetList[3][2]
        nTotal = facetList[4][0] + facetList[4][1] + facetList[4][2]

        print('totals ',oTotal,' ',cTotal,' ',eTotal,' ',aTotal,' ',nTotal)


        # Code for d3
        import json

        s='Emotionality '+str(int(sizes[0] * (facetList[0][0])))+'%'
        print('Test is ',s)

        j = {
            "id": "TOPICS", "children": [{
                "id": "Open "+str(int(openS))+'%',
                "children": [{"id": 'Emotion '+str(int(sizes[0] * (facetList[0][0]) / oTotal))+'%', "size": sizes[0] * (facetList[0][0]) / oTotal, "rank": 1},
                             {"id": "Intellect "+str(int(sizes[0] * (facetList[0][1]) / oTotal))+'%', "size": sizes[0] * (facetList[0][1]) / oTotal, "rank": 1},
                             {"id": "Liberal "+str(int(sizes[0] * (facetList[0][2]) / oTotal))+'%', "size": sizes[0] * (facetList[0][2]) / oTotal, "rank": 1}]
            }, {
                "id": "Conscientious "+str(int(conscS))+'%',
                "children": [{"id": "Dutiful "+str(int(sizes[1] * (facetList[1][0]) / cTotal))+'%', "size": sizes[1] * (facetList[1][0]) / cTotal, "rank": 1},
                             {"id": "Order "+str(int(sizes[1] * (facetList[1][1]) / cTotal))+'%', "size": sizes[1] * (facetList[1][1]) / cTotal, "rank": 1}, {
                                 "id": "Self Discipline "+str(int(sizes[1] * (facetList[1][2]) / cTotal))+'%', "size": sizes[1] * (facetList[1][2]) / cTotal, "rank": 1}]
            }, {
                "id": "Extraversion "+str(int(extroS))+'%',
                "children": [{"id": "Excitement Seeking " +str(int(sizes[2] * (facetList[2][0]) / eTotal))+'%', "size": sizes[2] * (facetList[2][0]) / eTotal, "rank": 1},
                             {"id": "Friend "+str(int(sizes[2] * (facetList[2][1]) / eTotal))+'%', "size": sizes[2] * (facetList[2][1]) / eTotal, "rank": 1},
                             {"id": "Gregarious "+str(int(sizes[2] * (facetList[2][2]) / eTotal))+'%', "size": sizes[2] * (facetList[2][2]) / eTotal, "rank": 1}]
            }, {
                "id": "Neuroticism "+str(int(neuroS))+'%',
                "children": [{"id": "Anger "+str(int(sizes[4] * (facetList[4][0]) / nTotal))+'%', "size": sizes[4] * (facetList[4][0]) / nTotal, "rank": 6},
                             {"id": "Depression "+str(int(sizes[4] * (facetList[4][1]) / nTotal))+'%', "size": sizes[4] * (facetList[4][1]) / nTotal, "rank": 6},
                             {"id": "Vulnerability "+str(int(sizes[4] * (facetList[4][2]) / nTotal))+'%', "size": sizes[4] * (facetList[4][2]) / nTotal, "rank": 6}]
            }, {
                "id": "Agreeable "+str(int(agreeS))+'%',
                "children": [{"id": "Cooperation "+str(int(sizes[3] * (facetList[3][0]) / aTotal))+'%', "size": sizes[3] * (facetList[3][0]) / aTotal, "rank": 6},
                             {"id": "Morality "+str(int(sizes[3] * (facetList[3][1]) / aTotal))+'%', "size": sizes[3] * (facetList[3][1]) / aTotal, "rank": 6},
                             {"id": "Trust "+str(int(sizes[3] * (facetList[3][2]) / aTotal))+'%', "size": sizes[3] * (facetList[3][2]) / aTotal, "rank": 6}]
            }]
        }
        facetlog={
            "id": "TOPICS", "children": [{
                "id": "Open ",
                "facet": [{"id": 'Emotionality', "size": sizes[0] * (facetList[0][0]) / oTotal},
                             {"id": "Intellect", "size": sizes[0] * (facetList[0][1]) / oTotal},
                             {"id": "Liberalism", "size": sizes[0] * (facetList[0][2]) / oTotal}]
            }, {
                "id": "Conscientious",
                "facet": [{"id": "Dutifulness", "size": sizes[1] * (facetList[1][0]) / cTotal},
                             {"id": "Orderliness", "size": sizes[1] * (facetList[1][1]) / cTotal}, {
                                 "id": "Self Discipline", "size": sizes[1] * (facetList[1][2]) / cTotal}]
            }, {
                "id": "Extraversion",
                "facet": [{"id": "Excitement Seeking", "size": sizes[2] * (facetList[2][0]) / eTotal},
                             {"id": "Friendliness", "size": sizes[2] * (facetList[2][1]) / eTotal},
                             {"id": "Gregariousness", "size": sizes[2] * (facetList[2][2]) / eTotal}]
            }, {
                "id": "Neuroticism",
                "facet": [{"id": "Anger", "size": sizes[4] * (facetList[4][0]) / nTotal},
                             {"id": "Depression", "size": sizes[4] * (facetList[4][1]) / nTotal},
                             {"id": "Vulnerability", "size": sizes[4] * (facetList[4][2]) / nTotal}]
            }, {
                "id": "Agreeable",
                "facet": [{"id": "Cooperation", "size": sizes[3] * (facetList[3][0]) / aTotal},
                             {"id": "Morality", "size": sizes[3] * (facetList[3][1]) / aTotal},
                             {"id": "Trust", "size": sizes[3] * (facetList[3][2]) / aTotal}]
            }]
        }

        with open('static/data-intermediate.json', 'w') as outfile:
            json.dump(j, outfile)

        logs = {"username": username, "count": count,
                "Scores": {"extroS": int(extroS), "neuroS": int(neuroS), "agreeS": int(agreeS), "conscS": int(conscS),
                           "openS": int(openS),
                           "Emotionality": sizes[0] * (facetList[0][0]) / oTotal,
                           "Intellect": sizes[0] * (facetList[0][1]) / oTotal,
                           "Liberalism": sizes[0] * (facetList[0][2]) / oTotal,
                           "Dutifulness": sizes[1] * (facetList[1][0]) / cTotal,
                           "Orderliness": sizes[1] * (facetList[1][1]) / cTotal,
                           "Self Discipline": sizes[1] * (facetList[1][2]) / cTotal,
                           "Excitement Seeking": sizes[2] * (facetList[2][0]) / eTotal,
                           "Friendliness": sizes[2] * (facetList[2][1]) / eTotal,
                           "Gregariousness": sizes[2] * (facetList[2][2]) / eTotal,
                            "Anger": sizes[4] * (facetList[4][0]) / nTotal,
                            "Depression": sizes[4] * (facetList[4][1]) / nTotal,
                            "Vulnerability": sizes[4] * (facetList[4][2]) / nTotal,
                            "Cooperation": sizes[3] * (facetList[3][0]) / aTotal,
                            "Morality": sizes[3] * (facetList[3][1]) / aTotal,
                            "Trust": sizes[3] * (facetList[3][2]) / aTotal
                           }}
        import json
        with open('static/logfile.jsonl', 'a') as outfile:
            outfile.write("{}\n".format(json.dumps(logs)))


    def compare_results(self):
        result_log = []
        scores = []
        with jsonlines.open('static/logfile.jsonl') as reader:
            for obj in reader:
                result_log.append(obj)
                scores.append(obj['Scores'])
        resDF = pd.DataFrame(result_log)
        scoresDF = pd.DataFrame(scores)
        df = pd.concat([resDF, scoresDF], axis=1)
        df = df.drop_duplicates('username')
        import matplotlib.pyplot as plt
        # opennness
        ax = df[['username', 'openS']].plot(x='username', y='openS',color='yellow', kind='barh', legend=False,
                                            figsize=(25, 14), fontsize=22)

        ax.set_xlabel("openS", fontsize=25)
        ax.set_ylabel("username", fontsize=25)
        plt.title('Openness Comparision' ,fontsize=40)
        plt.savefig('static/Visual/OpennessCompare.png')
        plt.clf()
        plt.close()


        # agreeableness
        ax = df[['username', 'agreeS']].plot(x='username', y='agreeS', kind='barh', legend=False,
                                             figsize=(25, 14), fontsize=22)
        ax.set_xlabel("agreeS", fontsize=25)
        ax.set_ylabel("username", fontsize=25)
        plt.title('Agreeableness Comparision', fontsize=40)
        plt.savefig('static/Visual/AgreeablenessCompare.png')
        plt.clf()
        plt.close()
        # conscS
        ax = df[['username', 'conscS']].plot(x='username', y='conscS',color='red', kind='barh', legend=False,
                                             figsize=(25, 14), fontsize=22)
        ax.set_xlabel("conscS", fontsize=25)
        ax.set_ylabel("username", fontsize=25)
        plt.title('Conscientious Comparision', fontsize=40)
        plt.savefig('static/Visual/ConscientiousCompare.png')
        plt.clf()
        plt.close()
        # neuro
        ax = df[['username', 'neuroS']].plot(x='username', y='neuroS',color='green', kind='barh', legend=False,
                                             figsize=(25, 14), fontsize=22)
        ax.set_xlabel("neuroS", fontsize=25)
        ax.set_ylabel("username", fontsize=25)
        plt.title('Neuroticism Comparision', fontsize=40)
        plt.savefig('static/Visual/NeuroticismCompare.png')
        plt.clf()
        plt.close()
        # extraversion
        ax = df[['username', 'extroS']].plot(x='username', y='extroS',color='violet', kind='barh', legend=False,
                                             figsize=(25, 14), fontsize=22)
        ax.set_xlabel("extroS", fontsize=25)
        ax.set_ylabel("username", fontsize=25)
        plt.title('Extraversion Comparision', fontsize=40)
        plt.savefig('static/Visual/ExtraversionCompare.png')
        plt.clf()
        plt.close()