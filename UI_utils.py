from collections import Counter
import string
import pandas as pd
from datetime import datetime, timedelta
import json
import requests
import plotly.express as px # interactive charts 
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# from wordcloud import WordCloud

# Getting the credentials from the es_config file
# import configparser
import pickle





def get_sources_list():

     topsourcesreachwise = []

     try:

          reach_map = pickle.load(open("./data_pipe/reach.pkl", "rb"))

          # print("key------------")

          # print(reach_map.keys())

          source_reachwise = sorted(reach_map['current_month_reach'].items(), key=lambda x:x[1], reverse=True)

          topsourcesreachwise = tuple(source_reachwise)[:10]
          
          topsourcesreachwisenames = [i[0] for i in topsourcesreachwise]

          # print(reach_map['current_month_reach'].keys())
          # print("--------source_reachwise-------")

          # print(topsourcesreachwisenames)

 

          
     except:
          pass
     
     return topsourcesreachwisenames


def results_over_time_graph(daily_agg_counts):

     # print(daily_agg_counts.head())
     fig = False
     try:
          fig = px.line(data_frame=daily_agg_counts,x=daily_agg_counts.index,y='mentionCounts')
     except:
          pass

     return fig


def get_word_cloud_graph(AMXOneD_object):
     
     


     fig = False

     df = pd.DataFrame.from_records(AMXOneD_object['data'])

     
     # try:
     fig = plt.figure( figsize=(15,10))

     wordcloud = WordCloud()

     # fig = wordcloud.generate_from_frequencies(frequencies=df)

     d = {}
     for r in df.iterrows():
          d[r[0]] = r[1]
     
     # print("##########################")

     # print(d)
     # d = {'google' : 0.5, 'microsoft' : 01}
     wordcloud = WordCloud()
     fig = wordcloud.generate_from_frequencies(frequencies=d)
     plt.figure()
     plt.imshow(wordcloud, interpolation="bilinear")
     plt.axis("off")
     plt.show()



     # except:
          # pass

     return fig

def get_media_type_graph(AMXOneD_object):



     fig = False

     df = pd.DataFrame.from_records(AMXOneD_object['data'])

     
     try:
          fig = px.pie(df, values='value', names='label', title=AMXOneD_object['title'])
     except:
          pass

     return fig

def get_reach_over_time_graph(df):

     fig = False
     # try:
     fig = px.line(data_frame=df,x='pubDate',y='reach')
     # except:
     #      pass

     return fig


def get_sentiment_over_time_graph(df):

     fig = False
     # try:
     fig = px.line(data_frame=df,x='pubDate',y=['sentimentType_POS','sentimentType_NEG','sentimentType_NEU'])
     # except:
     #      pass

     return fig