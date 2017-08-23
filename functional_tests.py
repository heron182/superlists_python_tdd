from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_a_list_and_retrieve_it(self):
        # John hears about the website and go check it up
        self.browser.get('http://127.0.0.1:8000')

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
        time.sleep(1)

        # After hitting enter the page lists
        # "1 - Buy cigarrets" as the first item
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row == '1 - Buy cigarrets' for row in rows))

        # A text box is inviting him to enter another item
        # So he types "Search about French Literature"
        self.fail('Finish the test')

        # The list is once again updated with the new item

        # John notices that a unique url has been generated for
        # his to-do list and there´s a little text explaining about it

        # He visists the url and checks the to-do list is there and saved


if __name__ == '__main__':
    unittest.main(warnings='ignore')
