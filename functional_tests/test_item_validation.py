from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import unittest

class ItemValidationTest(FunctionalTest):
    @unittest.skip
    def cannot_add_empty_item_to_list(self):
        # John visits the website and submit an empty list item

        # He get an error message saying he can´t add an empty item
        # to a list

        # He now type a description for the item and hits enter
        # and it works as expected

        # John intencionally submits a new empty item

        # He gets an error message again saying to correct it

        # He corrects it again
        self.fail('write me')
