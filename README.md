# Pynav2
## Headless programmatic web browser on top of Requests and Beautiful Soup

### Requirements
Python 3.4+

Unittest tested from Python 3.4 to 3.7

### Installation
If python3 is the default python binary
```bash
pip install pynav2
```
If python2 is the default python binary
```bash
pip3 install pynav2
```
### Licence
GNU LGPLv3 (GNU Lesser General Public License Version 3)

### Interactive mode examples
Required for all examples
```python
from pynav2 import Browser
b = Browser()
```

#### HTTP GET request and print the response
Get http://example.com (use https if available on server)
```python
>>> b.get('example.com')
<Response [200]>
>>> b.text  # alias for b.response.text
'<!DOCTYPE html>\n<html lang="mul" class="no-js">\n<head>\n<meta charset="utf-8">\n<title>example.com</title>...'
```

#### HTTP GET request and print the json response
Get http://example.com/user-agent/json wich return a the json-encoded content of a response if nay
```python
>>> b.get('example.com/user-agent/json')
<Response [200]>
>>> b.json  # alias for b.response.json()
{'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
```

#### HTTP POST request and print the response
```python
>>> data = {'q': 'python'}
>>> b.post('example.com/search', data=data)
<Response [200]>
>>> b.text
'<!DOCTYPE html>\n<html lang="mul" class="no-js">\n<head>\n<meta charset="utf-8">\n<title>example.com</title>...'
```

#### HTTP HEAD request and print headers
```python
>>> b.head('example.com')
<Response [200]>
>>> b.response.headers
{'Server': 'nginx', 'Content-Type': 'text/html; charset=utf-8', 'Content-Length': '48842', 'Age': '3154', 'Connection': 'keep-alive'}
```

#### Get all links
```python
>>> b.get('example.com')
<Response [200]>
>>> b.links
['http://example.com/news', 'http://example.com/forum', 'http://example.com/contact']
>>> for link in b.links:
...   print(link)
...
http://example.com/news
http://example.com/forum
http://example.com/contact

```

#### Filter links
Any beautifulSoup.find_all() parameter can be added, see [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
```python
>>> import re
>>> b.get('example.com')
<Response [200]>
>>> b.get_links(text='Python Events')  # regular expression
>>> b.get_links(class_="jump-link")  # no regular expression for class attribute
>>> b.get_links(href="windows")   # regular expression
>>> b.get_links(title=re.compile('success'))  # manual regular expression
```

#### Get all images
```python
>>> b.get('example.com')
<Response [200]>
>>> b.images
['http://example.com/img/logo.png', 'http://example.com/img/picture.jpg', 'http://there.com/news.gif']
```

#### Filter images
Any beautifulSoup.find_all() parameter can be added, see [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
```python
>>> b.get('example.com')
<Response [200]>
>>> b.get_images(src='logo')  # regular expression
>>> b.get_images(class_='python-logo')  # no regular expression for class attribute
>>> b.get_images(alt='yth')  # regular expression
```

#### Download file
```python
>>> b.verbose=True
>>> b.download('http://example.com/ubuntu-amd64', '/tmp')  # it will follow redirect and look for header content-disposition to find filename
downloading ubuntu-18.04.1-desktop-amd64.iso (1.8 GB) to: /tmp/ubuntu-18.04.1-desktop-amd64.iso
download completed in 12 minutes 5 seconds (1.8 GB)

```

####  Handle referer
```python
>>> b.handle_referer = True
>>> b.get('somewhere.com')
>>> b.get('example.com')  # header will have http://somewhere.com as referer
>>> b.get('there.com')  # header will have http://example.com as referer
```

####  Set referer manually 
```python
>>> b.referer = 'http://www.here.com'
>>> b.get('example.com')
```

####  Set user-agent 
```python
>>> from pynav2 import useragent
>>> b.user_agent = useragent.firefox_linux
>>> b.get('example.com')  # header request will have 'Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0' as User-Agent
>>> b.user_agent = 'my_app/v1.0'
>>> b.get('example.com')  # header request will have my_app/v1.0 as User-Agent 
```

#### Set sleep time before a request 
```python
>>> b.set_sleep_time(0.5, 1.5)  # random x seconds between 0.5 to 1.5 seconds and wait x before each request
>>> b.get('example.com') # wait x seconds before request
```

#### Define request timeout
10 seconds timeout
```python
>>> b.timeout = 10
```

#### Close all opened TCP sessions
```python
>>> b.get('example1.com')
>>> b.get('example2.com')
>>> b.get('example3.com')
>>> b.session.close()
```

#### Set HTTP proxy working with HTTPS request
For SOCKS proxies see [Requests documentation](http://docs.python-requests.org/en/master/user/advanced/#socks)
```python
>>> b.get('https://httpbin.org/ip').json()['origin']
111.111.111.111
>>> proxies = {'https':'10.0.0.0:1234'}
>>> b.get('https://httpbin.org/ip', proxies=proxies).json()['origin']
222.222.222.222
```

#### Get beautifulsoup instance
After a get or post request, Browser.bs (beautifulsoup) is automatically initiated with b.response.text

See [Beautifll Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
```python
>>> b.get('example.com')
>>> b.bs.find_all('a')
```

#### Get requests objects instances

See [Requests documentation](http://docs.python-requests.org/en/master/) 
```python
>>> b.get('example.com')
>>> b.session
>>> b.request
>>> b.response
```

#### Get browser history
```python
>>> b.get('example1.com')
>>> b.get('example2.com')
>>> b.get('example3.com')
>>> print b.history
['example1.com', 'example2.com', 'example3.com']
```
