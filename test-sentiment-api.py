import requests

# The URL of the FastAPI endpoint you want to send the POST request to
url = 'http://54.177.224.58:8000/items/'

# The data you want to send in the request body (JSON format in this example)
data = {
    'a': 'It is the happiest thing to happen! It is the happy thing to happen! It is the not bad thing to happen!',
    'article_number': '123'
}

# Send the POST request
response = requests.post(url, json=data)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    print('POST request succeeded!')
    print(response.json()['articleSentiment'])
else:
    # Request failed
    print(f'POST request failed with status code: {response.status_code}')
