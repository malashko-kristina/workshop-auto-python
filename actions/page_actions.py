from playwright.sync_api import Page, expect
import allure


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        with allure.step(f"Переход на URL: {url}"):
            self.page.goto(url)

    def press_on_enter_keyboard_button(self):
        with allure.step("Нажатие на клавишу Enter на физической клавиатуре"):
                self.page.keyboard.press('Enter')

    def check_url(self, expected_url, timeout):
        with allure.step(f"Проверка URL: ожидаемый URL - {expected_url}"):
            expect(self.page).to_have_url(expected_url, timeout=timeout)

    def wait_for_url_change(self, expected_url):
        with allure.step(f"Ожидание изменения URL на {expected_url}"):
            self.page.wait_for_url(expected_url, timeout=30000)

    def check_box(self, selector):
        with allure.step("Проставления флажка в чекбоксе"):
            self.page.check(selector)

    def wait_for_page_load(self):
        with allure.step(f"Ожидание загрузки страницы"):
            self.page.wait_for_load_state("load")


    def click_button(self, selector):
        with allure.step(f"Клик по элементу: {selector}"):
            self.page.click(selector)


    def is_element_present(self, selector):
        with allure.step(f"Проверка видимости элемента: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()


    def is_button_active(self, selector):
        with allure.step(f"Проверка активности кнопки: {selector}"):
            expect(self.page.locator(selector)).to_be_enabled(timeout=30000)


    def input_text(self, selector, text):
        with allure.step(f"Ввод теста '{text}' в элемент: {selector}"):
            self.page.fill(selector, text)

    def input_filtred_text(self, selector, text):
        with allure.step(f"Ввод теста 'FILTRED' в {selector}"):
            self.page.fill(selector, text)

    def wait_for_selector(self, selector):
        with allure.step(f"Ожидаем появления селектора: {selector} на протяжении 1.5 минут"):
            self.page.wait_for_selector(selector, state='visible', timeout=90000)

    def wait_for_disappear_selector(self, selector):
        with allure.step(f"Ожидаем появления селектора: {selector}"):
            self.page.wait_for_selector(selector, state='detached')

    def assert_text_present_on_page(self, text):
        with allure.step(f"Проверка наличия текста '{text}' на странице"):
            expect(self.page).to_have_text(text)


    def assert_text_in_element(self, selector, text):
        with allure.step(f"Проверка наличия текста '{text}' в элементе: {selector}"):
            expect(self.page.locator(selector)).to_have_text(text)


    def assert_element_attribute(self, selector, attribute, value):
        with allure.step(f"Проверка значения '{value}' аттрибута {attribute} элемента: {selector}"):
            expect(self.page.locator(selector)).to_have_attribute(attribute, value)


    def assert_element_hidden(self, selector):
        with allure.step(f"Проверка, что элемент {selector} скрыт"):
            expect(self.page.locator(selector)).to_be_hidden()


    def check_error_text_color(self, selector):
        with allure.step(f"Проверка, что текст ошибки красного цвета"):
            error_element = self.page.locator(selector)
            color = error_element.evaluate('(element) => window.getComputedStyle(element).color')
            return color == "rgb(238, 68, 80)"
