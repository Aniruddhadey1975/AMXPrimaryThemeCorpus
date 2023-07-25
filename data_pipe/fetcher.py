
import requests
import json
import pandas as pd
import numpy as np
import math
from data_pipe import utils as u
import time
# import urllib.parse
# import re

def get_journo_id(data_source, NAME): 

     journo_id = ''

     apiKey = data_source.attrs['api_key'].strip('\"').strip("\'")

     journo_url = data_source.attrs['journalist_url'].strip('\"').strip("\'")


     URL = f"{journo_url}?q={NAME}&apiKey={apiKey}"

     resp = requests.get(URL)

     journalists = resp.json()

     # print(journalists.keys())

     try:
          journo_id = journalists.get('results')[0]['id']
     except:
          pass


     return journo_id


def get_author_numbers(data_source,ss,journo_id):

     result_count = 0
     if (len(journo_id)):
          journalist_filter = '&journalistId=' + str(journo_id)

          # print("journalist_filter ", journalist_filter)

          result_count, _ = get_articles_live(ss,[data_source],lightMode=True, additional_filters=journalist_filter)

     return result_count

# basic preprocess
def preprocess(text):
    
    text = text.encode()

    return text

# def filter_on_title(ss):

#      additional_filters = ''

#      try:

#           if ss.keyword_in_title_include_exclude == 'include': 
#                if len(ss.keyword_in_title) >= 1:
                    

#                     for kw in ss.title_filter:
#                          additional_filters += '&title='+ kw
#                     # print(">>>>>>>>>>>>>>>>>>>>>", additional_filters)
#      except:
#           pass
     
#      return additional_filters




def filter_on_spam(ss):

     #&excludeLabel=Non-news&excludeLabel=Opinion

     additional_filters = ''

     # print("~~~~",ss.no_opinions)
     # print("~~~~",ss.non_news)
     # print("~~~~",ss.no_press_release)

     if ss.no_opinions:
          
          additional_filters += '&excludeLabel=Opinion'
          # print("additional_filters=",additional_filters)

     if ss.non_news:

          additional_filters += '&excludeLabel=Non-news'
          # print("additional_filters=",additional_filters)


     
     if ss.no_press_release:

          additional_filters += "&excludeLabel=Press Release"
          # print("additional_filters=",additional_filters)





     
     return additional_filters



def filter_on_source(ss):

     additional_filters = ''

     if len(ss.sources_pref) >= 1:
          
          for source in ss.sources_pref:
               additional_filters += '&source='+ source
               # print(">>>>>>>>>>>>>>>>>>>>>", additional_filters)
     
     return additional_filters


def get_articles_live(ss,ds_list,lightMode=False, additional_filters=''): # search settings

     counts_ts_df = pd.DataFrame()

     base_df = pd.DataFrame()

     selected_df = pd.DataFrame()

     empty_handed = True

     max_page = int(ds_list[0].attrs['max_page'])

     apiKey = ds_list[0].attrs['api_key'].strip('\"').strip("\'")

     article_url = ds_list[0].attrs['article_url'].strip('\"').strip("\'")

     batch_size = {ds_list[0].attrs['batch_size']}


     total_num_live_records_found = 0

     # filter on sources if specified

     # filter

     #initialize
     source_filter = ''
     
     try:
          source_filter = filter_on_source(ss)
     except:
          pass
     # filter on spams
     # 
     # intialize
     spam_filter = ''


     spam_filter = filter_on_spam(ss)



     # print("spam filter=",spam_filter)
