from django.core.urlresolvers import reverse
from rest_framework import status
from django.test import TestCase

from api.models import Post
from extuser.models import MyUser as User

class ModelTest(TestCase):
    """ Tests for API  """
    data = {
        "email": "Django@test.com",
        "first_name": "Django",
        "last_name": "Django",
        "date_of_birth": "1988-12-12",
        "password": "1234",
    }
    user_data = {
        "email" : "test@user.com",
        "first_name" : "test_user",
        "last_name": "test_user_last",
        "date_of_birth" : "2017-01-01",
        "password" : "123456",
    }
    post_data = {
        "title": "New Post",
        "text": "Demo text for this field"
    }
    def setUp(self):
        """Create superuser for all tests """
        self.test_user = User.objects.create_superuser(self.user_data["email"],  self.user_data["date_of_birth"],
                                                  self.user_data["first_name"], self.user_data["last_name"],
                                                  self.user_data["password"])

    def tearDown(self):
        """Delete superuser after all tests"""
        self.test_user.delete()

    def retrieve_passwd(self, email):
        """Return encoded password for requested user"""
        return User.objects.get(email=email).password

    def test_can_register_user(self):
        """ test for /api/v1/register/ [POST]"""
        response = self.client.post(reverse('user-register'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_get_token(self):
        """test for  /api/v1/get-token/ [POST]"""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        user = User.objects.get(email=self.user_data['email'])
        response = self.client.post(reverse('get-token'), {'email':self.user_data['email'],
                                                          'password':self.user_data['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_profile(self):
        """ test for /api/v1/profile/ [GET]"""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = self.user_data.copy()
        data['password'] = self.retrieve_passwd(self.user_data['email'])
        for item in data:
            self.assertEqual(data[item], response.json()['results'][0][item])

        self.client.logout()
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_user_list(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in self.user_data:
            self.assertTrue(item in response.content)

        self.client.logout()
        self.client.login(email=self.data['email'], password=self.data['password'])
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_user_detail(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        user_id = User.objects.get(email=self.user_data['email']).id
        response = self.client.get(reverse('user-detail', kwargs={'pk':user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = self.user_data.copy()
        data['password'] = self.retrieve_passwd(self.user_data['email'])
        for item in data:
            self.assertEqual(data[item], response.json()[item])

        self.client.logout()
        response = self.client.get(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_delete_user(self):
        pass

    def test_can_create_post(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(reverse('post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        response = self.client.post(reverse('post-list'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_post_list(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        self.client.login(email=self.data['email'], password=self.data['password'])
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_post_detail(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(reverse('post-list'), self.post_data)
        post_id = Post.objects.get().id

        response = self.client.get(reverse('post-detail', kwargs={'pk':post_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in self.post_data:
            self.assertEqual(self.post_data[item], response.json()[item])

        self.client.logout()
        response = self.client.get(reverse('post-detail', kwargs={'pk': post_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_users_posts(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        user = User.objects.get(email=self.user_data['email'])
        response = self.client.get(reverse('user-post', kwargs={'userId':user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        response = self.client.get(reverse('user-post', kwargs={'userId': user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




