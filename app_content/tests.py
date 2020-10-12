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
        """
        Helper function to Create Content with all valid fields
        """
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
        Create content with valid fields.
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        # And that we're returning a 200 created code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_content_without_document(self):
        """
        Create document without document field.
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

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 400 bad request code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_content_without_title(self):
        """
        Create content without title
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

        # We want to make sure we have 0 content in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 400 bad request code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_content_without_body(self):
        """
        Create content without body field
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

        # We want to make sure we have zero content in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 400 bad request code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_content_without_summary(self):
        """
        Create content without summary
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

        # We want to make sure we have zero content in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 400 bad request code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_content_with_any_document_extension(self):
        """
        Create content with any document extension except for pdf
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

        # We want to make sure we have zero content in the database..
        self.assertEqual(Content.objects.count(), 0)
        # And that we're returning a 400 bad request code.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_content_with_id(self):
        """
        Delete content with id
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.delete(reverse('rud_api', args=(1,)))
        self.assertEqual(Content.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_content_with_invalid_id(self):
        """
        Delete content with invalid id
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.delete(reverse('rud_api', args=(10,)))
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_content_with_cross_users(self):
        """
        Delete content with non-owner user
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.client.force_authenticate(self.user1)
        response = self.client.delete(reverse('rud_api', args=(1,)))
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_content_with_id(self):
        """
        Get content with id
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.get(reverse('rud_api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_content_with_invalid_id(self):
        """
        Get content with non-existing id
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        response = self.client.get(reverse('rud_api', args=(10,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_content_with_cross_users(self):
        """
        Get content with non-owner users
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        #login with another user
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('rud_api', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_content_with_id(self):
        """
        Edit content with an id
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        title = 'Test Title'
        body = 'Test Body'
        summary = 'Test Summary'
        new_data = {'title':title, 'body':body, 'summary':summary}
        response = self.client.put(reverse('rud_api', args=(1,)), new_data, format='multipart')
        con_dict = Content.objects.filter().values()[0]
        #Check if the response has updated values
        self.assertEqual(body, con_dict.get("body"))
        self.assertEqual(summary, con_dict.get("summary"))
        self.assertEqual(title, con_dict.get("title"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_content_with_cross_users(self):
        """
        Test edit content with the user whose is not owner of the content
        """
        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.client.force_authenticate(self.user1)
        title = 'Test Title'
        body = 'Test Body'
        summary = 'Test Summary'
        new_data = {'title':title, 'body':body, 'summary':summary}
        response = self.client.put(reverse('rud_api', args=(1,)), new_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_contents_through_admin(self):
        """
        Admin will check all the crud operations on content created by different users
        """

        response = self.create_content()

        # We want to make sure we have one content in the database..
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #user1 logs in
        self.client.force_authenticate(self.user1)
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.client.force_authenticate(self.admin_user)
        ##get all content(user1, user2)
        response = self.client.get(self.create_url)
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
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    def test_search_result(self):
        """Search result with 2 user created content and check they do not get fetched at the time of different logged in user"""
        #create content with first user
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #authenticate with another user
        self.client.force_authenticate(self.user1)
        #create content with second user
        response = self.create_content()
        self.assertEqual(Content.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #search the same title name
        response = self.client.get(reverse('search_con_api'), {"q":"Test Title8"})
        resp_data = json.loads(response.content)
        #check if the response has length 1
        self.assertEqual(1, len(resp_data))
        #check if the correct id has been shown
        self.assertEqual(2, resp_data.get("2").get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #authenticate with admin user
        self.client.force_authenticate(self.admin_user)

        response = self.client.get(reverse('search_con_api'), {"q":"Test Title8"})
        resp_data = json.loads(response.content)
        #check the response has both contents for admin user
        self.assertEqual(2, len(resp_data))
        self.assertEqual(1, resp_data.get("1").get("id"))
        self.assertEqual(2, resp_data.get("2").get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

