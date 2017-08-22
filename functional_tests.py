from selenium import webdriver
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
        self.fail('Finish the test')
        # He´s promptly asked to enter a to-do item

        # He types "Buy cigarrets" into a text box

        # After hitting enter the page lists
        # "1 - Buy cigarrets" as the first item

        # A text box is inviting him to enter another item
        # So he types "Search about French Literature"

        # The list is once again updated with the new item

        # John notices that a unique url has been generated for
        # his to-do list and there´s a little text explaining about it

        # He visists the url and checks the to-do list is there and saved


if __name__ == '__main__':
    unittest.main(warnings='ignore')
