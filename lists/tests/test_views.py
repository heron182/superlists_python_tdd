from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
from django.utils.html import escape


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ViewListTest(TestCase):

    def test_uses_list_templates(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%s/' % list_.id)
        self.assertTemplateUsed(response, 'lists.html')

    def test_pass_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get('/lists/%s/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)

    def test_display_multiple_items(self):
        new_list = List.objects.create()
        Item.objects.create(text='Item one', list=new_list)
        Item.objects.create(text='Item two', list=new_list)
        response = self.client.get('/lists/%s/' % new_list.id)
        self.assertContains(response, '1 - Item one')
        self.assertContains(response, '2 - Item two')

    def test_display_only_items_for_that_list(self):
        new_list = List.objects.create()
        Item.objects.create(text='Item one', list=new_list)
        Item.objects.create(text='Item two', list=new_list)
        other_list = List.objects.create()
        Item.objects.create(text='Item three', list=other_list)
        Item.objects.create(text='Item four', list=other_list)
        response = self.client.get('/lists/%s/' % new_list.id)
        self.assertContains(response, 'Item one')
        self.assertContains(response, 'Item two')
        self.assertNotContains(response, 'Item three')
        self.assertNotContains(response, 'Item four')


class NewListTest(TestCase):

    def test_create_new_list_via_POST_request(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': 'New list item'})
        self.assertEqual(Item.objects.count(), 1)
        list_item = Item.objects.first()
        self.assertIn('New list item', list_item.text)

    def test_redirect_after_POST_request(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': 'New list item'})
        created_list = List.objects.first()
        self.assertRedirects(response, '/lists/%s/' % created_list.id)

    def test_error_message_is_sent_back_to_homepage(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't add an empty item")
        self.assertContains(response, expected_error)

    def test_empty_list_items_for_new_list_is_not_saved(self):
        response = self.client.post('/lists/new',
                                    data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_can_create_new_item_via_POST_in_existing_list(self):
        new_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.post(
            '/lists/%s/' % new_list.id,
            data={'item_text': 'A new item for the list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.post(
            '/lists/%s/' % new_list.id,
            data={'item_text': 'A new item for the list'}
        )
        self.assertRedirects(response, '/lists/%s/' % new_list.id)

    def test_validation_errors_for_existing_list_end_up_on_list_page(self):
        list_ = List.objects.create()
        response = self.client.post('/lists/%s/' % list_.id,
                                    data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        expected_error = escape("You can't add an empty item")
        self.assertContains(response, expected_error)

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%s/' % list_.id)
