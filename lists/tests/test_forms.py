from django.test import TestCase
from lists.forms import ItemForm, ExistingItemForm, EMPTY_ERROR_MSG, DUPLICATE_ITEM_ERROR_MSG
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_item_renders_placeholder_and_css(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'][0],
                         EMPTY_ERROR_MSG)

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'item list'})
        form.save(for_list=list_)
        self.assertEqual(List.objects.first(), list_)
        self.assertEqual(Item.objects.count(), 1)


class TestExistingItemForm(TestCase):

    def test_form_item_renders_placeholder_and_css(self):
        list_ = List.objects.create()
        form = ExistingItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):
        list_ = List.objects.create()
        form = ExistingItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'][0],
                         EMPTY_ERROR_MSG)

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ExistingItemForm(for_list=list_, data={'text': 'item list'})
        form.save(for_list=list_)
        self.assertEqual(List.objects.first(), list_)
        self.assertEqual(Item.objects.count(), 1)
