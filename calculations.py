from data_pipe import data_structures as DS
from data_pipe import fetcher as live_dp
from data_pipe import ES as es_dp
import time
from datetime import datetime as dt, timedelta
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
import spacy
nlp = spacy.load('en_core_web_sm')
import random
from numerize import numerize
import math
from get_values import get_values
from separating_the_data_frame_for_each_articles import separating_the_data_frame_for_each_articles

def get_values(iterables, key_to_find):
    return list(filter(lambda x: key_to_find in x, iterables))

def final_dataframe_with_unique_and_grouping(df):
    df11 = df[["title", "summary"]]  # b will be post_thread_title and c will be posts_text, a will be website

    df1 = df11[df11.duplicated(keep=False)]
    all_details = df1.groupby(list(df1)).apply(lambda x: tuple(x.index)).tolist()

    reject = []
    all_merge = []

    for i in range(len(all_details)):
        for j in range(1, len(all_details[i])):
            reject.append(all_details[i][j])

    for i in range(len(all_details)):
        for j in range(len(all_details[i])):
            all_merge.append(all_details[i][j])

    all_accept_among_duplicate = [elem for elem in all_merge if elem not in reject]
    all_nonduplicate = [elem for elem in list(range(len(df))) if elem not in all_merge]

    syndication = [0] * len(df)
    for k2 in range(len(df)):
        if k2 in all_merge:
            syndication[k2] = len(get_values(all_details, k2)[0]) - 1
        else:
            syndication[k2] = 0

    all_listing_done = all_details + all_nonduplicate
    final_all_indexing = all_accept_among_duplicate + all_nonduplicate

    df['Syndication'] = syndication
    df = df.drop(df.index[reject[:]])
    df.reset_index(drop=True, inplace=True)

    return df, all_listing_done, final_all_indexing, all_details

def get_matchedKeywords(text):
    try:
        p = u.get_search_terms_regex()
        count = len(re.findall(p, text))
    except Exception as e:
        print(f"Error occurred: {e}")
        count = 0
    return count

import pandas as pd

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

        # Perform datetime conversion and filter out invalid dates
        counts_ts_df['pubDate'] = pd.to_datetime(counts_ts_df['pubDate'], format=format1, errors='coerce')
        counts_ts_df.dropna(subset=['pubDate'], inplace=True)

        counts_ts_df.set_index('pubDate', inplace=True)

        # Resample and interpolate
        mentions_agg_counts_smooth = counts_ts_df.resample('1h').sum()
        mentions_agg_counts_smooth['matchedKeywords'] = mentions_agg_counts_smooth['matchedKeywords'].apply(abs)
        mentions_agg_counts_smooth = mentions_agg_counts_smooth.interpolate(method='linear')
        mentions_agg_counts_smooth.rename(columns={'matchedKeywords': 'mentionCounts'}, inplace=True)

        # Save to CSV (optional, remove if not needed)
        mentions_agg_counts_smooth.to_csv("mentions_agg_counts_smooth.csv")

        return mentions_agg_counts_smooth

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def dashboard_view_top_authors():
    try:
        # Read the data
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['author', 'reach'])

        # Get the list of authors and their counts
        authors_list = tuple(articles_df['author'].dropna())
        author_counter = Counter(authors_list)
        author_sorted = sorted(author_counter.items(), key=lambda x: x[1], reverse=True)

        # Get the top 50 authors based on article counts
        top5authors = tuple(author_sorted)[:50]
        top5authorsDict = dict((x, int(y)) for x, y in top5authors)

        # Filter the reach_values DataFrame with only top authors
        reach_values = articles_df[articles_df['author'].isin(top5authorsDict.keys())]
        reach_values['counts'] = reach_values['author'].map(top5authorsDict)

        # Sort and keep the highest reach value for each author
        reach_values.sort_values(by=['counts', 'reach'], inplace=True, ascending=False)
        reach_values.drop_duplicates(subset=['author'], keep='first', inplace=True)

        # Create the final_authors_dict with author names and their respective counts
        final_authors_dict = dict(zip(reach_values['author'], reach_values['counts']))

        title = "View top authors"
        plot_data = u.create1DplotData(title=title, data_dict=final_authors_dict)

        return plot_data

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def dashboard_view_top_sources():
    try:
        # Read the data
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['source'])

        # Get the list of sources and their counts
        sources_list = tuple(articles_df['source'].dropna())
        source_counter = Counter(sources_list)
        source_sorted = sorted(source_counter.items(), key=lambda x: x[1], reverse=True)

        # Get the top 5 data sources based on article counts
        top5sources = tuple(source_sorted)[:5]
        top5sourcesDict = dict((x, int(y)) for x, y in top5sources)

        title = "View top sources"
        plot_data = u.create1DplotData(title=title, data_dict=top5sourcesDict)

        return plot_data

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def dashboard_view_geo_breakdown_us():
    try:
        # Read the data
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['state'])

        # Get the list of states and their counts
        states_list = tuple(articles_df['state'].dropna())
        states_counter = Counter(states_list)
        states_sorted = sorted(states_counter.items(), key=lambda x: x[1], reverse=True)

        # Get the top 5 states based on article counts
        top5states = tuple(states_sorted)[:5]
        top5statesDict = dict((x, int(y)) for x, y in top5states)

        title = "View Geographic breakdown"
        plot_data = u.create1DplotData(title=title, data_dict=top5statesDict)

        return plot_data

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_reach_value(source):
    try:
        if len(source) < 5:
            reach_value = 0
        else:
            reach_map = pickle.load(open("./data_pipe/reach.pkl", "rb"))
            reach_value = reach_map['current_month_reach'].get(source, 0)
    except FileNotFoundError:
        raise Exception("The 'reach.pkl' file not found. Please run the data_pipe to generate the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    return reach_value

def get_top_articles_by_reach():
    try:
        display_cols = ['pubDate', 'title', 'author', 'reach']
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=display_cols)
        articles_df = articles_df.sort_values(by='reach', ascending=False)
        return articles_df.head()

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_top_articles_by_ave():
    try:
        display_cols = ['pubDate', 'title', 'author', 'AVE']
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=display_cols)
        articles_df = articles_df.sort_values(by='AVE', ascending=False)
        return articles_df.head()

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_total_sentiments():
    try:
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['articleSentiment'])
        sent_list = tuple(articles_df['articleSentiment'].dropna())
        sentiment_counter = Counter(sent_list)
    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    
    return sentiment_counter

