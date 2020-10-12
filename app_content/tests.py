from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model # If used custom user model
from app_content.models import *
from django.core.files import File
import os, json

User = get_user_model()

class ContentTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        # self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.client = APIClient()
        self.user = User.objects.create_user(
        'testuser@user.com',
        'Atul',
        'Rai',
        8879192322,
        'fkjdsf',
        'Mumbai',
        'Mah',
        'India',
        400025,
        '8postUser'
        )
        self.user1 = User.objects.create_user(
        'testuser1@user.com',
        'Atul',
        'Rai',
        8879192322,
        'fkjdsf',
        'Mumbai',
        'Mah',
        'India',
        400025,
        '8postUser'
        )
        self.user2 = User.objects.create_user(
        'testuser2@user.com',
        'Atul',
        'Rai',
        8879192322,
        'fkjdsf',
        'Mumbai',
        'Mah',
        'India',
        400025,
        '8postUser'
        )
        self.admin_user = User.objects.create_superuser(
        "adminuser2@user.com",
        "Atul",
        "Rai",
        8879192322,
        400025,
        "123")
        self.client.force_authenticate(self.user)
        self.create_url = reverse('reg_con_api')

    def create_content(self):
        filename='test.pdf'
        document = File(open(os.path.join(os.getcwd(),'time_table.pdf'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'title': 'Test Title8',
                'body': 'Test body8',
                'summary': 'Test Summary8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content',
                'document':uploaded_file}

        response = self.client.post(self.create_url , data, format='multipart')
        return response
    
    def test_create_content(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon successful creation.

    def test_create_content_without_document(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        filename='test.pdf'
        document = File(open(os.path.join(os.getcwd(),'time_table.pdf'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'title': 'Test Title8',
                'body': 'Test body8',
                'summary': 'Test Summary8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content'}

        response = self.client.post(self.create_url , data, format='multipart')

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Additionally, we want to return the username and email upon successful creation.

    def test_create_content_without_title(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        filename='test.pdf'
        document = File(open(os.path.join(os.getcwd(),'time_table.pdf'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'body': 'Test body8',
                'summary': 'Test Summary8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content',
                'document':uploaded_file}

        response = self.client.post(self.create_url , data, format='multipart')

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Additionally, we want to return the username and email upon successful creation.

    def test_create_content_without_body(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        filename='test.pdf'
        document = File(open(os.path.join(os.getcwd(),'time_table.pdf'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'title': 'Test Title8',
                'summary': 'Test Summary8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content',
                'document':uploaded_file}

        response = self.client.post(self.create_url , data, format='multipart')

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Additionally, we want to return the username and email upon successful creation.
    
    def test_create_content_without_summary(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        filename='test.pdf'
        document = File(open(os.path.join(os.getcwd(),'time_table.pdf'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'title': 'Test Title8',
                'body': 'Test body8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content',
                'document':uploaded_file}

        response = self.client.post(self.create_url , data, format='multipart')

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Additionally, we want to return the username and email upon successful creation.


    def test_create_content_with_any_document_extension(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        filename='test.png'
        document = File(open(os.path.join(os.getcwd(),'test.png'), 'rb'))
        uploaded_file = SimpleUploadedFile(filename, document.read(), content_type='multipart/form-data')
        data = {'title': 'Test Title8',
                'body': 'Test body8',
                'summary': 'Test Summary8',
                'categories': 'hello',
                'categories': 'name',
                'categories': 'test2 content',
                'document':uploaded_file}

        response = self.client.post(self.create_url , data, format='multipart')

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Additionally, we want to return the username and email upon successful creation.

    def test_delete_content_with_id(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.delete(reverse('rud_api', args=(1,)))
        # And that we're returning a 200 created code.
        self.assertEqual(Content.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon successful creation.

    def test_delete_content_with_invalid_id(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.delete(reverse('rud_api', args=(10,)))
        # And that we're returning a 200 created code.
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Additionally, we want to return the username and email upon successful creation.


    def test_delete_content_with_cross_users(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.client.force_authenticate(self.user1)
        response = self.client.delete(reverse('rud_api', args=(1,)))
        # And that we're returning a 200 created code.
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Additionally, we want to return the username and email upon successful creation.


    def test_get_content_with_id(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.get(reverse('rud_api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon successful creation.

    def test_get_content_with_invalid_id(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.get(reverse('rud_api', args=(10,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Additionally, we want to return the username and email upon successful creation.

    def test_get_content_with_cross_users(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('rud_api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Additionally, we want to return the username and email upon successful creation.

    def test_put_content_with_id(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        title = 'Test Title'
        body = 'Test Body'
        summary = 'Test Summary'
        new_data = {'title':title, 'body':body, 'summary':summary}
        response = self.client.put(reverse('rud_api', args=(1,)), new_data, format='multipart')
        con_dict = Content.objects.filter().values()[0]
        self.assertEqual(body, con_dict.get("body"))
        self.assertEqual(summary, con_dict.get("summary"))
        self.assertEqual(title, con_dict.get("title"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon successful creation.

    def test_put_content_with_cross_users(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.client.force_authenticate(self.user1)
        title = 'Test Title'
        body = 'Test Body'
        summary = 'Test Summary'
        new_data = {'title':title, 'body':body, 'summary':summary}
        response = self.client.put(reverse('rud_api', args=(1,)), new_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Additionally, we want to return the username and email upon successful creation.

    def test_contents_through_admin(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """

        response = self.create_content()

        # We want to make sure we have one users in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.user1)
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.client.force_authenticate(self.admin_user)
        ##get all content(user1, user2)
        response = self.client.get(self.create_url)
        print('fijsdfsdjji',len(json.loads(response.content)))
        self.assertEqual(2, len(json.loads(response.content)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ##get by id
        response = self.client.get(reverse('rud_api', args=(1,)))
        self.assertEqual(1, json.loads(response.content).get("1").get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ##put by id
        title = 'Test Title'
        body = 'Test Body'
        summary = 'Test Summary'
        new_data = {'title':title, 'body':body, 'summary':summary}
        response = self.client.put(reverse('rud_api', args=(1,)), new_data, format='multipart')
        con_dict = Content.objects.filter().values()[0]
        self.assertEqual(body, con_dict.get("body"))
        self.assertEqual(summary, con_dict.get("summary"))
        self.assertEqual(title, con_dict.get("title"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ##delete
        response = self.client.delete(reverse('rud_api', args=(1,)))
        # And that we're returning a 200 created code.
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additionally, we want to return the username and email upon successful creation.

    

    def test_search_result(self):
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.user1)
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('search_con_api'), {"q":"Test Title8"})
        resp_data = json.loads(response.content)
        print("asdh", resp_data)
        self.assertEqual(1, len(resp_data))
        self.assertEqual(2, resp_data.get("2").get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.admin_user)

        response = self.client.get(reverse('search_con_api'), {"q":"Test Title8"})
        resp_data = json.loads(response.content)
        print("asdh", resp_data)
        self.assertEqual(2, len(resp_data))
        self.assertEqual(1, resp_data.get("1").get("id"))
        self.assertEqual(2, resp_data.get("2").get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

