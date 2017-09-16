from functional_tests.base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR_MSG
from selenium.webdriver.common.keys import Keys
from django.utils.html import escape
import unittest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(
            ".alert-danger")

    def test_cannot_add_empty_item_to_list(self):
        # John visits the website and submit an empty list item
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys(Keys.ENTER)
        # He get an error message saying he can´t add an empty item
        # to a list
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He types a description for the item and hits enter
        # and it works as expected
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('Buy oranges')
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy oranges')

        # John intencionally submits a new empty item
        inputbox = self.browser.find_element_by_id(
            'id_text').send_keys(Keys.ENTER)

        # He gets an error message again saying to correct it
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # He corrects it again
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy oranges')
        self.wait_for_row_in_table('2 - Buy milk')
        self.browser.quit()

    def test_cannot_add_duplicate_items(self):
        # John acces the website and starts a new list
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys('Buy meat')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy meat')

        # He tries to submit a duplicated list item
        self.get_input_box().send_keys('Buy meat')
        self.get_input_box().send_keys(Keys.ENTER)

        # A helpful error message is displayed informing he can´t add
        # a duplicated item
        error = self.wait_for(
            lambda: self.get_error_element())
        self.assertEqual(error.text, DUPLICATE_ITEM_ERROR_MSG)

    def test_error_messages_are_cleared_on_input(self):
        # John starts a new list and enters a duplicate item
        self.browser.get(self.live_server_url)
        self.get_input_box().send_keys('Make pudim')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Make pudim')
        self.get_input_box().send_keys('Make pudim')
        self.get_input_box().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertTrue(
                self.get_error_element().is_displayed()
            ))

        # He starts to to correct it and the error msg immediatly
        # disapear from the screen
        self.get_input_box().send_keys('D')
        self.wait_for(
            lambda: self.assertFalse(
                self.get_error_element().is_displayed()
            ))
