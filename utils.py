import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "moviekey.json"

import tmdbsimple as tmdb
from tmdbv3api import TMDb
tmdb2 = TMDb()
tmdb2.api_key = '1422b384f2b0eda87bcf3ceecc6d0df7'
tmdb.API_KEY = '1422b384f2b0eda87bcf3ceecc6d0df7'
from tmdbv3api import Movie

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "moviebot-ncnstc"

from gnewsclient import gnewsclient
from apiuse import upload


client = gnewsclient.NewsClient()

def get_news(parameters):
    client.topic = parameters.get('news_type')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country-code')
    return client.get_news()

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    print("############################",response.parameters)

    if response.intent.display_name == 'get_overview':
        movie_info = get_info(response.parameters)
        if dict(response.parameters)['get_money'] != '':
            cost_info = get_cost(response.parameters)
            return "*Production Cost :* " + cost_info
        if len(dict(response.parameters).get('get_fav')) > 0 :
            upload(msg, session_id,movie_info,True)
        else:
            upload(msg,session_id,movie_info)
        return str(movie_info)

    elif response.intent.display_name == 'get_news':
        news = get_news(dict(response.parameters))
        news_str = 'Here is your news : '
        for row in news:
            news_str += "\n\n{}\n\n{}".format(row['title'],row['link'])
        print(news_str)
        return str(news_str)[:400]
    
    elif response.intent.display_name == 'get_recommendation':
        recc = get_recommend(response.parameters)
        return recc

    else:
        return response.fulfillment_text

def get_cost(parameters):
    print("####get cost function chala")
    search = tmdb.Search()
    response = search.movie(query=parameters['movie_name'])
    idd = response['results'][0]['id']
    supremacy = tmdb.Movies(idd)
    supremacy.info()
    return str(supremacy.budget)

def get_info(parameters):
    search = tmdb.Search()
    
    response = search.movie(query=parameters['movie_name'])
    ans = str("Title : {}\n Release date : {} \nOverview : {} \nPopularity : {}".format(response['results'][0]['title'],response['results'][0]['release_date']
                    ,response['results'][0]['overview'],response['results'][0]['popularity']))
    return ans

def get_recommend(parameters):
    movie = Movie()
    search = tmdb.Search()
    response = search.movie(query=parameters['movie_name'])
    idd = response['results'][0]['id']
    recommendations = movie.recommendations(idd)
    ans = ''
    for recommendation in recommendations:
        ans += (recommendation.title+"\n")
    return ans