import os

from django.conf import settings
import httplib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

from testcases import TestServerTestCase

try:
    import json
except ImportError:
    import simplejson as json


class HTTPTestCase(TestServerTestCase):
    def setUp(self):
        self.start_test_server(address='localhost', port=8001)

    def tearDown(self):
        self.stop_test_server()

    def get_connection(self):
        return httplib.HTTPConnection('localhost', 8001)

    def test_get_list(self):
        connection = self.get_connection()
        connection.request('GET', '/api/v1/filenotes/', headers={'Accept': 'application/json'})
        response = connection.getresponse()
        connection.close()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.read(), '{"meta": {"limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1}, "objects": [{"file": "/media/uploads/test_image1.jpg", "id": "1", "name": "A picture as note", "resource_uri": "/api/v1/filenotes/1/"}]}')

    def test_post_file(self):
        post_obj = {
           'name': 'A new note.',
           'file': open(os.path.join(settings.BASE_PATH, 'files', 'fixtures', 'test_image2.jpg'), "rb")
        }
        
        register_openers()
        datagen, headers = multipart_encode(post_obj)
        
        request = urllib2.Request('http://localhost:8001/api/v1/filenotes/', datagen, headers)
        request.get_method = lambda: 'POST'
        ret = urllib2.urlopen(request)
        #print ret.headers