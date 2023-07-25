from data_pipe import data_structures as DS
from data_pipe import fetcher as live_dp
from data_pipe import ES as es_dp
import time # to simulate a real time data, time loop 
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import numpy as np
import requests
import itertools
import json
from collections import Counter
from data_pipe import utils as u
import re
import pickle
import searcher as s1
import yake
# from langdetect import detect
import spacy
nlp = spacy.load('en_core_web_sm')
import random
from numerize import numerize
import math
import Input_from_User_Primary_Theme_rev3 as Input_from_User_Primary_Theme_rev3


import pandas as pd
from get_values import get_values
from separating_the_data_frame_for_each_articles import separating_the_data_frame_for_each_articles

def final_dataframe_with_unique_and_grouping(df):


    df11=df[["title", "summary"]] #b will be post_thread_title and  c will be posts_text, a will be website

    df1 = df11[df11.duplicated(keep=False)]
    all_details = df1.groupby(list(df1)).apply(lambda x: tuple(x.index)).tolist()

    reject=[]
    all_merge=[]

    for i in range(len(all_details)):
        for j in range(1,len(all_details[i])):
            reject.append(all_details[i][j])

    for i in range(len(all_details)):
        for j in range(len(all_details[i])):
            all_merge.append(all_details[i][j])

    all_accept_among_duplicate = [elem for elem in all_merge if elem not in reject]
    all_nonduplicate = [elem for elem in list(range(len(df))) if elem not in all_merge] 

    syndication= [0]*len(df)
    for k2 in range(len(df)):
        if k2 in all_merge:
            syndication[k2]=len(get_values(all_details, k2)[0])-1
        else:
            syndication[k2] =0


    all_listing_done=all_details + all_nonduplicate
    final_all_indexing=all_accept_among_duplicate+all_nonduplicate

    df['Syndication'] = syndication
    df.drop(df.index[reject[:]], inplace=True)
    # df=df.reset_index(drop=True, inplace=True)
    df=df.reset_index(drop=True)
    return df,all_listing_done,final_all_indexing,all_details


def get_values(iterables, key_to_find):
    return list(filter(lambda x:key_to_find in x, iterables))




def get_matchedKeywords(text):

     p = u.get_search_terms_regex()

     count = 0

     try:
          count = len(re.findall(p,text))
     except:
          pass

     return count


def results_over_time():
    try:
        # Read the data
        counts_ts_df = pd.read_csv('./mergedArticles.csv', usecols=['pubDate', 'matchedKeywords'], encoding='ISO-8859-1')
        
        if counts_ts_df.empty:
            raise Exception('The mergedArticles.csv file is empty. Please run the search_pipe() function to populate the file with data.')
        
        # Data preprocessing
        counts_ts_df['pubDate'] = counts_ts_df['pubDate'].str[:19]  # Remove part after seconds: '2023-03-04T04:27:15.603343+00:00' -> '2023-03-04 04:27:15'
        counts_ts_df['pubDate'] = counts_ts_df['pubDate'].str.replace('T', ' ')  # '2023-03-04T04:27:15.603343+00:00' -> '2023-03-04 04:27:15'

        format1 = '%Y-%m-%d %H:%M:%S'

        # Filter out rows with invalid "pubDate" values
        invalid_date_indices = []
        for i, value in enumerate(counts_ts_df['pubDate']):
            try:
                pd.to_datetime(value, format=format1)
            except ValueError:
                invalid_date_indices.append(i)

        # Drop rows with invalid dates
        counts_ts_df.drop(index=invalid_date_indices, inplace=True)

        # Perform datetime conversion after filtering out invalid dates
        counts_ts_df['pubDate'] = pd.to_datetime(counts_ts_df['pubDate'], format=format1)
        counts_ts_df.set_index('pubDate', inplace=True)
        
        # Resample and interpolate
        mentions_agg_counts_smooth = counts_ts_df.resample('1h').sum()
        mentions_agg_counts_smooth['matchedKeywords'] = mentions_agg_counts_smooth['matchedKeywords'].apply(abs)
        mentions_agg_counts_smooth = mentions_agg_counts_smooth.interpolate(method='linear')
        mentions_agg_counts_smooth.rename({'matchedKeywords': 'mentionCounts'}, axis='columns', inplace=True)

        # Save to CSV (optional, remove if not needed)
        mentions_agg_counts_smooth.to_csv("mentions_agg_counts_smooth.csv")

        return mentions_agg_counts_smooth
        
    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")



