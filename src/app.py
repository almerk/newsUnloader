import requests
# url = "https://yandex.ru/news/rubric/computers"
# req = requests.get(url)
# req.encoding,      # returns 'utf-8'
# req.status_code,   # returns 200
# req.elapsed,       # returns datetime.timedelta(0, 1, 666890)
# req.url,           # returns 'https://tutsplus.com/'
 
# req.history      
# # returns [<Response [301]>, <Response [301]>]
 
# req.headers['Content-Type']
# # returns 'text/html; charset=utf-8'
req = requests.get('https://cdn.pixabay.com/photo/2015/03/26/09/40/forest-690058_960_720.jpg', stream=True)
req.raise_for_status()
with open('Forest.jpg', 'wb') as fd:
    for chunk in req.iter_content(chunk_size=50000):
        print('Received a Chunk')
        fd.write(chunk)