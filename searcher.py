from data_pipe import data_structures as DS
from data_pipe import fetcher as live_dp
from data_pipe import ES as es_dp
import calculations as calc
import time # to simulate a real time data, time loop 
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import json
import math


from data_pipe import utils as u

def get_search_settings():

     try:

          search_settings_cache = "live_search_UID_timestamp.json"

          # using default 
          # 
          default_data_source = DS.data_source() # keeping defaults

          fp = open(search_settings_cache)

          stored_search_settings = json.load(fp)

          ss = DS.search_filters()

          ss.__dict__.update(stored_search_settings)


          return default_data_source, ss
     except:
          return False
     

def start_fresh():

     # TODO
     # remove caches related to previous search


     # delete KPIs
     searched_kpis_instance_cache = "saved_kpis.json"

     # delete search settings 
     search_settings_cache = "live_search_UID_timestamp.json"

     return


def get_search_kpis():

     try:

          search_kpis_cache = "saved_kpis.json"

          # using default 
          # 
          default_data_source = DS.data_source() # keeping defaults

          fp = open(search_kpis_cache)

          stored_kpis = json.load(fp)

          ss = DS.searched_kpis()

          ss.__dict__.update(stored_kpis)


          return ss
     except:
          return False



def search_pipe(search_query,start_date,end_date,language,country,source_choice,keyword_in_title_include_exclude,keyword_in_title,no_opinions,non_news,no_press_release, with_less_reach,keyword_in_text,keyword_in_text_range,search_type, intitated_from_page,userID, searchID,lightMode=False):


     # print("custom_start_date=",start_date)
     if not (len(search_query)): 

          search_query = '*' # create an open search with dates



