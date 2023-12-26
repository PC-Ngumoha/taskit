from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task


class APIBaseTestCase(APITestCase):

    def authenticate(self):
        self.client.post(reverse("user-register"), {
            "email": "test@example.com",
            "password": "testing123#"
        })

        response = self.client.post(reverse("user-login"), {
            "email": "test@example.com",
            "password": "testing123#"
        })

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data.get('token')}")


class TestListCreateTasksView(APIBaseTestCase):

    def test_GET_should_raise_exception_if_no_auth_token(self):
        with self.assertRaises(Exception):
            self.client.get(reverse("tasks"))

    def test_GET_should_return_list_of_tasks(self):
        self.authenticate()
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_POST_should_fail_500_if_no_auth_token(self):
        with self.assertRaises(Exception):
            self.client.post(reverse("tasks"), {
                "title": "test title",
                "details": "details for the provided title"
            })

    def test_POST_should_fail_if_title_field_not_provided(self):
        self.authenticate()
        response = self.client.post(reverse("tasks"), {
            "details": "details for the provided title"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POST_should_fail_if_details_field_not_provided(self):
        self.authenticate()
        response = self.client.post(reverse("tasks"), {
            "title": "test title"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_POST_should_create_new_task(self):
        self.authenticate()
        prev_db_count = Task.objects.all().count()
        response = self.client.post(reverse("tasks"), {
            "title": "test title",
            "details": "details for the provided title"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), prev_db_count + 1)


class TestRetrieveUpdateDestroyTaskView(APIBaseTestCase):

    def test_GET_should_retrieve_specific_task(self):
        self.authenticate()
        payload = {
            "title": "test title",
            "details": "details for the provided title"
        }
        post_response = self.client.post(reverse("tasks"), payload)
        get_response = self.client.get(
            reverse("task", kwargs={'id': post_response.data.get('id')}))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data.get('title'), payload.get('title'))

    def test_PUT_should_update_specific_task(self):
        self.authenticate()
        payload = {
            "title": "test title",
            "details": "details for the provided title"
        }
        post_response = self.client.post(reverse("tasks"), payload)
        new_payload = {
            "title": "new title",
            "details": "details for the provided title"
        }
        task_id = post_response.data.get('id')
        put_response = self.client.put(
            reverse("task", kwargs={'id': task_id}),
            new_payload)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(put_response.data.get(
            'title'), payload.get('title'))
        self.assertEqual(put_response.data.get(
            'title'), new_payload.get('title'))
        self.assertEqual(Task.objects.get(id=task_id).title,
                         new_payload.get('title'))

    def test_PATCH_should_updated_specific_task(self):
        self.authenticate()
        payload = {
            "title": "test title",
            "details": "details for the provided title"
        }
        post_response = self.client.post(reverse("tasks"), payload)
        new_payload = {
            "title": "new title"
        }
        task_id = post_response.data.get('id')
        patch_response = self.client.patch(
            reverse("task", kwargs={'id': task_id}),
            new_payload)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(patch_response.data.get(
            'title'), payload.get('title'))
        self.assertEqual(patch_response.data.get(
            'title'), new_payload.get('title'))
        self.assertEqual(Task.objects.get(id=task_id).title,
                         new_payload.get('title'))

    def test_DELETE_should_delete_a_task_from_DB(self):
        self.authenticate()
        payload = {
            "title": "test title",
            "details": "details for the provided title"
        }
        post_response = self.client.post(reverse("tasks"), payload)
        task_id = post_response.data.get('id')
        delete_response = self.client.delete(
            reverse("task", kwargs={'id': task_id}))
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)
