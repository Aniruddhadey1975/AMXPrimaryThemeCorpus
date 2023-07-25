from collections import Counter
import string
import pandas as pd
from datetime import datetime, timedelta
import json
import requests
from elasticsearch.helpers import bulk
import searcher as s1
from data_pipe import data_structures as DS
# Getting the credentials from the es_config file
import configparser
import pickle
import re
from urllib.parse import quote
import os
  


def get_clean_text(text):

     cleaned_text = text

     try:
          cleaned_text = str(text.encode(encoding="ascii",errors="ignore")).lstrip("b'").rstrip("'").strip('"').strip("'")

     except:
          pass 
     
     return cleaned_text


def get_search_terms_regex():

     dummy,ss = s1.get_search_settings()

     search_terms_regex = '*'

     cleaned_q = ss.searchQuery
     replace_list = ['AND', 'OR', "NOT", "(", ")"]
     cleaned_q = re.sub(r'|'.join(map(re.escape, replace_list)), '', ss.searchQuery)
     search_terms_regex = [str(x) + "|"  for x in cleaned_q.split(" ")]

     search_terms_regex_str  = r"". join(search_terms_regex[:-1])


     return search_terms_regex_str



def create1DplotData(title,data_dict):

     data = []
     for k,v in data_dict.items():
          data.append({'label': k, 'value' : v})

     #### prepare plot data

     plot_data = DS.AMXOneD()

     plot_data.title = title
     plot_data.data = data
     

     return plot_data.__dict__




def extract_key_entity(originalList,keyEntity):
    e = ''
    if (len(originalList)):
        e = originalList[0].get(keyEntity)

    
    return e

def extract_state(locations):

     state = ''

     if len(locations):
          state = extract_key_entity(locations, 'state')

     return state



def get_es():

     es_connect = False

     es_config = configparser.ConfigParser()
     es_config.read('./data_pipe/es_config.ini')
     # print(f"config={es_config.sections()}")

     es_configs = dict(es_config['ES_SETTINGS'])

     # print("d=",es_configs)

     # Importing required packages
     try:
          from elasticsearch import Elasticsearch
          import boto3

     except Exception as e:
          # print(f"Error occured while importing required packages - {e}")
          pass

     # Creating ES and s3 client
     try:
          es_max_hits = 10000
          es_connect = Elasticsearch(es_configs['es_host'], basic_auth=('elastic',es_configs['es_pwd']))
          session = boto3.Session(aws_access_key_id=es_configs['aws_access_key_id'], aws_secret_access_key=es_configs['aws_secret_key'])
          s3 = session.client('s3')
     except Exception as e:
          # print(f"Error occured while creating ES/S3 client - {e}")
          pass


     return es_connect


def make_df(all_data_raw): 

     all_data = all_data_raw['hits']['hits']

     all_data_df = pd.json_normalize(all_data)

     return all_data_df


def flatten_list(l):

     try:
          return l[0]
     except:
          return None


    
def create_date_range(start_dt,end_dt):
   


     start_dt = datetime.strptime(start_dt, '%Y-%m-%d')
     end_dt = datetime.strptime(end_dt, '%Y-%m-%d')

     # difference between current and previous date
     delta = timedelta(days=1)

     # store the dates between two dates in a list
     dates = []

     while start_dt <= end_dt:
          # add current date to list by converting  it to iso format
          dates.append(start_dt.isoformat())
          # increment start date by timedelta
          start_dt += delta


     # print (dates)
     # return dates

     paired_dates = zip(dates[0::2], dates[1::2])

     return paired_dates


def process_search_term(search_term):
     
     search_term = search_term.strip(" ")

     search_term = search_term.replace(" ", "%20")

     search_term = search_term.replace('"', "%22")

     search_term = search_term.replace('&', '%26')

     # replace_list = ["&", "/"]

     # search_term = re.sub(r'|'.join(map(re.escape, replace_list)), '', search_term)

     return search_term


