"""
This file is part of Pynav2.

Pynav2 is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pynav2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Pynav2. If not, see <http://www.gnu.org/licenses/lgpl.html>.

Copyright 2018 Sloft http://bitbucket.org/sloft/pynav
"""

import random
import time
import os
import re
from urllib.parse import urljoin, urlparse

from requests import Response
from requests import PreparedRequest
from requests import Session
from bs4 import BeautifulSoup
from pynav2 import useragent as ua


class Browser(object):
    """ Headless programmatic web browser on top of requests and beautifulSoup """
    def __init__(self):
        self.session = Session()
        self.response = Response
        self.request = PreparedRequest
        self.bs = BeautifulSoup
        self.user_agent = ua.firefox_windows
        self.timeout = None  # request timeout
        self.verbose = False  # print additional information if True
        self.history = []  # urls history
        self.session.verify = False  # do not verify HTTPS certificate if False
        self._sleep_time_min = 0.0
        self._sleep_time_max = 0.0
        self._handle_referer = False

    def get(self, url, **kwargs):
        """ call a GET request with url and any requests parameters """
        return self._request('GET', url, **kwargs)

    def head(self, url, **kwargs):
        """ call a HEAD request with url and any requests parameters """
        return self._request('HEAD', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        """ call a POST request with url, dict data and any requests parameters """
        return self._request('POST', url, data, **kwargs)

    def _request(self, method, url: str, data=None, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        self._sleep()

        if not url.startswith('http'):
            url = 'http://' + url  # urllib3 will replace http by https if available on server

        if self._handle_referer and len(self.history) > 0:
            self.referer = self.history[-1]

        if method == 'GET':
            self.response = self.session.get(url, **kwargs)
            self._init_beautifulSoup()
        if method == 'HEAD':
            self.response = self.session.head(url, allow_redirects=True, **kwargs)
        if method == 'POST':
            self.response = self.session.post(url, data, **kwargs)
            self._init_beautifulSoup()

        self.history.append(url)
        self.url = url

        self.request = self.response.request

        self.relative_url = self.url.replace(self.url.split('/')[-1], '')
        up = urlparse(self.url)
        self.base_url = "{scheme}://{netloc}/".format(scheme=up.scheme, netloc=up.netloc)

        return self.response

    def _init_beautifulSoup(self):
        self.bs = BeautifulSoup(self.response.text, features="html.parser")

    def download(self, url: str, path: str=None, filename: str=None, data=None, **kwargs):
        """ download file from url to path (folder)

            this mehtod will try to get the file name by looking at the header Content-disposition or last part of the url

            filename is optional, download to path/filename if filename is set
            data is optional, use a POST request with dict data if data is set"""
        if not url.startswith('http'):
            url = 'http://' + url  # urllib3 will replace by https if available

        filename_tmp, filesize, url = self._extract_file_infos(url, data)
        if filename_tmp is '':
            filename_tmp = url.split('/')[-1]

        # Case root url (http://example.com)
        if filename_tmp is '':
            filename_tmp = 'root.html'

        if filename is None:
            filename = filename_tmp

        if path is None:
            path = os.getcwd()

        if not os.path.isdir(path):
            os.makedirs(path)

        download_path = os.path.join(path, filename)

        kwargs.setdefault('timeout', self.timeout)
        self._sleep()

        if data is not None:
            r = self.session.post(url, stream=True, data=data, **kwargs)
        else:
            r = self.session.get(url, stream=True, **kwargs)

        if self.verbose:
            print("downloading {filename} ({filesize}) to: {download_path}".format(filename=filename, filesize=filesize, download_path=download_path))
        bytes_downloaded = 0
        with open(download_path, 'wb') as fd:
            start_time = time.time()
            for chunk in r.iter_content(chunk_size=512):
                fd.write(chunk)
                bytes_downloaded += len(chunk)
            end_time = time.time()

            elapsed_time = self._convert_seconds(end_time - start_time)

        if self.verbose:
            print('download completed in {0} ({1})'.format(str(elapsed_time), self._humanize_bytes(bytes_downloaded)))

    def set_sleep_time(self, sleep_time_min=0.0, sleep_time_max=0.0):
        """Define time to wait before sending each request
           Random seconds between sleep_time_min and sleep_time_max
           sleep_time_min, sleep_time_max : int or float"""
        self._sleep_time_min = sleep_time_min
        if sleep_time_min > sleep_time_max:
            self._sleep_time_max = sleep_time_min
        else:
            self._sleep_time_max = sleep_time_max

    def get_links(self, href: str=None, class_: str=None, text: str=None, **kwargs):
        """ return a dict of all urls found in the last response
            all parameters are optionals
            href is a regex filter on the link href attribute (<a href="anything inside href attribute"></a>)
            class_ is a filter on the link exact class name attribute (<a class="exact_class"></a>)
            text is a regex filter on the link text (<a>anything inside a tag</a>
            any beautifulSoup.find_all() parameter can be added """
        if href is not None:
            href = re.compile(href)
            kwargs['href'] = href
        if class_ is not None:
            kwargs['class_'] = class_
        if text is not None:
            text = re.compile(text)
            kwargs['string'] = text

        return [self._add_path(link.get('href')) for link in self.bs.find_all('a', **kwargs)]

    def get_images(self, src: str=None, class_: str=None, alt: str=None, **kwargs):
        """ return a dict of all urls of images found in the last response
                    all parameters are optionals
                    src is a regex filter on the image src attribute (<img src="anything inside src attribute" />)
                    class_ is a filter on the image exact class name attribute (<img class="exact_class" />)
                    alt is a regex filter on the image alt attribute (<img alt="anything inside alt attribute" />)
                    any beautifulSoup.find_all() parameter can be added """
        if src is not None:
            src = re.compile(src)
            kwargs['src'] = src
        if class_ is not None:
            kwargs['class_'] = class_
        if alt is not None:
            alt = re.compile(alt)
            kwargs['alt'] = alt

        return [self._add_path(link.get('src')) for link in self.bs.find_all('img', **kwargs)]

    @property
    def text(self):
        """ Return the text of the response if any """
        return self.response.text

    @property
    def json(self):
        """ returns the json-encoded content of the response, if any """
        return self.response.json()

    @property
    def links(self):
        """ return a dict of all urls found in the last response """
        return self.get_links()

    @property
    def images(self):
        """ return a dict of all urls of images found in the last response """
        return self.get_images()

    @property
    def user_agent(self) -> str:
        """ Return the current user agent """
        if 'Referer' in self.session.headers:
            return self.session.headers['User-Agent']
        else:
            return None

    @user_agent.setter
    def user_agent(self, user_agent: str):
        """ Decorator to set the user-agent in request header """
        self.session.headers['User-Agent'] = user_agent

    @property
    def referer(self):
        """ Decorator to get the referer, url of the previous request """
        if 'Referer' in self.session.headers:
            return self.session.headers['Referer']
        else:
            return None

    @referer.setter
    def referer(self, referer: str):
        """ Decorator to set the referer, url of the previous request """
        self.session.headers['Referer'] = referer

    @property
    def handle_referer(self):
        """ Decorator to get the boolean value of the handle_referer attribute """
        return self._handle_referer

    @handle_referer.setter
    def handle_referer(self, handle: bool):
        """ Decorator to set the handle_referer boolean value. Use history to add referer to request header if True """
        self._handle_referer = handle
        if not handle:
            if 'Referer' in self.session.headers:
                self.session.headers.pop('Referer')

    def clear_history(self):
        self.history = []

    def _convert_seconds(self, seconds):
        if seconds < 1.0:
            return 'less than 1 second'

        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            s = '' if hours == 1 else 's'
            return '{hours} hour{s} {minutes} minutes {seconds} seconds'.format(hours=hours, s=s, minutes=minutes, seconds=seconds)
        elif minutes > 0:
            s = '' if minutes == 1 else 's'
            return '{minutes} minute{s} {seconds} seconds'.format(minutes=minutes, s=s, seconds=seconds)
        elif seconds > 1:
            return '{0} seconds'.format(seconds)
        else:  # seconds < 1
            return 'less than 1 second'

    def _extract_file_infos(self, url, data=None):
        filename = ''
        filesize = ''
        if data is not None:
            rh = self.session.post(url, allow_redirects=True, data=data)
            rh.close()
        else:
            rh = self.session.head(url, allow_redirects=True)
        url = rh.url  # real url after redirect ('Location' in headers)
        if 'Content-disposition' in rh.headers:
            content_disposition = rh.headers['Content-disposition']
            res = re.findall('"(.+?)"', content_disposition, re.S)
            if len(res) == 1:
                filename = res[0]
        if 'Content-Length' in rh.headers:
            content_length = rh.headers['Content-Length']
            filesize = self._humanize_bytes(content_length)
        return filename, filesize, url

    def _humanize_bytes(self, nb_bytes, precision=1):
        """Return an humanized string representation of a number of bytes"""
        abbrevs = (
            (1 << 50, 'PB'),
            (1 << 40, 'TB'),
            (1 << 30, 'GB'),
            (1 << 20, 'MB'),
            (1 << 10, 'KB'),
            (1, 'bytes')
        )
        nb_bytes = float(nb_bytes)
        if nb_bytes == 1:
            return '1 byte'
        for factor, suffix in abbrevs:
            if nb_bytes >= factor:
                break
        if suffix == 'bytes':
            precision = 0
        return '{0:.{1}f} {2}'.format(nb_bytes / factor, precision, suffix)

    def _sleep(self):
        sleep_time = random.uniform(self._sleep_time_min, self._sleep_time_max)  # random float
        if sleep_time > 0:
            time.sleep(sleep_time)

    def _add_path(self, url):
        """generate an absolute url from url, internal use"""
        if re.search('://', url):
            return url
        else:
            if re.search('mailto:', url):
                return url
            if url == '':
                return self.base_url
            if url[0] == '/':
                return urljoin(self.base_url, url)
            else:
                return urljoin(self.relative_url, url)
