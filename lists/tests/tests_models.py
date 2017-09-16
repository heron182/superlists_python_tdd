from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertIn(item, list_.items.all())

    def test_cant_save_empty_item(self):
        list_ = List.objects.create()
        empty_item = Item.objects.create(list=list_, text='')
        with self.assertRaises(ValidationError):
            empty_item.save()
            empty_item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='meh')
        with self.assertRaises(ValidationError):
            item2 = Item(list=list_, text='meh')
            item2.full_clean()

    def test_CAN_save_same_item_to_different_lists(arg):
        list1_ = List.objects.create()
        list2_ = List.objects.create()
        item1 = Item.objects.create(list=list1_, text='meh')
        item2 = Item(list=list2_, text='meh')
        item2.full_clean()

    def test_str_representation(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='hum')
        self.assertEqual(str(item), 'hum')


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%s/' % list_.id)
