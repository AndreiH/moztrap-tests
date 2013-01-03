#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import MozTrapBasePage


class MozTrapManageProductsPage(MozTrapBasePage):

    _page_title = 'Manage-Products'
    _delete_product_locator = (By.CSS_SELECTOR, '#manageproducts .listitem .controls .action-delete[title="delete %(product_name)s"]')
    _filter_input_locator = (By.ID, 'text-filter')
    _filter_suggestion_locator = (By.CSS_SELECTOR, '#filter .textual .suggest .suggestion[data-type="name"][data-name="%(filter_name)s"]')
    _filter_locator = (By.CSS_SELECTOR, '#filterform .filter-group input[data-name="name"][value="%(filter_name)s"]:checked')
    _filter_remove_locator = (By.XPATH, '//label[@class="onoffswitch"][text()="%(filter_name)s"]')
    _suggestion_dropdown_locator = (By.CSS_SELECTOR, ".textual .suggest li a")

    def go_to_manage_products_page(self):
        self.get_relative_path('/manage/products/')
        self.is_the_current_page

    def delete_product(self, name='Test Product'):
        _delete_locator = (self._delete_product_locator[0], self._delete_product_locator[1] % {'product_name': name})

        self.selenium.find_element(*_delete_locator).click()
        self.wait_for_ajax()

    def filter_products_by_name(self, name):
        _filter_locator = (self._filter_locator[0], self._filter_locator[1] % {'filter_name': name.lower()})
        _filter_suggestion_locator = (self._filter_suggestion_locator[0], self._filter_suggestion_locator[1] % {'filter_name': name})

        self.selenium.find_element(*self._filter_input_locator).send_keys(name)
        self.selenium.find_element(*_filter_suggestion_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_locator))
        self.wait_for_ajax()

    def filter_products_by_name_without_mouse(self, name):
        _filter_locator = (self._filter_locator[0], self._filter_locator[1] % {'filter_name': name.lower()})
        _filter_suggestion_locator = (self._filter_suggestion_locator[0], self._filter_suggestion_locator[1] % {'filter_name': name})

        filter_input_locator = self.selenium.find_element(*self._filter_input_locator)
        filter_input_locator.send_keys(name)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*self._suggestion_dropdown_locator))
        filter_input_locator.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(*_filter_locator))
        self.wait_for_ajax()

    def remove_name_filter(self, name):
        _filter_remove_locator = (self._filter_remove_locator[0], self._filter_remove_locator[1] % {'filter_name': name.lower()})

        self.selenium.find_element(*_filter_remove_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_visible(*_filter_remove_locator))