def get_total_ave():
    try:
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['AVE'])
        total_ave = articles_df.mean()[0]
        total_ave, total_ave_in_str = convert_to_millions_or_thousands(total_ave)
    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
    
    return total_ave, total_ave_in_str

def get_total_reach():
    total_reach = 0
    total_reach_in_str = str(total_reach)

    try:
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['reach'])
        total_reach = articles_df.mean()[0]

        total_reach, total_reach_in_str = convert_to_millions_or_thousands(total_reach)

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

    return total_reach, total_reach_in_str

def convert_to_millions_or_thousands(n):
    display_str = numerize.numerize(n)
    return n, display_str

def get_media_type():
    try:
        articles_df = pd.read_csv("./mergedArticles.csv", usecols=['author'])
        n_rec = len(articles_df)

        if n_rec < 100:
            n_rec_base = 100  # to adjust for % as asked by Rhombus
        else:
            n_rec_base = n_rec

        media_list = ["Online"] * (n_rec_base - 1)
        media_list.append("Print")  # adding category

        media_list_counter = Counter(media_list)
        media_list_sorted = sorted(media_list_counter.items(), key=lambda x: x[1], reverse=True)

        mediaDict = dict((x, (y / n_rec_base)) for x, y in media_list_sorted)

        title = "Media distribution"
        plot_data = u.create1DplotData(title=title, data_dict=mediaDict)

        return plot_data

    except FileNotFoundError:
        raise Exception("The file './mergedArticles.csv' does not exist. Please run the search_pipe() function to create the file.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_dummy_sentiment(text="hello"):
    return random.choice(['NEU', 'POS', 'NEG'])


def custom_sentiment(text):
    # The URL of the FastAPI endpoint you want to send the POST request to
    url = 'http://54.177.224.58:8000/items/'
    data = {
        'a': text,
        'article_number': '123'
    }

    try:
        # Send the POST request
        response = requests.post(url, json=data)

        # Check the response status code
        if response.status_code == 200:
            overall_sent = response.json().get('articleSentiment', 'NEU')
        else:
            overall_sent = 'NEU'  # Default if request failed or response format is unexpected
    except requests.exceptions.RequestException as e:
        # Request failed due to network/connection issues or other request-specific errors
        overall_sent = 'NEU'
    except Exception as e:
        # Other unexpected exceptions during request or JSON parsing
        overall_sent = 'NEU'

    return overall_sent

def get_sentiment_from_data(sent_subset):
    # Find the index with the maximum value along each row of the subset
    series = sent_subset.idxmax(axis=1)

    # Remove the 'sentiment.' prefix from each element in the series
    series = series.str.replace('sentiment.', '')

    # Return the modified series with sentiment values
    return series

def get_syndication_uniques(df):
    # Set 'syndication' column with all values as 1
    df['syndication'] = [1] * len(df)

    # Group by 'title' and aggregate the syndication count, source, and reach
    df = df.groupby(['title'], as_index=False).agg({'syndication': 'sum', 'source': 'first', 'reach': 'sum'})

    # Subtract 1 from the 'syndication' values
    df['syndication'] = df['syndication'] - 1

    return df

def get_word_cloud_data(text):
    # Define parameters for YAKE keyword extraction
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 20

    # Initialize the YAKE keyword extractor
    kw_extractor = yake.KeywordExtractor(lan=language,
                                         n=max_ngram_size,
                                         dedupLim=deduplication_threshold,
                                         dedupFunc=deduplication_algo,
                                         windowsSize=windowSize,
                                         top=numOfKeywords)

    # Extract keywords with scores from the given text
    keywords = kw_extractor.extract_keywords(text)

    # Create a DataFrame from the extracted keywords and scores
    df = pd.DataFrame(data=keywords, columns=['label', 'value'])

    # Transform the scores (values) to make them suitable for word cloud (1 - value)
    df['value'] = 1 - df['value']

    # Convert the DataFrame to a dictionary of dictionaries with each keyword and its score
    phrasesDict = df.to_dict(orient='index')

    title = "Word cloud"
    plot_data = u.create1DplotData(title=title, data_dict=phrasesDict)

    return plot_data

def extract_person_names(text):
    # Load the SpaCy English model
    nlp = spacy.load("en_core_web_sm")

    author = "NA"

    # Process the text
    doc = nlp(text)

    try:
        # Extract person names
        person_names = [entity.text for entity in doc.ents if entity.label_ == 'PERSON']

        # Get the first person name (if any)
        if person_names:
            author = person_names[0]

        # Check if the author is one of the specified names, and set to "NA" if so
        if author in ['admin', 'Admin', 'Webmaster', 'webmaster']:
            author = "NA"
    except:
        pass

    return author

def get_reach_over_time():
    df = pd.read_csv("./mergedArticles.csv", usecols=['pubDate', 'reach'])
    dfDict = df.to_dict(orient='index')
    title = "Reach over time"
    plot_data = u.create1DplotData(title, dfDict)
    return plot_data

def check_date_format(text):
    pubdate = None
    date_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    date_match = re.search(date_pattern, text)
    if date_match:
        pubdate = date_match.group()
    return pubdate

def find_keyword_in_title(titles, keyword_in_title):
    # Ensure lower case for universal comparison
    titles = titles.str.lower()

    # Initialize the mask with False
    mask = False

    # Check if the keyword is present in the titles
    mask = titles.str.contains(keyword_in_title[0].lower())

    # To find occurrences of multiple keywords, extend the function
    # and combine masks using boolean summation (e.g., mask = mask1 | mask2 | ...)

    return mask

def find_keyword_in_entire_text(article_text, keyword_in_entire_text):
    # Ensure lower case for universal comparison
    article_text = article_text.lower()

    # Initialize the mask with False
    mask = False

    # Check if the keyword is present in the entire text
    mask = article_text.str.contains(keyword_in_entire_text[0].lower())

    # To find occurrences of multiple keywords, extend the function
    # and combine masks using boolean summation (e.g., mask = mask1 | mask2 | ...)

    return mask

def outlet_breakdown():
    # Read the DataFrame with 'source' column
    df = pd.read_csv("./mergedArticles.csv", usecols=['source'])
    df['vendor'] = 'perigon'  # Assuming the 'vendor' column is initialized with 'perigon' for all rows

    # Initialize the dictionary to store the data for output
    d = {}
    d['title'] = 'Outlet Breakdown'
    d['subtitle'] = 'Subtitle placeholder'
    d['Summary'] = 'Outlet breakdown of the Online and Print Media'

    # Load the online media and print media data (assuming they are pickled and saved in files)
    with open("online_media.pkl", "rb") as file:
        online_media = pickle.load(file)
    with open("print_media.pkl", "rb") as file:
        print_media = pickle.load(file)

    # Separate the online media and print media data based on the 'vendor' column
    online_media_df = df[df['vendor'] != 'pressreader']
    print_media_df = df[df['vendor'] == 'pressreader']

    # Add label data for Online and Print media
    d['labels'] = [{'label': 'Print', 'value': len(print_media_df), 'color': '#ff9900'}]
    d['labels'].append({'label': 'Online', 'value': len(online_media_df), 'color': '#006699'})

    # Process the online media data
    urls = df['source'].to_list()
    x = [online_media.get(url, {'Sub Media Type': 'Web'})['Sub Media Type'] for url in urls]
    om_breakdown = dict(Counter(x))
    d['data'] = {'online': om_breakdown}

    # TODO - Incorporate pressreader breakdown once pressreader is integrated

    return d

def sentiment_with_spacy_summarization_on_dataframe(mergedArticles):
    # Set up the pipeline for sentiment analysis using BERTweet
    sentiment_analyzer = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')

    outputxx = []

    for iii in range(len(mergedArticles)):
        try:
            # Preprocess the text
            a2a2 = str(mergedArticles['display_content'].iloc[iii])
            docstext = re.sub(r'[^A-Za-z. 0-9, ?]+', '', a2a2)
            a2a2title = str(mergedArticles['title'].iloc[iii])
            docstitle = re.sub(r'[^A-Za-z. 0-9, ?]+', '', a2a2title)
            docs = docstitle + "." + docstext
            docs = docstext

            # Perform sentiment analysis on the article text using BERTweet
            result = sentiment_analyzer(docs)
            adict = result[0]
            senti_label = adict['label']
            outputxx.append(senti_label)

        except Exception as e:
            print(e)
            outputxx.append("Neu")

    # Add the sentiment labels to the DataFrame
    mergedArticles["articleSentiment"] = pd.DataFrame(outputxx)

    return mergedArticles