def dashboard_view_top_authors():

     # default_data_source, ss = s1.get_search_settings()

     final_authors_dict = {}

     articles_df = pd.read_csv("./mergedArticles.csv", usecols=['author','reach'])

     authors_list = tuple(articles_df['author'].dropna())

     author_counter = Counter(authors_list)

     author_sorted = sorted(author_counter.items(), key=lambda x:x[1], reverse=True)

     # get 20 entries to have sufficient data
     top5authors = tuple(author_sorted)[:50]

     top5authorsDict = dict((x, int(y)) for x, y in top5authors)

     # get author reach mapping
     authors_names = list(top5authorsDict.keys())
     # print("authors_names", )
     reach_values = articles_df[articles_df['author'].isin(authors_names)]

     author_counts = [top5authorsDict[k] for k in reach_values['author']]

     reach_values['counts'] = author_counts

     reach_values.sort_values(by=['counts','reach'],inplace=True,ascending=False)
     reach_values.drop_duplicates(subset=['author'],keep='first',inplace=True)
     reach_values.drop_duplicates(subset=['counts'],keep='first',inplace=True)

     # print(reach_values)
     
     for (a,v) in reach_values[['author','counts']].values:
          final_authors_dict[a] = v

     title = "View top authors"

     plot_data = u.create1DplotData(title=title, data_dict=final_authors_dict)

     return plot_data



def dashboard_view_top_sources():

     default_data_source, ss = s1.get_search_settings()


     articles_df = pd.read_csv("./mergedArticles.csv", usecols=['source'])

     sources_list = tuple(articles_df['source'].dropna())

     source_counter = Counter(sources_list)

     source_sorted = sorted(source_counter.items(), key=lambda x:x[1], reverse=True)

     top5sources = tuple(source_sorted)[:5]

     top5sourcesDict = dict((x, int(y)) for x, y in top5sources)

     title = "View top sources"

     plot_data = u.create1DplotData(title=title, data_dict=top5sourcesDict)

     return plot_data



def dashboard_view_geo_breakdown_us():


     default_data_states, ss = s1.get_search_settings()


     articles_df = pd.read_csv("./mergedArticles.csv", usecols=['state'])

     states_list = tuple(articles_df['state'].dropna())

     states_counter = Counter(states_list)

     states_sorted = sorted(states_counter.items(), key=lambda x:x[1], reverse=True)

     top5states = tuple(states_sorted)[:5]

     top5statesDict = dict((x, int(y)) for x, y in top5states)

     title = "View Geographic breakdown"

     plot_data = u.create1DplotData(title=title, data_dict=top5statesDict)

     return plot_data




def get_reach_value(source):

     if len(source) < 5:

          reach_value = 0
     else:

          reach_map = pickle.load(open("./data_pipe/reach.pkl", "rb"))
          try:

               reach_value = reach_map['current_month_reach'][source]
          except:
               reach_value = 0

     return reach_value



def get_top_articles_by_reach():

     display_cols = ['pubDate','title', 'author', 'reach']

     articles_df = pd.read_csv("./mergedArticles.csv", usecols=display_cols)

     articles_df = articles_df.sort_values(by=['reach'],ascending=False)

     return articles_df.head()



def get_top_articles_by_ave():

     display_cols = ['pubDate','title', 'author', 'AVE']

     articles_df = pd.read_csv("./mergedArticles.csv", usecols=display_cols)

     articles_df = articles_df.sort_values(by=['AVE'],ascending=False)

     return articles_df.head()



def get_total_sentiments():

     try:
          articles_df = pd.read_csv("./mergedArticles.csv", usecols=['articleSentiment'])

          sent_list = tuple(articles_df['articleSentiment'].dropna())

          sentiment_counter = Counter(sent_list)

          
     except:
          sentiment_counter=0
     return sentiment_counter

def get_total_ave():

     total_ave = 0
     total_ave_in_str = str(total_ave)


     try:
          articles_df = pd.read_csv("./mergedArticles.csv", usecols=['AVE'])

          total_ave = articles_df.mean()

          total_ave,total_ave_in_str = convert_to_millions_or_thousands(total_ave[0])

     except:
          pass


     return total_ave,total_ave_in_str