# initialize       
#  
     total_articles = 0

     mergedArticles = pd.DataFrame()

     # create empty files


     mergedArticles.to_csv("./mergedArticles_with_syndication.csv",sep=',',encoding='utf-8-sig')
     mergedArticles.to_csv("./mergedArticles.csv",sep=',',encoding='utf-8-sig')

     # SUmit is changing here
     # df,all_listing_done,final_all_indexing,all_details=final_dataframe_with_unique_and_grouping(df)

     # initialize the values 

     live_articles_df = pd.DataFrame()

     mergedArticles_binary = pd.DataFrame()

     counts_df = pd.DataFrame()

     es_articles_df = pd.DataFrame()

     num_live_records_found = 0

     num_es_records_found = 0

     hybrid = 0



                                             # search_query,custom_start_date,custom_end_date,language_options,location_options,sources_selected,keyword_in_title_include_exclude=None,keyword_in_title=[],no_opinions=False,non_news=False,no_press_release=False, with_less_reach,search_type = "simple_search", intitated_from_page = "",userID="123", searchID = "XX", hybrid=hybrid, lightMode=False


                                             # search_query,custom_start_date,custom_end_date,language_options,location_options,sources_selected,keyword_in_title_include_exclude=None,keyword_in_title=[],no_opinions=False,non_news=False,no_press_release=False, with_less_reach,search_type = "simple_search", intitated_from_page = "",userID="123", searchID = "XX", hybrid=hybrid, lightMode=False
     search_settings = DS.search_api_inputs(searchQuery = search_query, start_date = str(start_date), end_date = str(end_date),lang_list=language,loc_list=country,sources_pref=source_choice,keyword_in_title_include_exclude=keyword_in_title_include_exclude,keyword_in_title = keyword_in_title, no_opinions = no_opinions, non_news=non_news,no_press_release=no_press_release, search_type=search_type,with_less_reach=with_less_reach, intitated_from_page = intitated_from_page,userID = userID, searchID=searchID)


     search_settings.start_date = start_date

     search_settings.end_date = end_date


     live_search_settings = DS.search_api_inputs(searchQuery = search_query, start_date = str(start_date), end_date = str(end_date),lang_list=language,loc_list=country,sources_pref=source_choice,keyword_in_title_include_exclude=keyword_in_title_include_exclude,keyword_in_title = keyword_in_title,no_opinions = no_opinions, non_news=non_news,no_press_release=no_press_release, search_type=search_type,with_less_reach=with_less_reach)

     es_search_settings = DS.search_api_inputs(searchQuery = search_query, start_date = str(start_date), end_date = str(end_date),lang_list=language,loc_list=country,sources_pref=source_choice,keyword_in_title_include_exclude=keyword_in_title_include_exclude,keyword_in_title = keyword_in_title,no_opinions = no_opinions, non_news=non_news,no_press_release=no_press_release, search_type=search_type,with_less_reach=with_less_reach)


     # print("search type", search_settings.search_type )

     # print("keyword_in_title_include_exclude", search_settings.keyword_in_title_include_exclude )

     # print("keyword_in_title", search_settings.keyword_in_title )
     search_settings_dict = search_settings.__dict__ # store newly initialized search

     search_settings_cache = "live_search_UID_timestamp.json"
     
     with open(search_settings_cache, 'w') as fp:
          json.dump(search_settings_dict, fp,indent=4)

     # print("search start ", search_settings.start_date)
     # print("search end ", search_settings.end_date)

     # create a copy for live and one for ES 



     # print("#########search settings##############################")

     # print(search_settings)

     # print("#######################################")



     # print(f"ES data available till {search_settings.prestored_end_date}")

     begin_response = time.time()


     if not lightMode: # new search, not an ongoing search

          default_data_source = DS.data_source() # keeping defaults

          # next day from ES prestored 
          nextday = dt.strptime(search_settings.prestored_end_date, '%Y-%m-%d') + timedelta(days=1)

          # print("nextday = ", nextday)

       
          if hybrid:
               
          # fetch data from ES



               # print("~~~~~~~~~~~~fetch data from ES------------------------")


               # search till the date data is available in ES

               # es_search_settings.start_date = start_date

               actual_search_end_date_obj = dt.strptime(search_settings.end_date, '%Y-%m-%d')

               es_prestored_end_date_obj = dt.strptime(es_search_settings.prestored_end_date, '%Y-%m-%d')
               
               

               if actual_search_end_date_obj > es_prestored_end_date_obj: # if limited data is available
                    es_search_settings.end_date = es_search_settings.prestored_end_date


               # print(" ES search start ", es_search_settings.start_date)
               # print("ES search end ", es_search_settings.end_date)

               num_es_records_found, es_articles_df = es_dp.get_articles_ES(es_search_settings,[default_data_source])

               # print("FROM ES")
               # print(es_articles_df.head())

 


               



          # fetch live data from where ES has ended



          if (len(es_articles_df) > 1):

               live_search_settings.start_date = str(nextday.date())

               # print(f"modified ----------{live_search_settings.start_date}")

          # end date as is 
          live_search_settings.end_date = end_date

          # print(" LIVE search start ", live_search_settings.start_date)
          # print("LIVE search end ", live_search_settings.end_date)



          # call live only if valid dates i.e. remaining timeframe

          live_start_date_obj = dt.strptime(live_search_settings.start_date, '%Y-%m-%d')

          live_end_date_obj = dt.strptime(live_search_settings.end_date, '%Y-%m-%d')

          actual_search_end_date_obj = dt.strptime(search_settings.end_date, '%Y-%m-%d')

          # is it required to go live - if it is not already covered by ES

          if actual_search_end_date_obj > live_start_date_obj:

               if live_end_date_obj > live_start_date_obj : 

                    res = live_dp.get_articles_live(live_search_settings,[default_data_source],lightMode=lightMode)


                    if(res):
                         num_live_records_found, live_articles_df = res

                         # print("LIVE cols")

                         # print(live_articles_df.columns)


                         # print(live_articles_df.head())


          # combine es and live dataframes
          mergedArticles = pd.concat([es_articles_df,live_articles_df])
          print(f"Hey Sumit, we have {len(mergedArticles)} articles before applying syndication.")
          mergedArticles,all_listing_done,final_all_indexing,all_details=calc.final_dataframe_with_unique_and_grouping(mergedArticles) #changed to incorporate syndication. 30/06/2023
          # we need to save the data here.
          print(f"Hey Sumit, we have {len(mergedArticles)} articles after applying syndication.")
          # mergedArticles['Syndication'] = mergedArticles['Syndication'].apply(lambda x: str(x))
          # print(mergedArticles['Syndication'])
          total_articles= num_live_records_found + num_es_records_found

          if not total_articles and mergedArticles.empty:
               return (total_articles,mergedArticles)




          # print("---------")
          if not mergedArticles.empty:

               # store raw data without removing duplicates - for syndication function - another dataframe

               # print("Here, I am at line 286")
               # print(mergedArticles['Syndication'])
 
               mergedArticles.to_csv("./mergedArticles_with_syndication.csv",sep=',',encoding='utf-8-sig')
 

               
               # clean it, check formats, remove duplicates

               mergedArticles['Syndication'] = mergedArticles['Syndication'].astype(str)

               # mergedArticles['pubDate'] = mergedArticles['pubDate'].apply(calc.check_date_format)
               
               # mergedArticles['title'] = mergedArticles['title'].apply(u.get_clean_text)

               # only considering content and summary as advised by business 
               mergedArticles['display_content'] = mergedArticles[['content','summary']].agg(' '.join, axis=1)
               
               # mergedArticles['display_content'] = mergedArticles['display_content'].apply(u.get_clean_text)

               # mergedArticles['display_content'] = mergedArticles['display_content'].fillna(value="No description available.")

               # mergedArticles = mergedArticles[mergedArticles['reprint']==False]
          


               # remove incorrect dates
               # print("Here, I am at line 313")
               # print(mergedArticles['Syndication'])

               # mergedArticles.dropna(subset=['pubDate'], inplace=True)

               # print("Here, I am at line 318")
               # print(mergedArticles['Syndication'])

               # These below lines are commented here. Sumit. dated 05-07-2023

               # # basic duplicates removal
               # mergedArticles.drop_duplicates(subset=['articleId'], inplace=True)
               # # if all fields are same, only then remove other wise keep for syndication
               # mergedArticles.drop_duplicates(subset=['title', 'author', 'source'], inplace=True)


               # # remove redundant items with same content before sending to front end

               # mergedArticles.drop_duplicates(subset=['title'], inplace=True)

               # mergedArticles.drop_duplicates(subset=['display_content'], inplace=True)

               ## fuzzy logic can be added for similar titles or texts deduplication where there are minor words additions 

               # print("Here, I am at line 335")
               # print(mergedArticles['Syndication'])


               ##### end of ADVANCE SEARCH - lower priority websites filter i.e. with less reach

               #### ADVANCE SEARCH FILTERING -  keyword prominance / exclude - include in title

               if search_settings.search_type=='advance_search':

    

                    if len(search_settings.keyword_in_title[0]): # if it is not an empty list

                         matched_articles_list = calc.find_keyword_in_title(mergedArticles['title'],keyword_in_title)

                         mergedArticles['found_in_title'] = matched_articles_list

                         total_matched_articles_keyword_by_title = int(mergedArticles['found_in_title'].sum())

                         base_l = len(mergedArticles)
                         # print("earlier total articles = ", total_articles)
                         # print("base_l=",base_l)

                         if search_settings.keyword_in_title_include_exclude == 'include':

                              mergedArticles = mergedArticles[mergedArticles['found_in_title']==True]
                              l1 = len(mergedArticles)
                              p1 = l1/base_l
                              # print("l1=",l1)
                              # print("p=",p1)
                              total_articles = math.floor(p1*total_articles)
                              # print("new total", total_articles)

                              
                         
                         else:
                              mergedArticles = mergedArticles[mergedArticles['found_in_title']==False]
                              l2 = len(mergedArticles)
                              p2 = l2/base_l
                              # print("l2=",l2)
                              # print("p2=",p2)
                              total_articles = math.ceil(p2*total_articles)

                              # print("new total", total_articles)

                              # total_articles = total_articles - total_matched_articles_keyword_by_title


                              
                         
                         # drop the found in title column
                         try:
                              mergedArticles.drop(columns=['found_in_title'],inplace=True)
                         except:
                              pass



               


               #### ADVANCE SEARCH FILTERING -  keyword prominance / keyword in article title and text range
                    # print("keyword_in_text=",keyword_in_text)
                    if len(keyword_in_text[0]):
                         mergedArticles['short_content'] = [a[:keyword_in_text_range] for a in mergedArticles['display_content']]
                         mergedArticles['find_keyword_in_text'] = mergedArticles['short_content'].str.contains(keyword_in_text[0])
                         matches_in_range = int(mergedArticles['find_keyword_in_text'].sum())
                         total_articles = matches_in_range
                         mergedArticles = mergedArticles[mergedArticles['find_keyword_in_text']==True]


               



               #### END OF ADVANCE SEARCH FILTERING -  keyword prominance / keyword in article title and text range




               # extract author names 

               mergedArticles['author'] = mergedArticles['author'].apply(calc.extract_person_names)

               mergedArticles['matchedKeywords'] = mergedArticles['title'].apply(calc.get_matchedKeywords)

               mergedArticles['reach'] = mergedArticles['source'].apply(calc.get_reach_value)

               mergedArticles['AVE'] = mergedArticles['reach']* 0.025 * 0.37


               ##### ADVANCE SEARCH - lower priority websites filter i.e. with less reach

               # print(">>>>>>>>>>with_less_reach=",with_less_reach)

               if search_settings.with_less_reach: # if this filter is requested by the user

                    # print("Filter on lesser reach aaplied")

                    n_removed_with_lesser_reach = len(mergedArticles[mergedArticles['reach'] < 5000.0]) # threshould as given by business 

                    total_articles = total_articles - n_removed_with_lesser_reach

                    mergedArticles = mergedArticles[mergedArticles['reach'] >= 5000.0]
                    # reduce the total number by records filtered 
                    total_articles = len(mergedArticles)
                   





               # mergedArticles['articleReach'] = mergedArticles['source'].apply(calc.get_reach_value)

               # mergedArticles['articleAVE'] = mergedArticles['articleReach'] * 0.025 * 0.37 # the factor for AVE

               # mergedArticles = calc.get_syndication_uniques(mergedArticles)

               
               # try: 
               #      mergedArticles['articleSentiment'] = calc.get_sentiment_from_data(mergedArticles[['sentiment.positive', 'sentiment.negative', 'sentiment.neutral']])
               #      mergedArticles['articleSentiment'] = mergedArticles['articleSentiment'].fillna('NEU')
               # except: # by default dummy entries      
               #      mergedArticles['articleSentiment'] = ['NEU']*len(mergedArticles)

               mergedArticles=calc.sentiment_with_spacy_summarization_on_dataframe(mergedArticles)

               # mergedArticles['articleSentiment'] = mergedArticles['title'].apply(calc.custom_sentiment)
               # mergedArticles['articleSentiment'] = mergedArticles['title'].apply(calc.sentiment_light)

               
               # mergedArticles['articleSentiment'] = mergedArticles['title'].apply(calc.agg_sentiment)







               # sort by latest
               if not mergedArticles.empty : 

                    # mergedArticles = mergedArticles.sort_values(by = ['pubDate'], ascending=False)

                    # store it for later use
                    # print("Here, I am at line 480")
                    # print(mergedArticles['Syndication'])
 
                    mergedArticles.to_csv('mergedArticles.csv',sep=',',encoding='utf-8-sig')

                    # print("Here, I am at line 486")
                    # print(mergedArticles['Syndication'])


                    # print(mergedArticles[['title', 'display_content', 'pubDate', 'source', 'author', 'matchedKeywords', 'articleSentiment', 'reach','AVE']].to_dict('records'))

               end_response = time.time()
               total_time_taken = end_response-begin_response

               # print(f"data fetch total time taken {total_time_taken}")

               
               # save the kpis
               searched_kpis_instance = DS.searched_kpis(searchID=searchID,total_articles=total_articles) # other entries to be populated once ready

              

               searched_kpis_instance_dict = searched_kpis_instance.__dict__ # store newly initialized search kpis

               

               searched_kpis_instance_cache = "saved_kpis.json"
          
               with open(searched_kpis_instance_cache, 'w') as fp:
                    json.dump(searched_kpis_instance_dict, fp,indent=4)





     else:
          
          mergedArticles = pd.read_csv('./mergedArticles.csv')

          # print("Here, I am at line 520")
          # print(mergedArticles['Syndication'])
          print(len(mergedArticles))
          
          stored_kpis = get_search_kpis()

          total_articles = stored_kpis.total_articles

     # print("Line number 528")
     # print(type(total_articles))

     # return (total_articles, mergedArticles)
     return (len(mergedArticles), mergedArticles)
          

