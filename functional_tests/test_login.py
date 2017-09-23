import re
from django.core import mail
from selenium.webdriver.common.keys import Keys
from functional_tests.base import FunctionalTest

TEST_EMAIL = 'me@domain.com'
SUBJECT_EMAIL = 'Your login link for Superlists'


class TestLogin(FunctionalTest):

    def test_can_get_email_link_to_login(self):
        # John enter the website and notices a form
        # on the navbar telling him to enter an email address
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message on the screen is telling him
        # to check his email in box for a link
        self.wait_for(
            lambda: self.assertIn(
                'Check your email',
                self.browser.find_element_by_tag_name('body').text)
        )

        # He checks his email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT_EMAIL, email.subject)

        # It has a url link in it
        self.assertIn('Please access the following link to access superlists',
                      email.body)
        url_search = re.search('http://.+/.+$', email.body)
        if not url_search:
            self.fail('Url link no found on email body\n%s' % email.body)
        url_link = url_search.group(0)
        self.assertIn(self.live_server_url, url_link)

        # He clicks it
        self.browser.get(url_link)

        # He is logged in to the website
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)