def get_total_reach():

     total_reach = 0
     total_reach_in_str = str(total_reach)


     try:
          articles_df = pd.read_csv("./mergedArticles.csv", usecols=['reach'])

          total_reach = articles_df.mean()

          total_reach,total_reach_in_str = convert_to_millions_or_thousands(total_reach[0])

     except:
          pass
     return total_reach,total_reach_in_str



def convert_to_millions_or_thousands(n):

     display_str = numerize.numerize(n)
  

     return n,display_str


def get_media_type():
     

     articles_df = pd.read_csv("./mergedArticles.csv", usecols=['author'])

     n_rec = len(articles_df)

     
     if n_rec < 100:

          n_rec_base = 100 # to adjust for % as asked by Rhombus

     else:
          n_rec_base = n_rec


     media_list = ["Online"] * (n_rec_base - 1)

     media_list.append("Print")# adding category 

     media_list_counter = Counter(media_list)

     media_list_sorted = sorted(media_list_counter.items(), key=lambda x:x[1], reverse=True)


     mediaDict = dict((x, (y/n_rec_base)) for x, y in media_list_sorted)

     title = "Media distribution"

     plot_data = u.create1DplotData(title=title, data_dict=mediaDict)

     return plot_data


def get_dummy_sentiment(text="hello"):

     return random.choice(['NEU','POS','NEG'])


def custom_sentiment(text):

     # The URL of the FastAPI endpoint you want to send the POST request to
     url = 'http://54.177.224.58:8000/items/'
     data = {
    'a': text,
    'article_number': '123'
     }
     # Send the POST request
     response = requests.post(url, json=data)
     # Check the response status code
     if response.status_code == 200:
          overall_sent = response.json()['articleSentiment']

     # Request was successful
          # print('POST request succeeded!')
          # print(response.json()['articleSentiment'])
     else: 
          overall_sent = 'NEU' # default
     # Request failed
          # print(f'POST request failed with status code: {response.status_code}')


     return overall_sent




def get_sentiment_from_data(sent_subset):
    # This function takes a subset of data containing sentiment values
    
    # Find the index with the maximum value along each row of the subset
    series = sent_subset.idxmax(axis=1)
    
    # Remove the 'sentiment.' prefix from each element in the series
    series = series.str.replace('sentiment.', '')
    
    # Return the modified series with sentiment values
    return series


def get_syndication_uniques(df):

     df['syndication'] = [1] * len(df)

     df = df.groupby(['title'], as_index=False).agg({'syndication': 'sum', 'source': 'first', 'reach': 'sum'})

     df['syndication'] = df['syndication']  - 1

     return df



def get_word_cloud_data(text):

# Extraction given the text.
     # r.extract_keywords_from_text(text)


     # To get keyword phrases ranked highest to lowest with scores.
     language = "en"
     max_ngram_size = 3
     deduplication_thresold = 0.9
     deduplication_algo = 'seqm'
     windowSize = 1
     numOfKeywords = 20

     kw_extractor = yake.KeywordExtractor(lan=language, 
                                        n=max_ngram_size, 
                                        dedupLim=deduplication_thresold, 
                                        dedupFunc=deduplication_algo, 
                                        windowsSize=windowSize, 
                                        top=numOfKeywords)
                                             
     keywords = kw_extractor.extract_keywords(text)


     df = pd.DataFrame(data = keywords, columns = ['label', 'value'])

     df['value'] = 1 - df['value']


     phrasesDict = df.to_dict(orient='index')

     title = "Word cloud"
     plot_data = u.create1DplotData(title=title, data_dict=phrasesDict)
     # print(phrase_with_scores[0])

     return plot_data




def extract_person_names(text):
    # Load the SpaCy English model
    
    author = "NA"
    
    # Process the text
    doc = nlp(text)
    
    try:
    # Extract person names
          person_names = []
          for entity in doc.ents:
               if entity.label_ == 'PERSON':
                    person_names.append(entity.text)
          
          author = person_names[0]

          if author in ['admin', 'Admin',"Webmaster", "webmaster"]:
               author = "NA"
    except:
         pass

    return author



