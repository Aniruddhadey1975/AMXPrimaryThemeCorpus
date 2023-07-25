import streamlit as st # web development
st.set_option('deprecation.showPyplotGlobalUse', False)

import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import math
import plotly.graph_objects as go
 
from wordcloud import WordCloud
from datetime import datetime as dt
from datetime import timedelta
import collections

from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import timeit
from collections import Counter
import string
import random
import calculations as calc
import searcher as s1
import UI_utils as ui_utils
from wordcloud import STOPWORDS
stopwords = set(STOPWORDS)
import pickle
import matplotlib.pyplot as plt

sources_selected = {}


st.set_page_config(
    page_title = 'AlphametricX Search',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title

# st.title("Search POC V1 with Elastic pipes")


# set empty frames 

mergedArticles = pd.DataFrame() # set empty
total_articles = 0





## tabs 

search_tab, advance_search_tab , executive_dashboard_tab , brand_dashboard_tab  = st.tabs(["Search","Advance Search" , "Executive Dashboard", "Brand Dashboard"])

##################### SEARCH TAB  start###################################################
with search_tab:

    st.header("Search : Time frame 2022-23")
    # top-level filters 


    with st.form("search_form"):

         
        d = dt.now()
        today = d.date()
        year_back = dt.now() - timedelta(days=1*365)
        year_back_date = year_back.date()

        week_back = dt.now() - timedelta(days=7)
        week_back_date = week_back.date()

        previous_day = dt.now() - timedelta(days=1)
        previous_day_date = previous_day.date()

        

        search_query = st.text_input("Please enter any Individual, Topic or Keywords")




        c1, c2, c3, c4 = st.columns((1, 1, 1, 1))

        with c1:
            
            media_expander = st.expander(label="Media Type")

            with media_expander:        
                media_options = {
                'print': st.checkbox('Print',value=True),
                'online': st.checkbox('Online',value=True),
                'blogs': st.checkbox('Blogs'),
                'forums': st.checkbox('Forums'),
                'broadcast': st.checkbox('Broadcast'),
                
            }
                
            

        with c2:
            
            location_expander = st.expander(label="Location")

            with location_expander:        
                location_options = {
                'US': st.checkbox('us',value=True),
                'UK': st.checkbox('uk'),
    
                
            }
            
        with c3:
            
            language_expander = st.expander(label="Language")

            with language_expander:        
                language_options = {
                'EN': st.checkbox('EN',value=True),
                'DE': st.checkbox('DE'),
    
                
            }
                

        with c4: 

            timeline_expander = st.expander(label="Timeline")

            with timeline_expander:

                # timeline_key = st.radio("Timeline", ('custom', '1D', '1W', '1M'))



                custom_start_date = st.text_input(label='custom_start_date')
                custom_end_date = st.text_input(label='custom_end_date')
                st.write("Date format : 2023-01-01 (YYYY-MM-DD)")
                source_selection = {}


        row2 = st.container()

        with row2:

            submitted = st.form_submit_button("Go")
            st.write(st.__version__)

    ######## end of search form 
        if submitted:

            sources_selected = []

            for k,v in source_selection.items():
                if v: 
                    # print("for ",k, "v is ", v)
                    sources_selected.append(k)

            # print("sources_selected=", sources_selected)

            # check if inputs are available

            if (search_query and custom_start_date and custom_end_date):

                search_start = dt.now()
                # try:
                (total_articles, mergedArticles) = s1.search_pipe(search_query,custom_start_date,custom_end_date,language_options,location_options,sources_selected,keyword_in_title_include_exclude=None,keyword_in_title=[],no_opinions=False,non_news=False,no_press_release=False, with_less_reach=False,keyword_in_text=[],keyword_in_text_range=20,search_type = "simple_search", intitated_from_page = "",userID="123", searchID = "XX", lightMode=False)
                # except:
                #     st.write("No results found")
                #     exit(1)
                
                search_end = dt.now()
                # print(">>total_articles = ", total_articles)
                
                timetaken = search_end - search_start

                # print(timetaken)

                st.write("Response time(s): ", timetaken)
            else:
                st.write("ERROR: Please provide all the required fields, e.g. search query and timeframe.")
                exit(0)


                

                ###############################################################################################################################




            search_results = st.empty()


            with search_results.container():
                        # create three columns
                kpi1, kpi2, kpi3 = st.columns(3)




                total_reach,total_reach_str = calc.get_total_reach()
                
                total_ave, total_ave_str = calc.get_total_ave()
                
                total_articles,total_articles_str = calc.convert_to_millions_or_thousands(total_articles)

                kpi1.metric(label="Total Articles ", value=str(total_articles))



                kpi2.metric(label="Total Reach ", value=total_reach_str)



                kpi3.metric(label="Total AVE ", value=total_ave_str)


            if total_articles > 0 and not (mergedArticles.empty):

                mentions_graph = st.container()


                with mentions_graph:                    

                    mentions_agg_counts = calc.results_over_time()

                    
                    fig = ui_utils.results_over_time_graph(mentions_agg_counts)
                    

                    if fig:

                        if len(mentions_agg_counts) >= 5:
                            st.write(fig)
                    else:
                        st.write('----------------------------------------')

                        
# search results block, display only if results are found
                search_results = st.container()

                
                with search_results:

                    articles_list = st.container()          

                    with articles_list:

                        for _, a in mergedArticles.head(50).iterrows():

                            row1 = st.container()     

                            with row1:

                                content_col, stats_col = st.columns([0.75,0.25])

                                with content_col:
                                    inner_table = st.container()

                                    with inner_table:
                                        article_row = st.container()

                                        info_row = st.container()

                                        sep_row = st.container()

                                        with article_row:
                                            pic, desc = st.columns([0.20,0.80])

                                            with pic:
                                                st.write("picture place holder")
                                            
                                            with desc: 
                                                # st.write("article description")

                                                article_desc_row = st.container()

                                                with article_desc_row:
                                                    a_title_row = st.container()
                                                    a_desc_row = st.container()
                                                    with a_title_row:
                                                        st.markdown("**" + a['title'] + "**")

                                                    with a_desc_row:
                                                    
                                                        st.write(a['display_content'][:100] + "...")

                                                        st.write("[Article link](",a['url'],")")

                                            

                                        with info_row:

                                            st.write(a['source'], "|"," ",  a['pubDate'],"|", " ", a['author'], "|", " ",a['state'] , " US", "|", " ", a['matchedKeywords'], " Matching kwywords", "|", " ", "Online news" ) 
                                            
                                    
                            with stats_col:

                                    sent_stat_row = st.container()
                                    reach_ave_syndication_row = st.container()
                                    matches_row = st.container()

                                    with sent_stat_row:
                                        try:
                                            st.write(a['articleSentiment'] ) 
                                        except: 
                                            pass

                                    with reach_ave_syndication_row:
                                        article_reach, article_reach_str = calc.convert_to_millions_or_thousands(a['reach'])
                                        article_ave, article_ave_str = calc.convert_to_millions_or_thousands(a['AVE'])
                                        st.write("Reach ",article_reach_str,"\t" ,  " AVE", article_ave_str)       

                                    with sep_row:
                                        st.write("___________________________________________________________________________________________")

                                    
                        

                        # fig, ax = plt.subplots()
                                
                        # ax.hist(mergedArticles['author'], bins=20)

                        # st.pyplot(fig)


##################### SEARCH TAB  end ###################################################


##################### ADVANCE SEARCH TAB  start###################################################
with advance_search_tab:

    st.header("Search : Time frame 2022-23")
    # top-level filters 


    with st.form("advance_search_form"):

        # st.header("Data available in ES (2023-05-01 to 2023-05-31) ") 
        d = dt.now()
        today = d.date()
        year_back = dt.now() - timedelta(days=1*365)
        year_back_date = year_back.date()

        week_back = dt.now() - timedelta(days=7)
        week_back_date = week_back.date()

        previous_day = dt.now() - timedelta(days=1)
        previous_day_date = previous_day.date()

        
        search_query_all_c, search_query_any_c,search_query_non_c = st.columns([1,1,1])

        with search_query_all_c:

            search_query_all = st.text_area("All of these")
        
        with search_query_any_c:
            search_query_any = st.text_area("Any of these")
        
        with search_query_non_c:
            search_query_non = st.text_area("None of these")

        search_query_all = search_query_all.replace(",", " AND ")
        search_query_any = search_query_any.replace(",", " OR ")
        search_query_non = search_query_non.replace(",", " OR ")
        # search_query_all = "(" +  search_query_all.replace(",", " AND ")  + ") "
        # search_query_any = "(" +  search_query_all.replace(",", " OR ")  + ") "
        # search_query_non =  + " NOT "  +  "(" +  search_query_all.replace(",", " AND ")  + ")"

        # search_query = search_query_all = "(" + search_query_all + ") " + " AND "  + " (" + search_query_any + ")" + " AND " + "(" + "NOT " + "(" + search_query_non + ")" + ")"
        
        search_query = search_query_all = "(" + search_query_all + ") " + " AND "  + " (" + search_query_any + ")"  + " NOT " + "(" + search_query_non + ")" 

        st.write("Searching for : ", search_query)


        c1, c2, c3, c4 = st.columns((1, 1, 1, 1))

        with c1:
            
            media_expander = st.expander(label="Media Type")

            with media_expander:        
                media_options = {
                'print': st.checkbox('Print',value=True),
                'online': st.checkbox('Online',value=True),
                'blogs': st.checkbox('Blogs'),
                'forums': st.checkbox('Forums'),
                'broadcast': st.checkbox('Broadcast'),
                
            }
                
            

        with c2:
            
            location_expander = st.expander(label="Location")

            with location_expander:        
                location_options = {
                'US': st.checkbox('us',value=True),
                'UK': st.checkbox('uk'),
    
                
            }
            
        with c3:
            
            language_expander = st.expander(label="Language")

            with language_expander:        
                language_options = {
                'EN': st.checkbox('EN',value=True),
                'DE': st.checkbox('DE'),
    
                
            }
                

        with c4: 

            timeline_expander = st.expander(label="Timeline")

            with timeline_expander:

                # timeline_key = st.radio("Timeline", ('custom', '1D', '1W', '1M'))



                custom_start_date = st.text_input(label='custom_start_date')
                custom_end_date = st.text_input(label='custom_end_date')
                st.write("Date format : 2023-01-01 (YYYY-MM-DD)")

                source_selection = {}
############### advance search filters
        advance_search_expander = st.expander("Advance filters")


        with advance_search_expander:

            source_customization, keyword_prominance, exclude_media = st.columns([1,1,1])


            with source_customization:

                st.write("**Source customization**")

                sources_list = ui_utils.get_sources_list()


                # st.write(sources_list)

                source_selection = {}

                for source in sources_list:
                    source_selection[source] = st.checkbox(label=source)

                sources_selected = []

                for k,v in source_selection.items():
                    if v: 
                        sources_selected.append(k)

            with keyword_prominance:
                st.write("Keyword prominance")

                keyword_in_title, keyword_placement = st.columns([1,1])

                with keyword_in_title:
                    st.write("Keyword in title")
                    keyword_in_title_include_exclude = st.radio("Select inclusion or exclusion : ", ("include", "exclude"))
                    keyword_in_title = st.text_area(label="Keywords in title")

                    # split it into comma separated list - as availed from UI
                    keyword_in_title = keyword_in_title.split(',')
                with keyword_placement:
                    st.write("Keyword placement")
                    st.write("Enter keywords to check in specific range")
                    keyword_in_text = st.text_area(label="Keywords in content range")
                    keyword_in_text_range = st.slider('Within range', min_value=0,max_value=20,value=20)
                    # split it into comma separated list - as availed from UI
                    keyword_in_text = keyword_in_text.split(',')


                with exclude_media:
                    st.write("**Spam exclusions**")
                    st.write("Select what to exclude")

                    # no_spam_filter = st.checkbox('None',value=True)
                    no_opinions = st.checkbox('No Opinions')
                    non_news = st.checkbox('Non News')
                    no_press_release=st.checkbox('No press release')
                    with_less_reach = False # temporary
                    # with_less_reach = st.checkbox('Lower priority websites')

            
#################### end of advance search filters


        row2 = st.container()

        with row2:

            # hybrid = st.checkbox('ES',value=True)
            submitted = st.form_submit_button("Go")
            

    ######## end of search form 
        if submitted:

            # print("no_opinions=",no_opinions)
            # print("non_news=",non_news)
            # print("with_less_reach=",with_less_reach)


            sources_selected = []

            for k,v in source_selection.items():
                if v: 
                    # print("for ",k, "v is ", v)
                    sources_selected.append(k)

            # print("sources_selected=", sources_selected)



            # check if inputs are available

            if (search_query and custom_start_date and custom_end_date):

                search_start = dt.now()
                # try:
                
                (total_articles, mergedArticles) = s1.search_pipe(search_query,custom_start_date,custom_end_date,language_options,location_options, sources_selected,keyword_in_title_include_exclude=keyword_in_title_include_exclude,keyword_in_title=keyword_in_title,no_opinions=no_opinions,non_news=non_news,no_press_release=no_press_release, with_less_reach=with_less_reach,keyword_in_text=keyword_in_text,keyword_in_text_range=keyword_in_text_range,search_type = "advance_search", intitated_from_page = "",userID="123", searchID = "XX", lightMode=False)
                # except:
                #     st.write("No results found")
                #     exit(1)
                
                search_end = dt.now()
                # print(">>total_articles = ", total_articles)
                
                timetaken = search_end - search_start

                # print(timetaken)

                st.write("Response time(s): ", timetaken)



                

                ###############################################################################################################################




                search_results = st.empty()


                with search_results.container():
                            # create three columns
                    kpi1, kpi2, kpi3 = st.columns(3)



                    

                    # if total_articles> 1000: 
                    #     total_articles_str = numerize.numerize(total_articles)
                    # else:
                    #     total_articles_str = str(total_articles)

                    try:

                        total_reach,total_reach_str = calc.get_total_reach()
                        
                        total_ave, total_ave_str = calc.get_total_ave()
                        
                        total_articles,total_articles_str = calc.convert_to_millions_or_thousands(total_articles)

                        kpi1.metric(label="Total Articles ", value=str(total_articles))



                        kpi2.metric(label="Total Reach ", value=total_reach_str)



                        kpi3.metric(label="Total AVE ", value=total_ave_str)
                    except:
                        # place holder for error msg
                        st.write("______________________________")


                if total_articles > 0 and (not mergedArticles.empty): # if results are found

                    mentions_graph = st.container()


                    with mentions_graph:

                        
                        try:

                            mentions_agg_counts = calc.results_over_time()

                            
                            fig = ui_utils.results_over_time_graph(mentions_agg_counts)
                        
                        except:
                            fig = ''


                        if fig:

                            if len(mentions_agg_counts) >= 5:
                                st.write(fig)
                        else:
                            st.write('----------------------------------------')

                # search results block of the results are found        

                    search_results = st.container()

                    

                    with search_results:

                        st.header("Search results")

                        articles_list = st.container()          
                        

                        with articles_list:




                            # mergedArticles['keywords_match'] = mergedArticles['display_content'].apply(kw_counter)

                            # st.table(mergedArticles)


                            for _, a in mergedArticles.head(50).iterrows():

                                row1 = st.container()     

                                with row1:

                                    content_col, stats_col = st.columns([0.75,0.25])

                                    with content_col:
                                        inner_table = st.container()

                                        with inner_table:
                                            article_row = st.container()

                                            info_row = st.container()

                                            sep_row = st.container()

                                            with article_row:
                                                pic, desc = st.columns([0.20,0.80])

                                                with pic:
                                                    st.write("picture place holder")
                                                
                                                with desc: 
                                                    # st.write("article description")

                                                    article_desc_row = st.container()

                                                    with article_desc_row:
                                                        a_title_row = st.container()
                                                        a_desc_row = st.container()
                                                        with a_title_row:
                                                            st.markdown("**" + a['title'] + "**")

                                                        with a_desc_row:
                                                            st.write(a['display_content'][:100] + "...")

                                                            st.write("[Article link ](",a['url'],")")

                                                        

                                                

                                            with info_row:

                                                st.write(a['source'], "|"," ",  a['pubDate'],"|", " ", a['author'], "|", " ",a['state'] , " US", "|", " ", a['matchedKeywords'], " Matching kwywords", "|", " ", "Online news" ) 
                                                
                                        
                                with stats_col:

                                        sent_stat_row = st.container()
                                        reach_ave_syndication_row = st.container()
                                        matches_row = st.container()

                                        with sent_stat_row:
                                            try:
                                                st.write(a['articleSentiment'] ) 
                                            except: 
                                                pass

                                        with reach_ave_syndication_row:
                                            article_reach, article_reach_str = calc.convert_to_millions_or_thousands(a['reach'])
                                            article_ave, article_ave_str = calc.convert_to_millions_or_thousands(a['AVE'])
                                            st.write("Reach ",article_reach_str,"\t" ,  " AVE", article_ave_str)     
                                            # st.write("Syndication ",a['syndication'])  
                                            # pub_date,author, matched_kw, source = st.columns([1,1,1,1])

                                            # with pub_date:
                                            #     st.write(a["pubDate"]) 

                                            # with author:
                                            #     st.write(a["author"])

                                            # with matched_kw:
                                            #     try:
                                            #         st.write("Matched ", a['matchedKeywords'], " words")  
                                            #     except:
                                            #         st.write(random.randint(6, 15))  

                                                    
                                            
                                            # with source:
                                            #     st.write(a['source'])  


                                        with sep_row:
                                            st.write("___________________________________________________________________________________________")

                                        
                            

                            # fig, ax = plt.subplots()
                                    
                            # ax.hist(mergedArticles['author'], bins=20)

                            # st.pyplot(fig)


##################### ADVANCE SEARCH TAB  end ###################################################


############ limiting to search results for testing
    # exit(0)


##################### EXECUTIVE DASHBOARD START #############################################


    with executive_dashboard_tab:

        if mergedArticles.empty:
            st.write("Please make a search")

        else: # already existing search 

            view_exec_dashboard = 1
            if view_exec_dashboard:

                executive_dashboard_view = st.container()                               

                with executive_dashboard_view:

                    st.header("EXECUTIVE DASHBOARD")  

                    sentiment_header_row = st.container()
                    sentiment_pos_kpi,sentiment_neg_kpi, sentiment_neu_kpi,sent_insight= st.columns([1,1,1,1])

                    sentiment_counts = calc.get_total_sentiments(total_articles=total_articles)
                    sent_pos, sent_pos_str = calc.convert_to_millions_or_thousands(sentiment_counts['POS'])

                    sent_neg, sent_neg_str = calc.convert_to_millions_or_thousands(sentiment_counts['NEG'])

                    sent_neu, sent_neu_str = calc.convert_to_millions_or_thousands(sentiment_counts['NEU'])

                    sentiment_pos_kpi.metric(label="Positive", value=sent_pos_str)
                    sentiment_neg_kpi.metric(label="Negative", value=sent_neg_str)
                    sentiment_neu_kpi.metric(label="Neutral", value=sent_neu_str)


                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")
                    article_list_reach_article_list_ave_row = st.container()
                    article_list_reach, article_list_ave= st.columns([1,1])

                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")

                    with article_list_reach_article_list_ave_row:
                        with article_list_reach:
                            st.write("article_list_reach")
                            top_articles_by_reach = calc.get_top_articles_by_reach()
                            st.table(top_articles_by_reach[['pubDate','title','reach']])
                    
                        with article_list_ave:
                            st.write("article_list_ave")
                            top_articles_by_ave = calc.get_top_articles_by_ave()

                            st.table(top_articles_by_ave[['pubDate','title','AVE']])


                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")


                    media_type_word_cloud_row = st.container()
                    media_type, word_cloud= st.columns([1,1])

                    with media_type_word_cloud_row:
                        with media_type:
                            st.write("media type chart")

                            media_type_data = calc.get_media_type()

                            fig = ui_utils.get_media_type_graph(media_type_data)

                            if fig:
                                media_graph = st.container()
                                with media_graph:
                                    st.write(fig)

                            media_type_data_expander = st.expander(label="Media type data")
                            

                            with media_type_data_expander:
                                st.write(media_type_data)                            
                        
                        with word_cloud:
                            st.write("word cloud place holder")

                            text = " ".join(i for i in mergedArticles['title'])

                            text_spaced = text.split(" ")

                            word_cloud = WordCloud(width = 400, height = 300,background_color ='white',stopwords = stopwords,min_font_size = 10).generate(text)

                            word_cloud_data = calc.get_word_cloud_data(text)

                            st.image(word_cloud.to_array())


                            word_cloud_data_expander = st.expander(label="Word cloud data")

                            

                            with word_cloud_data_expander:
                                st.write("Word cloud data")
                                st.write(word_cloud_data)                            



                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")

                    
                    top_source_top_themes_row = st.container()
                    top_source , top_themes= st.columns([1,1])

                    with top_source_top_themes_row:
                        with top_source:
                            st.write("Top sources")

                            top5sources = calc.dashboard_view_top_sources()

                            c = st.container()

                            t = top5sources['data']

                            df = pd.DataFrame.from_records(t)

                            with c:
                                try:
                                    fig = px.bar(data_frame=df, y='label', x= 'value')
                                    st.write(fig)
                                except:
                                    st.write("Not sufficient data for plotting.")
                            
                            topsourceChartdata = st.expander(label="Top Source Chart Data")

                            with topsourceChartdata:
                                st.write(top5sources)



                        with top_themes:
                            st.write("Top themes")

                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")

                    
                    outlet_breakdown_top_authors = st.container()
                    outlet_breakdown, top_authors= st.columns([1,1])

                    with outlet_breakdown_top_authors:
                        with outlet_breakdown:
                            st.write("Outlet breakdown")

                            d1 = calc.outlet_breakdown()
                            # Setting labels for items in Chart
                            key = list(d1['data']['online'].keys())
                            value = list(d1['data']['online'].values()) 
                            explode = tuple(0.05 for i in range(len(value)))
                            plt.pie(value, labels=key,autopct='%1.1f%%', pctdistance=0.85,explode=explode)
                            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
                            fig = plt.gcf()
                            fig.gca().add_artist(centre_circle)
                            plt.title(d1['title'])
                            st.write(fig)
                            

                                # Displaying Chart
                                

                        with top_authors:
                            st.write("Top authors")

                            top5authors = calc.dashboard_view_top_authors()

                            c = st.container()

                            t = top5authors['data']

                            df = pd.DataFrame.from_records(t)

                            with c:
                                try:
                                    fig = px.bar(data_frame=df, y='label', x= 'value')
                                    st.write(fig)
                                except:
                                    st.write("_____")
                            
                            topauthorChartdata = st.expander(label="Top author Chart Data")

                            with topauthorChartdata:
                                st.write(top5authors)


                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")

                    
                    geo_breakdown_create_new_db = st.container()
                    geo_breakdown, create_new_db = st.columns([1,1])

                    with geo_breakdown_create_new_db:
                        with geo_breakdown:
                            st.write("geo breakdown")
                            geo_breakdown_us = calc.dashboard_view_geo_breakdown_us()
                            st.write(geo_breakdown_us)

                        with create_new_db:
                            if st.header('Create new dashboard'):
                                st.write('-> Hyperlink to next tab')

                    sep = st.container()
                    with sep:
                        st.write("--------------------------------")



################### EXECUTIVE DASHBOARD END ###############################################
            


                    
##################### Dashboard TAB  start###################################################

with brand_dashboard_tab:

    # initialize 

    brand_dashboard_visible = False

    st.header("AlphametricX Brand Dashboard")
    
    brand_dashboard = st.container()

    with brand_dashboard:
        st.header("Brand dashboard view")


    if mergedArticles.empty:
        st.write("Please make a search")
    else:
        brand_dashboard_visible = True

    if brand_dashboard_visible:
        vol_ana_sent_ana = st.container()

        vol_ana, sent_ana = st.columns([1,1])

        with vol_ana:

            vol_anac1,vol_anac2 = st.columns([1,1])

            with vol_anac1:
                vol_ave = st.container()
                vol_reach = st.container()
                vol_articles = st.container()

                total_reach,total_reach_str = calc.get_total_reach()
                    
                total_ave, total_ave_str = calc.get_total_ave()
                
                total_articles,total_articles_str = calc.convert_to_millions_or_thousands(total_articles)

                vol_articles.metric(label="Total Articles ", value=total_articles_str)



                vol_reach.metric(label="Total Reach ", value=total_reach_str)



                vol_ave.metric(label="Total AVE ", value=total_ave_str)

 
        
            with vol_anac2:
                st.write("shows volume trend w.r.t. previous period.")

            with sent_ana:

                sent_anac1,sent_anac2 = st.columns([1,1])

                with sent_anac1:
                    sent_pos_kpi = st.container()
                    sent_neg_kpi = st.container()
                    sent_neu_kpi = st.container()

                    sentiment_counts = calc.get_total_sentiments(total_articles=total_articles)

                    sent_pos, sent_pos_str = calc.convert_to_millions_or_thousands(sentiment_counts['POS'])

                    sent_neg, sent_neg_str = calc.convert_to_millions_or_thousands(sentiment_counts['NEG'])

                    sent_neu, sent_neu_str = calc.convert_to_millions_or_thousands(sentiment_counts['NEU'])

                    sent_pos_kpi.metric(label="Positive", value=sent_pos_str)
                    sent_neg_kpi.metric(label="Negative", value=sent_neg_str)
                    sent_neu_kpi.metric(label="Neutral", value=sent_neu_str)

            


                with sent_anac2:
                    st.write("shows sentiment trend w.r.t previous period.")

        sent_over_time_coverage_over_time = st.container()

        with sent_over_time_coverage_over_time:

            sent_over_time,coverage_over_time = st.columns([1,1])

            with sent_over_time:
                st.write("Sentiment over time in %")

                sentiment_agg_counts = calc.sentiment_over_time(total_articles)

                # WIP

                fig = ui_utils.get_sentiment_over_time_graph(sentiment_agg_counts)

 
                if fig:
                    st.write(fig)
                else:
                    st.write("----")               


            with coverage_over_time:
                st.write("coverage_over_time")

                try:

                    mentions_agg_counts = calc.results_over_time()

                    fig = ui_utils.results_over_time_graph(mentions_agg_counts)

                except:
                    fig = ''

                if fig:
                    st.write(fig)
                else:
                    st.write("----")

        media_type_dist_reach_over_time =st.container()
        media_type_dist, reach_over_time = st.columns([1,1])

        with media_type_dist_reach_over_time:
            with media_type_dist:
                st.write("Media type")

                media_type_data = calc.get_media_type()

                fig = ui_utils.get_media_type_graph(media_type_data)

                if fig:
                    media_graph = st.container()
                    with media_graph:
                        st.write(fig)

                media_type_data_expander = st.expander(label="Media type data")
                

                with media_type_data_expander:
                    st.write(media_type_data)                            


            with reach_over_time:
                st.write("Reach over time")

                reach_over_time_data = calc.get_reach_over_time()
                

                fig = ui_utils.get_reach_over_time_graph(mergedArticles[['pubDate','reach']])

                st.write(fig)

                reach_over_time_data_expander = st.expander(label="Reach over time")

                # with reach_over_time_data_expander:
                #     st.write(reach_over_time_data)




