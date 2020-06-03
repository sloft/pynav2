import re
import unittest
from pynav2 import Browser as B
from pynav2 import useragent as ua


class UnittestsPynav2(unittest.TestCase):

    def testUserAgentDefault(self):
        url = 'http://0.0.0.0:8080/user-agent'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        self.assertEqual(b.response.json(), {'user-agent': ua.firefox_windows})

    def testUserAgentModified(self):
        url = 'http://0.0.0.0:8080/user-agent'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.user_agent = ua.chrome_linux
        b.get(url)
        b.session.close()
        self.assertEqual(b.response.json(), {'user-agent': ua.chrome_linux})

    def testGetImage(self):
        url = 'http://0.0.0.0:8080/'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        images = b.get_images(src='logo')
        res = ['http://0.0.0.0:8080/static/python-logo.png']
        self.assertListEqual(res, images)

    def testGetImage2(self):
        url = 'http://0.0.0.0:8080'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        images = b.get_images(class_='python-logo')
        res = ['http://0.0.0.0:8080/static/python-logo.png']
        self.assertListEqual(res, images)

    def testGetImage3(self):
        url = 'http://0.0.0.0:8080'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        images = b.get_images(alt='yth')
        res = ['http://0.0.0.0:8080/static/python-logo.png']
        self.assertListEqual(res, images)

    def testReferer(self):
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.handle_referer = True
        self.assertEqual(b.referer, None)
        b.get('http://0.0.0.0:8080/user-agent')
        self.assertEqual(b.referer, None)
        b.get('http://0.0.0.0:8080/')
        self.assertEqual(b.referer, 'http://0.0.0.0:8080/user-agent')
        b.get('http://0.0.0.0:8080/user-agent')
        b.session.close()
        self.assertEqual(b.referer, 'http://0.0.0.0:8080/')

    def testGetLink(self):
        url = 'http://0.0.0.0:8080'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        links = b.get_links(text='Python Events')
        res = ['http://0.0.0.0:8080/events/python-events', 'http://0.0.0.0:8080/events/python-events/past/', 'http://0.0.0.0:8080/events/python-events', 'http://0.0.0.0:8080/events/python-events/past/']
        self.assertListEqual(res, links)

    def testGetLink2(self):
        url = 'http://0.0.0.0:8080'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        links = b.get_links(href="windows")
        res = ['http://0.0.0.0:8080/downloads/windows/', 'http://0.0.0.0:8080/downloads/windows/']
        self.assertListEqual(res, links)

    def testGetLink3(self):
        url = 'http://0.0.0.0:8080'
        b = B()
        b.set_sleep_time(0.1, 0.3)
        b.get(url)
        b.session.close()
        links = b.get_links(title=re.compile('success'))
        res = ['http://0.0.0.0:8080/success-stories/', 'http://0.0.0.0:8080/success-stories/']
        self.assertListEqual(res, links)
