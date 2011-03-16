try:
    import json
except ImportError:
    import simplejson as json

from django.contrib.auth.models import User
from django.test import TestCase
from core.tests.mocks import MockRequest
from related_resource.api.resources import NoteResource, UserResource
from related_resource.api.urls import api


class RelatedResourceTest(TestCase):
    urls = 'related_resource.api.urls'
    
    def setUp(self):
        self.user = User.objects.create(username="testy_mctesterson")
    
    def test_cannot_access_user_resource(self):
        resource = api.canonical_resource_for('users')
        request = MockRequest()
        request.GET = {'format': 'json'}
        request.method = 'PUT'
        request.raw_post_data = '{"username": "foobar"}'
        resp = resource.wrap_view('dispatch_detail')(request, pk=self.user.pk)
        
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(User.objects.get(id=self.user.id).username, self.user.username)
    
    def test_related_resource_authorization(self):
        resource = api.canonical_resource_for('notes')
        request = MockRequest()
        request.GET = {'format': 'json'}
        request.method = 'POST'
        request.raw_post_data = '{"content": "The cat is back. The dog coughed him up out back.", "created": "2010-04-03 20:05:00", "is_active": true, "slug": "cat-is-back", "title": "The Cat Is Back", "updated": "2010-04-03 20:05:00", "author": {"id": %s, "username": "foobar"}}' % self.user.id
        
        resp = resource.post_list(request)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(User.objects.get(id=self.user.id).username, self.user.username)

    def test_nested_related_resource_put(self):
        resource = api.canonical_resource_for('mediabit-full')

        request = MockRequest()
        request.GET = {'format': 'json'}
        resp = resource.get_detail(request, pk=1)
        self.assertEqual(resp.status_code, 200)
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['title'], 'Funny Cat Picture')
        self.assertEqual(deserialized['note']['title'], 'First Post!')
        
        # modifying the resource
        deserialized['title'] = 'Very Funny Cat Picture'
        deserialized['note']['title'] = 'Really First Post!'
        serialized = json.dumps(deserialized)

        # test if we can write back the requested resource
        request = MockRequest()
        request.GET = {'format': 'json'}
        request.method = 'PUT'
        request.raw_post_data = serialized
        resp = resource.put_detail(request)
        self.assertEqual(resp.status_code, 204)
        
        request = MockRequest()
        request.GET = {'format': 'json'}
        resp = resource.get_detail(request, pk=1)
        deserialized = json.loads(resp.content)
        self.assertEqual(deserialized['title'], 'Very Funny Cat Picture')
        self.assertEqual(deserialized['note']['title'], 'Really First Post!')