def get_reach_over_time():
     
     df=pd.read_csv("./mergedArticles.csv",usecols=['pubDate','reach'])

     dfDict = df.to_dict(orient='index')
     
     title = "Reach over time"
     
     plot_data = u.create1DplotData(title,dfDict)

     return plot_data

def check_date_format(text):
     pubdate = None
     p = r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d'
     date_pattern = re.compile(p)
     op = date_pattern.findall(text)
     try:
          pubdate = op[0]
     except:
          pass
     return pubdate



def find_keyword_in_title(titles,keyword_in_title):

     mask = ''

     #ensure lower case for universal comparision
     titles = titles.str.lower()

     # testing for 1 keyword so index is 0, this can be converted into loop and a combined mask with boolean summation can be created.

     mask = titles.str.contains(keyword_in_title[0].lower())
     # mask = []
     # for t in titles:
     #      if keyword_in_title[0] in t:
     #           mask.append(True)
     #      else:
     #           mask.append(False)

     return mask


def find_keyword_in_entire_text(article_text,keyword_in_entire_text):

     mask = ''

     #ensure lower case for universal comparision
     article_text = article_text.str.lower()

     # testing for 1 keyword so index is 0, this can be converted into loop and a combined mask with boolean summation can be created.

     mask = article_text.str.contains(keyword_in_entire_text[0].lower())

     return mask


def outlet_breakdown():
     '''
     This function expects input in the form of df that has one column vendor to decide weather records belong to online media or print media

     '''
     df = pd.read_csv("./mergedArticles.csv", usecols=['source'])
     df['vendor'] = 'perigon'
     d = {} # this will contain the data that will be returned
     d['title'] = 'Outlet Breakdown'
     d['subtitle'] = 'Subtile placeholder'
     d['Summary'] = 'Outlet breakdown of the Online and Print Media'
     with open("online_media.pkl","rb") as file:
          online_media = pickle.load(file)
     with open("print_media.pkl","rb") as file:
          print_media = pickle.load(file)

     online_media_df = df[df['vendor'] != 'pressreader']
     print_media_df = df[df['vendor'] == 'pressreader']
     d['labels'] = [{'label':'Print','value':len(print_media_df),'color':'#ff9900'}]
     d['labels'].append({'label':'Online','value':len(online_media_df),'color':'#006699'})
     #Processing the online media data
     urls = df['source'].to_list()
     x = [ online_media.get(url, {'Sub Media Type': 'Web'})['Sub Media Type'] for url in urls ]
     om_breakdown = dict(Counter(x))
     d['data'] = {'online':om_breakdown}
     # TODO - incorporate once pressreader is integrated
     # d['data'].append(pressreader_breakdown)
     return d



def sentiment_with_spacy_summarization_on_dataframe(mergedArticles):
    
     import re

     import numpy as np # linear algebra

     import os

     # from happytransformer import HappyTextToText

     # happy_tt1 = HappyTextToText("BERT", "sshleifer/distilbart-cnn-12-6")

     from transformers import pipeline

     sentiment_analyzer=pipeline("sentiment-analysis",model = "finiteautomata/bertweet-base-sentiment-analysis")

     import spacy

     from spacy.lang.en.stop_words import STOP_WORDS

     from string import punctuation

     from heapq import nlargest

     stopwords=list(STOP_WORDS)

     nlp=spacy.load('en_core_web_sm')

     import pandas as pd
     outputxx=[]

     for iii in range(len(mergedArticles)):

        try:

          
            a2a2 = str(mergedArticles['display_content'].iloc[iii])
            docstext = re.sub(r'[^A-Za-z. 0-9, ?]+', '',a2a2)
            a2a2title = str(mergedArticles['title'].iloc[iii])
            docstitle = re.sub(r'[^A-Za-z. 0-9, ?]+', '',a2a2title)
            docs=docstitle+"."+docstext
            docs=docstext
            #docs=docs[0:500]
            result=sentiment_analyzer(docs)
            adict=result[0]
            senti_label=adict['label']
            outputxx.append(senti_label)

        except:

            print(iii)

            outputxx.append("Neu")
     mergedArticles["articleSentiment"]=pd.DataFrame(outputxx)
     
     return mergedArticles

# # summarize_sentiment(text)


