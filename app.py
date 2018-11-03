import requests
from flask import Flask, render_template, url_for, request, redirect

from tweepy import error
from collect_data import collect_data
from personality_recog import get_tweets
from Plot_Dashboard import Dashboard
from Profile import Profile
from ml_facade import ML_Facade
from exception import APILengthError as ex

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        if request.method == "POST":
            username = request.form['url']
            collect_data(username)
            print('Done Adding Profile ')
            return redirect(url_for('add', done=True))
        return render_template('add.html')
    except error.TweepError:
        return render_template('except.html'), 500

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    try:
        if request.method == "POST":
            profile = Profile()
            profile.setusername(request.form['username'])
            print(profile.username)
            try:
                profile.setuser_profile('TwitterProfileData/timeline' + profile.username + '.jsonl')
                stweet, count ,name = get_tweets(profile.user_profile)
            except FileNotFoundError:
                print("File Not Found")
                return redirect(url_for('analyse', file_error=True))
            try:
                ex.APILengthError.test_api_error(count)
            except ex.APILengthError as e:
                return redirect(url_for('analyse', count_error=True))
                print("Test Error")
            profile.setcount(count)
            print('count ', profile.count)
            ml_facade = ML_Facade()
            extrovScore, neuroScore, agreeScore, conscScore, openScore, facetList = ml_facade.ml_process(stweet,
                                                                                                         profile.count)
            dashboard = Dashboard()
            dashboard.plot_graph_view(extrovScore, neuroScore, agreeScore, conscScore, openScore, facetList,
                                      profile.username, profile.count)
            dashboard.compare_results()
            print('Done ML ')
            return redirect(url_for('index', profile_name=profile.username, full_name=name))
        return render_template('analyse.html')
    except requests.exceptions.RequestException as e:
        return render_template('except.html'), 500

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    return render_template('compareres.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def page_not_found(e):
    print(e)
    return render_template('500.html'), 500

def log_test(username, count, extrovScore, neuroScore, agreeScore, conscScore, openScore, facetList):
    logs = {"username": username, "count": count,
            "Scores": {"extroS": extrovScore, "neuroS": neuroScore, "agreeS": agreeScore, "conscS": conscScore,
                       "openS": openScore, "FacetList": facetList}}
    import json
    with open('static/logfile.jsonl', 'a') as outfile:
        outfile.write("{}\n".format(json.dumps(logs)))

@app.route('/removelog', methods=['GET', 'POST'])
def removelog():
    with open('static/logfile.jsonl', "w"):
        pass
    return render_template('compareres.html')


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
