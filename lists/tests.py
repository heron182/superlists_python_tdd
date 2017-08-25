from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item
# Create your tests here.


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_can_handle_POST_request(self):
        response = self.client.post('/',
                                    data={'item_text': 'New list item'})
        self.assertEqual(Item.objects.count(), 1)
        list_item = Item.objects.first()
        self.assertIn('New list item', list_item.text)

    def test_redirect_after_POST_request(self):
        response = self.client.post('/',
                        data={'item_text': 'New list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_dont_save_item_on_GET_request(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_display_multiple_items(self):
        Item.objects.create(text='First item')
        Item.objects.create(text='Thats the second item')
        response = self.client.get('/')
        self.assertIn('First item', response.content.decode())

class ItemModelTest(TestCase):
    def test_can_save_and_retrieve_items(self):
        first_item = Item()
        first_item.text = 'The first item created'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item created'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item, second_saved_item = saved_items
        self.assertEqual(first_saved_item.text, 'The first item created')
        self.assertEqual(second_saved_item.text, 'The second item created')