def Input_from_User_Primary_Theme_rev3():
    merged_articles = pd.read_csv('.\mergedArticles.csv')

    
    # Sample data for demonstration
    # Sample data for demonstration
    data = {
    'Corporate': ["Social Responsibility", "Openings & Closure", "CXO Mention / Movement", "Events", "Profit", "Bootleg / Copies", "Launch"],
    'Sensitive_Skin_Massaging': ["blemish, blemishes", "breakout(s)", "fragrance free", "unscented", "gentle", "hypoallergenic", "irritating, irritated", "noncomedogenic", "oil-free", "redness", "sensitive sensitivity", "vulnerable", "distressed", "delicate", "reactive reaction", "compromised", "exposed", "damage", "itch", "dry", "rash", "eczema", "psoriasis", "acne", "rosacea", "dermatitis", "oncology", "cancer", "healthy", "hydrating hydrate hydration", "microbiome", "moisturizing, moisturize, moisturization", "prebiotic", "strengthen", "protect", "improves", "wash", "soft", "firm", "cracked", "fragile", "paraben", "phthalates", "harmful"],
    'Therapeutic': ["calming", "calm", "nourishing", "nourishes", "soothing", "soothes", "relieves", "relief", "smoothing", "protect", "replenish", "enriched", "restores", "restorative", "restoring", "restore", "rest", "nurturing", "nurture", "resilience", "resilient"],
    'Comorbidity': ["Comorbidity", "diabetic", "eczema", "psoriasis"],
    'Credentials': ["clinically proven", "derm recommended", "proven", "effective", "recommended", "dermatologist approved", "approved", "Leader", "celebrity recommended", "award winning", "experts"],
    'Efficacy': ["blotchiness", "crow's feet", "clinically proven", "derm recommended", "effective", "healthy", "microbiome", "prebiotic", "recommended"],
    'Beauty_Massaging': ["aging", "complex", "dullness", "hydrating", "hydrate", "hydration", "exfoliate", "lines moisturizing", "moisturize", "moisturization", "puffiness", "radiant spots", "strengthen", "texture", "tone", "wrinkles", "brighten", "absorb", "broad spectrum", "protect", "protection non-greasy", "resistant", "resistance"],
    'Ingredient_Massaging': ["Colloidal oatmeal", "Oat", "Oat flour", "Oat kernal", "Dimethicone", "Prebiotic oat", "Shea Butter", "Emollients", "Soy", "Aloe", "Oils", "Lavender", "Ceramides", "Glycerin", "Vitamin E", "Blackberry Extract", "Sunflower Oil", "Almond Oil", "Hydrocortisone", "Cica", "Honey", "Apricot", "Vanilla", "Coconut", "natural shiitake", "southernwood", "dill", "feverfew", "kiwi", "avobenzone", "complex", "enviroguard technology", "lotus", "mineral", "oxybenzone", "SPF", "titanium", "UVA/UVB", "zinc"],
    'Dove': ["confidence", "skin confidence", "self-esteem", "Real Beauty"],
    'CeraVe': ["Essential Ceramides", "Dermatologists", "ceramides", "ceramides 1", "ceramides 3", "ceramides  6-II", "fatty acids", "lipids", "MultiVesicular Emulsion Technology", "MVE Technology", "hydrate", "restore", "replenish"],
    'Aquaphor': ["protective barrier", "healing", "enhance healing", "minimal ingredients", "sensitive skin", "Petrolatum", "dermatologist recommended", "dry", "cracked skin", "restore"],
    'Jergens': ["transform skin", "soft", "smooth", "gorgeous skin", "Natural Glow", "healthier-looking skin", "radiate"],
    'Nivea': ["researchers", "skin types", "skin types (culture, gender, age)", "climate conditions", "cleanse", "nourish", "protect", "gentle", "effective", "effective care"],
    'Vaseline': ["petroleum jelly", "heal", "dry skin", "expert recommended", "Intensive Care", "healing"],
    'Cetaphil': ["gentle skin", "dermatologist recommended", "dermatologist trusted", "sensitive skin", "skin types", "skin conditions", "healthcare professionals", "medical experts"],
    'Gold_Bond': ["physicians", "healing", "cracked skin", "medicated", "therapeutic"],
    'Goddess_Garden': ["Nova Covington", "organic", "plant-based", "pure minerals"],
    'Bare_Republic': ["biodegradable", "clean ingredients", "cruelty free", "trusted performance", "environmentally friendly", "everyday adventures", "eco-active", "titanium dioxide", "zinc oxide"],
    'Supergoop': ["skincare with SPF", "skincare with sunscreen", "experts in SPF", "Holly Thaggard", "Superpowered SPF", "Ounce by ounce", "feel-good"],
    'Neutrogena': ["Dermatologist recommended", "Dermatologist tested", "Neoglucosamine", "skin experts", "hyaluronic acid", "#1", "most awarded", "every day is SUNday", "zinc"],
    'Olay': ["skin scientists", "ageless", "Vitamin B3", "Glycerin", "Retinyl Propionate", "Amino Peptides", "clinical studies", "trusted"],
    'CeraVe': ["Essential Ceramides", "Dermatologists", "ceramides", "ceramides 1", "ceramides 3", "ceramides  6-II", "fatty acids", "lipids", "MultiVesicular Emulsion Technology", "MVE Technology", "hydrate", "restore", "replenish"],
    'Cetaphil': ["gentle skin", "dermatologist recommended", "dermatologist trusted", "sensitive skin", "skin types", "skin conditions", "healthcare professionals", "medical experts"],
    'Burt_Bees': ["True To Nature", "nature's rules", "nature", "hive", "bees", "bee wax"],
    'Garnier': ["skin experts", "natural ingredients", "natural", "antioxidants", "moisture barrier"],
    'Yes_To': ["natural ingredients", "natural", "fruits", "vegetables"],
    'Simple_Skincare': ["Sensitive Skin", "Experts", "clean", "clean ingredients", "Ophthalmologist-tested", "Dermatologist tested", "Dermatologist recommended", "pH Balance"],
    'Babyganics': ["plant-derived", "certified organic", "pediatrician & dermatologist tested", "#marvelousmess", "#babyganics"],
    'Alba_Botanica': ["Do Beautiful", "#dobeautiful", "body-loving products", "100% vegetarian products", "botanical ingredients", "earth friendly"],
    'Hawaiian_Tropic': ["#alohatherapy", "indulgent sun care", "discover the beauty of sun protection", "indulgent protection", "skin nourishing antioxidants", "exotic botanicals"],
    'Sun_Baby_Bum': ["Trust the Bum", "oxybenzone free", "octinoxate free", "reef friendly", "vegan", "gluten free", "cruelty free", "sulfate free", "paraben free"]
    }
    # Transpose the data dictionary to get the correct structure for the DataFrame
    data_transposed = {k: [", ".join(v)] for k, v in data.items()}

    # Create a DataFrame from the transposed data
    df = pd.DataFrame.from_dict(data_transposed, orient='index', columns=['Keywords'])
    
    def categorize_text(text):
        for index, row in df.iterrows():
            keywords = row['Keywords'].split(', ')
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    return index
        return 'Uncategorized'      
        

    user_input = merged_articles    
    selected_columns = ['title', 'summary', 'description', 'content']
    new_df = user_input[selected_columns].astype(str)
    
    # Use .loc to set the 'MergedText' column
    new_df.loc[:, 'MergedText'] = new_df[selected_columns].apply(lambda row: ' '.join(row), axis=1)
    
    results = []

    # Iterate through the records in the 'MergedText' column
    for record in new_df['MergedText']:
        result = str(categorize_text(record))
        results.append(result)
        
    unique_elements, counts = np.unique(results, return_counts=True)
    
    # Check if there is only one category found
    if len(unique_elements) == 1:
        # If there's only one category, you can handle it accordingly.
        # For example, you might want to return that category or handle it differently.
        final_list_5_themes = [unique_elements[0], None, None, None]
    else:
        # Sort the unique elements and counts in descending order
        sorted_indices = np.argsort(-counts)
        sorted_elements = unique_elements[sorted_indices]
        sorted_counts = counts[sorted_indices]

    # Get the 5 most occurring elements (up to 4 elements if available)
    final_list_5_themes = sorted_elements
    
    print(final_list_5_themes)
    
    # Convert the list elements to strings and pad the list with None if there are less than 4 elements
    #final_list_5_themes = [str(theme) for theme in final_list_5_themes]
    #final_list_5_themes += [str(None)] * (4 - len(final_list_5_themes))
    
    
    return final_list_5_themes
