import pytest

from samo.config import CONFIG
from samo.core import ENVIRONMENT

SERVER = 'http://' + CONFIG.get('SAMO_HOST', ENVIRONMENT)
PORT = CONFIG.get('SAMO_PORT', ENVIRONMENT)


def test_login(browser, create_contrib_user):
    url = f'{SERVER}:{PORT}/auth/login'
    browser.visit(url)
    browser.fill('username', create_contrib_user.username)
    browser.fill('password', 'test')
    button = browser.find_by_id('login-submit')
    button.click()
    assert browser.is_text_present('Logged in successfully as test_contrib')


@pytest.mark.skip(reason="Currently failing due to splinter bug")
def test_add(browser, create_contrib_user):
    url = f'{SERVER}:{PORT}/auth/login'
    browser.visit(url)
    browser.fill('username', create_contrib_user.username)
    browser.fill('password', 'test')
    button = browser.find_by_id('login-submit')
    button.click()
    url = f'{SERVER}:{PORT}/blog/add'
    browser.visit(url)
    browser.find_by_id('title').first.fill('DummyTitle01')
    browser.find_by_id('content').first.fill('Ana are mere. Ann has apples. У Анны есть яблоки.')
    browser.find_by_id('tags').first.fill('tag1,tag2,tag3 ')
    title = browser.find_by_tag('h3').first
    title.click()
    button = browser.find_by_id('postadd-submit').first
    button.click()
    assert browser.is_text_present("Stored post 'DummyTitle01'")


def test_comments(browser, create_post_edit, create_contrib_user):
    login_url = f'{SERVER}:{PORT}/auth/login'
    browser.visit(login_url)
    browser.fill('username', create_contrib_user.username)
    browser.fill('password', 'test')
    button = browser.find_by_id('login-submit')
    button.click()

    url = f'{SERVER}:{PORT}/blog/post/' + create_post_edit.slug
    browser.visit(url)
    browser.find_by_id('content').first.fill('Ana are mere.')
    button = browser.find_by_id('commentadd-submit').first
    button.click()
    browser.visit(url)
    assert browser.is_text_present("test")


@pytest.mark.skip(reason="Currently failing due to splinter bug")
def test_signup(browser):
    url = f'{SERVER}:{PORT}/auth/signup'
    browser.visit(url)
    browser.fill('username', 'test19233d')
    browser.fill('display_name', 'test')
    browser.fill('email', 'mail@example.com')
    browser.fill('password', 'test')
    browser.fill('password2', 'test')
    button = browser.find_by_id('signup-submit')
    button.click()
    assert browser.is_text_present('A confirmation email has been sent via email.')


def test_edit(browser, create_post_edit, create_contrib_user):
    login_url = f'{SERVER}:{PORT}/auth/login'
    browser.visit(login_url)
    browser.fill('username', create_contrib_user.username)
    browser.fill('password', 'test')
    button = browser.find_by_id('login-submit')
    button.click()

    url = f'{SERVER}:{PORT}/blog/post/' + create_post_edit.slug
    browser.visit(url)
    button = browser.find_by_id('editpost').first
    button.click()
    browser.find_by_id('title').first.fill('111 aaa')
    browser.find_by_id('content').first.fill('222 bbb')
    browser.find_by_id('tags').first.fill('333, ccc')
    button = browser.find_by_id('postadd-submit').first
    button.click()

    assert (browser.is_text_present('111 aaa') and browser.is_text_present('222 bbb') and browser.is_text_present(
        '333'))


def test_delete(browser, create_post_delete, create_contrib_user):
    login_url = f'{SERVER}:{PORT}/auth/login'
    browser.visit(login_url)
    browser.fill('username', create_contrib_user.username)
    browser.fill('password', 'test')
    button = browser.find_by_id('login-submit')
    button.click()

    url = f'{SERVER}:{PORT}/blog/post/' + create_post_delete.slug
    browser.visit(url)
    button = browser.find_by_id('deletepost').first
    button.click()
    button = browser.find_by_id('confirmdelete').first
    button.click()

    assert (browser.is_text_present('Deleted post'))
