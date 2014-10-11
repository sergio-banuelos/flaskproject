# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager
from datetime import datetime

from selenium import webdriver


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()


@after.all
def close_browser(total):
    world.browser.quit()


def find_field_by_class(browser, attribute):
    xpath = "//input[@class='%s']" % attribute
    elems = browser.find_elements_by_xpath(xpath)
    return elems[0] if elems else False


@step('I go to "([^"]*)"')
def given_i_go_to_url(step, url):
    world.response = world.browser.get(url)


@step('I fill in field with id "([^"]*)" with "([^"]*)"')
def when_i_fill_in_field_with_id_group1_with_group2(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)


@step('I fill in field with id "([^"]*)" with "([^"]*)"')
def and_i_fill_in_field_with_id_group1_with_group2(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)


@step('I submit the form')
def and_i_submit_the_form(step):
    with AssertContextManager(step):
        form = world.browser.find_element_by_class_name('form-horizontal')
        form.submit()


@step('I do click in the button "([^"]*)"')
def and_i_do_click_in_button(step, field_class):
    with AssertContextManager(step):
        button = world.browser.find_element_by_class_name(field_class)
        button.click()


@step('I see that the element with class "(.*?)" contains "(.*?)"')
def element_contains(step, element_class, value):
    with AssertContextManager(step):
        element = world.browser.find_element_by_class_name(element_class)
        assert (value in element.text), "Got %s, %s " % (element.text, value)


@step('I see that the title of the page contains "([^"]*)"')
def then_i_see_the_title(step, title):
    with AssertContextManager(step):
        element = world.browser.find_element_by_tag_name('h2')
        assert title == element.text, "Got %s " % element.text


@step('I update the field with id "([^"]*)" with "([^"]*)"')
def when_i_update(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)

fechaActual = datetime.now().strftime("%Y-%m-%d %l:%M:%S")
fechaActualComparacion = datetime.now().strftime("%Y-%m-%d")


@step('I update the field with id "([^"]*)" with actual date')
def when_i_update_with_actual_date(step, field_id):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(fechaActual)


@step('I see that the element with class "([^"]*)" contains the actual date')
def then_the_element_with_actual_date(step, element_class):
    with AssertContextManager(step):
        element = world.browser.find_element_by_class_name(element_class)
        assert fechaActualComparacion in element.text, "Got %s " % element.text


@step('I see at least "([^"]*)" appoitments with the class "([^"]*)"')
def then_i_see_two_appoitments(step, num, element_class):
    with AssertContextManager(step):
        elements = world.browser.find_elements_by_class_name(element_class)
        assert len(elements) > int(num)


@step('I select the appointment with the title "([^"]*)"')
def when_i_select_the_appointment_with_the_title(step, title):
    with AssertContextManager(step):
        element = world.browser.find_element_by_link_text(title)
        element.click()


@step('I see that the element with the class "([^"]*)" not contains "([^"]*)"')
def then_the_element_with_the_class_not_contains(step, element_class, title):
    with AssertContextManager(step):
        elements = world.browser.find_elements_by_class_name(element_class)
        lst = []
        for e in elements:
            lst.append(e.text)

        assert title not in lst