## break down search query, make lower case

     # ss.searchQuery = ss.searchQuery.lower()

     search_terms = [ss.searchQuery]


         
     for search_term in search_terms:

          search_term_processed = u.process_search_term(search_term) 

          # params = {"q" : search_term}

          # encoded_params = urllib.parse.urlencode(params) # for future - complex charecters 

          # quality data with filters on paid news plus only top sources
          # url = f'{article_url}?apiKey={apiKey}&from={ss.start_date}&to={ss.end_date}&q={search_term}&country=us&sourceGroup=top100&showNumResults=true&showReprints=false&paywall=false&excludeLabel=Non-news&excludeLabel=Opinion&excludeLabel=Paid News&excludeLabel=Roundup&excludeLabel=Press Release&sortBy=date&language=en&medium=Article' + source_filter

          # all data with only language and country specification

          

          # url = f'{article_url}?apiKey={apiKey}&from={ss.start_date}&to={ss.end_date}&q={search_term}&country=us&language=en&medium=Article' + source_filter + spam_filter

          url = 'https://api.goperigon.com/v1/all?apiKey='+ apiKey +'&from='+ ss.start_date +'&to='+ ss.end_date +'&country=' + 'us' + '&showReprints=true&showNumResults='+ 'true' + '&language=' + 'en' +'&q='+ search_term_processed + source_filter + spam_filter
          
          # print("NO ARTICLES URL$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
          # print(url)
          
          # processing time 
          time.sleep(1)

          resp = requests.get(url)

          resp_json = resp.json()


          # print(resp_json.keys())

          try:
               num_live_records_found = resp_json['numResults']
               # print("numResults=",resp_json['numResults'] )
          except:
               num_live_records_found = 0



          total_num_live_records_found = num_live_records_found

          # print("**************%%-+-%%%%************************")

          batch_size = 100

          max_page = math.ceil(num_live_records_found/batch_size)

          if max_page > 10:
               max_page = 10 # fetch first 5 pages only at start for testing

          if not lightMode: # go and get articles data 
     # page wise query to api, colect data
               
               for page_num in np.arange(0,max_page,1): 

                    # print(f"-------------------------[{search_term}-{page_num}]--------------------------------------------")

                    # referring to zero-th element of source list contained in search settings
                    # url = f"https://api.goperigon.com/v1/stories/all?apiKey={apiKey}&page={page_num}&size={ds_list[0].attrs['batch_size']}&from={ss.start_date}&to={ss.end_date}&showNumResults=true&q={search_term}"
                    
                    
                    # url = f"https://api.goperigon.com/v1/stories/all?apiKey={apiKey}&page={page_num}&size={ds_list[0].attrs['batch_size']}&from={ss.start_date}&to={ss.end_date}&showNumResults=true&q={search_term}"

                    # data_url = f"https://api.goperigon.com/v1/all?apiKey={apiKey}&language=en&country=us&sourceGroup=top1000&size={ds_list[0].attrs['batch_size']}&from={ss.start_date}&to={ss.end_date}&showNumResults=true&q={search_term}&medium=Article&page={page_num}"
                    

                    data_url = 'https://api.goperigon.com/v1/all?apiKey='+ apiKey +'&from='+ ss.start_date +'&to='+ ss.end_date +'&country=' + 'us' + '&showReprints=true&showNumResults='+ 'true' + '&language=' + 'en' +'&q='+ search_term_processed + source_filter + spam_filter + "&page=" + str(page_num) + "&size=" + str(batch_size) # just need to add pagination for multiple calls 

                    # data_url = url + "&page=" + str(page_num) + "&size=" + str(batch_size) # just need to add pagination for multiple calls 
                    
                    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    # print("data = ", data_url)
                    gp_data = {}
                    
                    # to avoid back to back api calls
                    # processing time 
                    time.sleep(0.2)


                    gp_req = requests.get(data_url)

                    gp_req_json = gp_req.json()

                    # print("gp_req_json=", gp_req_json.keys())

                    extraction_key = 'results'

                    if 'articles' in gp_req_json.keys():
                         extraction_key = 'articles'


                    gp_data = gp_req_json.get(extraction_key)


                    if (not gp_data) :

                         # print("existing at", page_num)

                         break
                    
                    
                    gp_df = pd.json_normalize(gp_data)


                    # gp_df['searched_for'] = [search_term] * len(gp_df) 
                    # print("############################################")
                    # print("gp_df=", gp_df.columns)
               

                    # base_df = pd.concat([base_df,gp_df])


                    base_df = pd.concat([base_df,gp_df], ignore_index=False)

                    base_df = base_df.reindex(axis='columns')


                    # print(f"combined_dfs[{search_term}]=",combined_dfs[search_term].describe() )

                    # total_num_live_records_found += num_live_records_found

                    empty_handed = False # got some data

                    # print("base_df = ", base_df.columns)


          if (not empty_handed): # found some data



               # sort by pub date


               base_df.sort_values(by=['pubDate'], ascending=True, inplace=True)


               columns_remapping = { 'authorsByline': 'author', 'source.domain': 'source' }

               # replace commas from text to semicolon to avoid csv conflict 

               base_df['title'] = base_df['title'].str.replace(',',';')
               base_df['content'] = base_df['content'].str.replace(',',';')
               base_df['description'] = base_df['description'].str.replace(',',';')
               base_df['summary'] = base_df['summary'].str.replace(',',';')
     
               base_df = base_df.rename(columns=columns_remapping)
          
               imp_cols = ['url', 'articleId', 'country','language', 'pubDate', 'title', 'summary', 'description', 'content', 'source','sentiment.positive', 'sentiment.negative', 'sentiment.neutral', 'author', 'locations','reprint']
               

               selected_df = base_df[imp_cols]










               # process locations columns specially 

               selected_df['state'] = selected_df['locations'].apply(u.extract_state)




     return (total_num_live_records_found,selected_df) # in case of light mode the df would be empty, only record number would be available



