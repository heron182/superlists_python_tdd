from django.test import TestCase
from lists.models import Item, List

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
