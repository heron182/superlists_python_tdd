from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from django.utils.html import escape
import unittest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_item_to_list(self):
        # John visits the website and submit an empty list item
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys(Keys.ENTER)
        # He get an error message saying he can´t add an empty item
        # to a list
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector('.alert-danger'))
        self.assertEqual(escape(error.text),
                         escape('You can\'t add an empty item'))

        # He types a description for the item and hits enter
        # and it works as expected
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('Buy oranges')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy oranges')

        # John intencionally submits a new empty item
        inputbox = self.browser.find_element_by_id(
            'id_text').send_keys(Keys.ENTER)

        # He gets an error message again saying to correct it
        error = self.wait_for(
            lambda: self.browser.find_element_by_css_selector('.alert-danger'))
        self.assertEqual(escape(error.text),
                         escape('You can\'t add an empty item'))

        # He corrects it again
        inputbox = self.browser.find_element_by_id('id_text')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy oranges')
        self.wait_for_row_in_table('2 - Buy milk')
        self.browser.quit()
