from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
import time
import unittest


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+ staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_table(self, row_text):
        MAX_WAIT = 10
        start = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_create_a_list_and_retrieve_it(self):
        # John hears about the website and go check it up
        self.browser.get(self.live_server_url)

        # He notices to-do lists on its header and title
        self.assertIn('To-Do Lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do List', header_text.text)

        # He´s promptly asked to enter a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # He types "Buy cigarrets" into a text box
        inputbox.send_keys('Buy cigarrets')
        inputbox.send_keys(Keys.ENTER)

        # After hitting enter the page lists
        # "1 - Buy cigarrets" as the first item
        self.wait_for_row_in_table('1 - Buy cigarrets')

        # A text box is inviting him to enter another item
        # So he types "Search about French Literature"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Search about French Literature')
        inputbox.send_keys(Keys.ENTER)

        # The list is once again updated with the new item
        self.wait_for_row_in_table('1 - Buy cigarrets')
        self.wait_for_row_in_table('2 - Search about French Literature')

        # John closes the website
        self.browser.quit()

    def test_can_create_multiple_lists_with_unique_urls(self):
        # John visits the website and start creating a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy fruit')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Buy fruit')

        # He notices his list has a unique url
        john_list_url = self.browser.current_url
        self.assertRegex(john_list_url, '/lists/.+')

        # He goes to sleep
        self.browser.quit()

        # Emmon comes along and creates a new list
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # Theres no sign of John´s list on Emmon´s list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1 - Buy fruit', page_text)

        # Emmon types a new item for  it´s list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Do groceries')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1 - Do groceries')

        # Emmon gets his own unique url
        emmon_list_url = self.browser.current_url
        self.assertRegex(emmon_list_url, '/lists/.+')
        self.assertNotEqual(john_list_url, emmon_list_url)

        # Theres no trace of John´s list on the page
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1 - Buy fruit', page_text)

    def test_layout_and_styling(self):
        # John goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


if __name__ == '__main__':
    unittest.main(warnings='ignore')
