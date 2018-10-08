import os
import unittest

from splinter import Browser

from samo.core import DB
from samo.models import User, Post, Comment

os.environ["PATH"] += ';' + os.getcwd() + '\\' + 'assets'

SERVER = 'http://127.0.0.1'
PORT = 5000
HEADLESS = False


class TestSignup(unittest.TestCase):

    def test_signup(self):
        with Browser(headless=HEADLESS) as browser:
            url = f'{SERVER}:{PORT}/auth/signup'
            browser.visit(url)
            browser.fill('username', 'test')
            browser.fill('display_name', 'test')
            browser.fill('email', 'test@test.te')
            browser.fill('password', 'test')
            browser.fill('password2', 'test')
            button = browser.find_by_id('signup-submit')
            button.click()
            self.assertTrue(browser.is_text_present('Welcome, test! Please login.'))

    def tearDown(self):
        user = DB.session.query(User).filter_by(username='test').first()
        DB.session.delete(user)
        DB.session.commit()


class TestLogin(unittest.TestCase):

    def setUp(self):
        del_user = DB.session.query(User).filter_by(username='test').first()

        if del_user:
            DB.session.delete(del_user)
            DB.session.commit()

        self.user = User(username="test", displayname="test", email="test@test.com", password="test")
        DB.session.add(self.user)
        DB.session.commit()

    def test_login(self):
        with Browser(headless=HEADLESS) as browser:
            url = f'{SERVER}:{PORT}/auth/login'
            browser.visit(url)
            browser.fill('username', 'test')
            browser.fill('password', 'test')
            button = browser.find_by_id('login-submit')
            button.click()
            self.assertTrue(browser.is_text_present('Posts by test'))

    def tearDown(self):
        DB.session.delete(self.user)
        DB.session.commit()


class TestAdd(unittest.TestCase):

    def setUp(self):
        del_user = DB.session.query(User).filter_by(username='test').first()

        if del_user:
            DB.session.delete(del_user)
            DB.session.commit()
        self.user = User(username="test", displayname="test", email="test@test.com", password="test")
        DB.session.add(self.user)
        DB.session.commit()

    def test_add(self):
        with Browser(headless=HEADLESS) as browser:
            url = f'{SERVER}:{PORT}/auth/login'
            browser.visit(url)
            browser.fill('username', 'test')
            browser.fill('password', 'test')
            button = browser.find_by_id('login-submit')
            button.click()

            url = f'{SERVER}:{PORT}/blog/add'
            browser.visit(url)
            browser.find_by_id('title').first.fill('DummyTitle01')
            browser.find_by_id('content').first.fill('Ana are mere. Ann has apples. У Анны есть яблоки.')
            browser.find_by_id('s2id_autogen1').first.fill('tag1,tag2,tag3 ')
            title = browser.find_by_tag('h3').first
            title.click()
            button = browser.find_by_id('postadd-submit').first
            button.click()
            self.assertTrue(browser.is_text_present("Stored post 'DummyTitle01'"))

    def tearDown(self):
        DB.session.delete(self.user)
        post = DB.session.query(Post).filter_by(title='DummyTitle01').first()
        DB.session.delete(post)
        DB.session.commit()


class TestComments(unittest.TestCase):

    def setUp(self):
        del_user = DB.session.query(User).filter_by(username='test').first()

        if del_user:
            DB.session.delete(del_user)
            DB.session.commit()

        self.user = User(username="test", displayname="test", email="test@test.com", password="test")
        self.post = Post(title="DummyTitle02", content="Hello test", user=self.user, publish=True)
        DB.session.add(self.user)
        DB.session.add(self.post)
        DB.session.commit()
        stored_post = DB.session.query(Post).filter_by(title="DummyTitle02").first()
        self.slug = stored_post.slug

    def test_comment(self):
        url = f'{SERVER}:{PORT}/blog/post/' + self.slug
        with Browser(headless=HEADLESS) as browser:
            browser.visit(url)
            browser.find_by_id('name').first.fill('DummyPerson01')
            browser.find_by_id('email').first.fill('test@test.te')
            browser.find_by_id('content').first.fill('Ana are mere.')
            button = browser.find_by_id('commentadd-submit').first
            button.click()
            browser.visit(url)
            self.assertTrue(browser.is_text_present("DummyPerson01"))

    def tearDown(self):
        DB.session.query(Comment).filter_by(name='DummyPerson01').delete()
        DB.session.delete(self.post)
        DB.session.delete(self.user)
        DB.session.commit()


if __name__ == '__main__':
    unittest.main()
