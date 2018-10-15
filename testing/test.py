import os
import unittest

from splinter import Browser

from samo.core import db
from samo.models import User, Post, Comment, Role

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
            self.assertTrue(browser.is_text_present('A confirmation email has been sent via email.'))

    def tearDown(self):
        user = db.session.query(User).filter_by(username='test').first()
        db.session.delete(user)
        db.session.commit()


class TestLogin(unittest.TestCase):

    def setUp(self):
        del_user = db.session.query(User).filter_by(username='test').first()

        if del_user:
            db.session.delete(del_user)
            db.session.commit()

        self.user = User(username="test", displayname="test", email="test@test.com", password="test")
        db.session.add(self.user)
        db.session.commit()

    def test_login(self):
        with Browser(headless=HEADLESS) as browser:
            url = f'{SERVER}:{PORT}/auth/login'
            browser.visit(url)
            browser.fill('username', 'test')
            browser.fill('password', 'test')
            button = browser.find_by_id('login-submit')
            button.click()
            self.assertTrue(browser.is_text_present('Logged in successfully as test.'))

    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()


class TestAdd(unittest.TestCase):

    def setUp(self):
        del_user = db.session.query(User).filter_by(username='test').first()

        if del_user:
            db.session.delete(del_user)
            db.session.commit()

        role = Role.query.filter(Role.name == 'Contributor').first_or_404()

        self.user = User(username="test", displayname="test", email="test@test.com", password="test", roles=[role])

        db.session.add(self.user)
        db.session.commit()

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
        db.session.delete(self.user)
        post = db.session.query(Post).filter_by(title='DummyTitle01').first()
        db.session.delete(post)
        db.session.commit()


class TestComments(unittest.TestCase):

    def setUp(self):
        del_user = db.session.query(User).filter_by(username='test').first()

        if del_user:
            db.session.delete(del_user)
            db.session.commit()

        self.user = User(username="test", displayname="test", email="test@test.com", password="test")
        self.post = Post(title="DummyTitle02", content="Hello test", user=self.user, publish=True)
        db.session.add(self.user)
        db.session.add(self.post)
        db.session.commit()
        stored_post = db.session.query(Post).filter_by(title="DummyTitle02").first()
        self.slug = stored_post.slug

    def test_comment(self):
        with Browser(headless=HEADLESS) as browser:
            login_url = f'{SERVER}:{PORT}/auth/login'
            browser.visit(login_url)
            browser.fill('username', 'test')
            browser.fill('password', 'test')
            button = browser.find_by_id('login-submit')
            button.click()

            url = f'{SERVER}:{PORT}/blog/post/' + self.slug
            browser.visit(url)
            browser.find_by_id('content').first.fill('Ana are mere.')
            button = browser.find_by_id('commentadd-submit').first
            button.click()
            browser.visit(url)
            self.assertTrue(browser.is_text_present("test"))

    def tearDown(self):
        db.session.query(Comment).filter_by(comment_user=self.user).delete()
        db.session.delete(self.post)
        db.session.delete(self.user)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
