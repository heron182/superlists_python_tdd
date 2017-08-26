from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
# Create your tests here.


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListItemModelTest(TestCase):
    def test_can_save_and_retrieve_items(self):
        new_list = List()
        new_list.save()

        first_item = Item()
        first_item.text = 'The first item created'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item created'
        second_item.list = new_list
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(List.objects.count(), 1)
        first_saved_item, second_saved_item = saved_items
        self.assertEqual(first_saved_item.text, 'The first item created')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.text, 'The second item created')
        self.assertEqual(second_saved_item.list, new_list)


class ListViewTest(TestCase):

    def test_uses_list_templates(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%s/' % list_.id)
        self.assertTemplateUsed(response, 'lists.html')

    def test_pass_correct_view_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get('/lists/%s/'% correct_list.id)
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


class NewItemTest(TestCase):
    def test_can_create_new_item_via_POST_in_existing_list(self):
        new_list = List.objects.create()
        other_list = List.objects.create()
        self.client.post(
            '/lists/%s/add_item' % new_list.id  ,
            data={'item_text': 'A new item for the list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, new_list)
        self.assertEqual(new_item.text, 'A new item for the list')

    def test_redirects_to_list_view(self):
        new_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.post(
            '/lists/%s/add_item' % new_list.id,
            data={'item_text': 'A new item for the list'}
        )
        self.assertRedirects(response, '/lists/%s/' % new_list.id)
