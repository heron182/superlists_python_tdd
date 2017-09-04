from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class NewVisitorTest(FunctionalTest):
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
