# AlphametricX Search Sandbox

## At top level: 
1.	App1.py : This file calls functions and classes from other modules. 
2.	Searcher.py : It receives the search query and brings the data from ES and live. Then they are merged. It also calls caulculations.py to calculate different fields like reach, ave and so on.
3.	Calculations.py : This includes the field calculations as well as graph data calculations. 
4.	Utils.py: This is a common file that contains general functions used by different modules. 
5.	UI-Utils.py : Not very important, it basically creates charts from the data. 
## Data_pipe : 
This module includes 
1.	Fetcher.py : the file for live search data
2.	ES.py: The file for elastic search data 
3.	Data_structures.py : This includes definitions of the key classes used across the scripts. 

## How to use:
1.	Set up the virtual environment and use requirements1.text for the same. Python version advised is _3.9.6_.
2.   Explicitly install NLP - language model with 

```
python -m spacy download en_core_web_sm 

```

Note: on AWS use python3. 

3.	To run, on command prompt – “streamlit run app1.py”




