from datetime import datetime as dt
from datetime import timedelta
import configparser
config = configparser.ConfigParser()
config.read('./data_pipe/config.ini')
# print(f"config={config.sections()}")


class data_source:
     
     def __init__(self,attrs={}):

          self.attrs = attrs

          # pre-populate perigon attributes if not specified 
          if not self.attrs:
               self.attrs = dict(config['GP_DEFAULT'])

          # print(">>>>>",self.attrs)



class search_filters: 
     # setting defaults
     # def __init__(self,search_text,time_start=today-7,time_end=today,lang_list=['en'],media_types_list=['online'],loc_list=['us'],source_list=[data_source()]):
     def __init__(self,start_date = '2023-01-01', end_date = '2023-01-02',searchQuery="*",lang_list=['EN'],media_types_list=['print','online'],loc_list=['US'],sources_pref=[],keyword_in_title_include_exclude=None,keyword_in_title=[],no_opinions=False,non_news=False,no_press_release=False, with_less_reach=False):

          self.searchQuery = searchQuery
          
          # If one needs to add buffer of 1 day encompassing the time range
          # a = dt.strptime(start_date, "%Y-%m-%d") - timedelta(days=1)
          # b = dt.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

          # self.start_date = a.strftime("%Y-%m-%d")
          # self.end_date = b.strftime("%Y-%m-%d")

          a = dt.strptime(start_date, "%Y-%m-%d")
          b = dt.strptime(end_date, "%Y-%m-%d")

          self.start_date = a.strftime("%Y-%m-%d")
          self.end_date = b.strftime("%Y-%m-%d")

          
          self.lang_list = lang_list
          self.media_types_list = media_types_list
          self.loc_list = loc_list
          self.sources_pref = sources_pref
          self.keyword_in_title_include_exclude = keyword_in_title_include_exclude
          self.keyword_in_title = keyword_in_title

          self.no_opinions = no_opinions
          self.non_news = non_news
          self.no_press_release = no_press_release
          self.with_less_reach = with_less_reach
          # self.duration = dt.strptime(self.end_date, "%Y-%m-%d") - dt.strptime(self.start_date,"%Y-%m-%d" )
          # self.sum_freq = timeline['sum_freq']
          # self.resample_freq = timeline['resample_freq']
          self.prestored_end_date = dict(config['ES_stats'])['prestored_end_date'].strip("\'")

          if not start_date:
               d = dt.now()

               today_date = d.date()
               #default delta 
               delta = 1
               self.end_date = today_date
               self.end_date = today_date - timedelta(days=1)



# specified as the standard plot data format for 1 D


class search_api_inputs(search_filters):

     def __init__(self, start_date='2023-01-01', end_date='2023-01-02', searchQuery="*", lang_list=['EN'], media_types_list=['print', 'online'], loc_list=['US'], sources_pref=[],keyword_in_title_include_exclude=None,keyword_in_title=[],no_opinions=False,non_news=False,no_press_release=False, with_less_reach=False,search_type="simple", intitated_from_page = "",userID = "123", searchID='XXX'):

          super().__init__(start_date, end_date, searchQuery, lang_list, media_types_list, loc_list, sources_pref,keyword_in_title_include_exclude,keyword_in_title,no_opinions=no_opinions,non_news=non_news,no_press_release=no_press_release,with_less_reach=with_less_reach)
          self.searchID = searchID
          self.search_type = search_type
          self.intitated_from_page = intitated_from_page
          self.userID = userID

class AMXOneD: 

#### ref design from UI team

# {
#   'title': "Results Over Time Line Chart",
#   'subtitle': "Some Description",
#   "summary": { "label": "label", "sublabel": "sublabel" },
#   "data": [
#     { "label": "2023-01-01", "value": 20000 },
#     { "label": "2023-01-02", "value": 25000 },
#     { "label": "2023-01-03", "value": 30000 },
#     { "label": "2023-01-04", "value": 20000 },

#   ],
#   "labels": [
#     {
#       "label": "label",
#       "value": "value",
#       "color": "#E20074",
#     },
#   ],
# }

####

     def __init__(self,title="title", subtitle = "subtitle", summary = {"label": "label", "sublabel": "sublabel" }, data = [{}], labels = [{"label": "label", "value": "value", "color":"color"}] ):

          self.title = title
          self.subtitle = subtitle
          self.summary = summary
          self.data = data
          self.labels = labels




class searched_kpis:
     
     def __init__(self, searchID = "XX", total_articles= 10000, total_sent_counts = {'positive' : 1000, 'negative': 1000, 'neutral' : 1000}, total_reach = 10000, total_ave = 925,vol=10):
          self.searchID = searchID
          self.total_articles = total_articles
          self.total_sent_counts = total_sent_counts
          self.total_reach = total_reach
          self.total_ave = total_ave
          self.vol = vol


     


                    


