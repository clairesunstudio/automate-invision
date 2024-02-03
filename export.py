from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import downloads
import private


class WebScraper:
    DRIVER_PATH = '/usr/local/bin/chromedriver'
    URL = 'https://login.invisionapp.com/auth/sign-in?redirectTo=&redirHash=&origin=v6'
    TIME_OUT = 3

    def __init__(self):
        self.service = Service(executable_path=self.DRIVER_PATH)
        self.options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': private.downloadDir}
        self.options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 30)

    def set_up(self):
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(2000, 1200)
        self.driver.get(self.URL)

    def log_in(self):
        try:
            time.sleep(1)
            self.wait = WebDriverWait(self.driver, self.TIME_OUT)
            emailField = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_email"] | //*[@id="emailAddress"] '
                                                      '| //*[@id="signin_email"]')))
            emailField.send_keys(private.username)
            time.sleep(1)
            pwField = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="password"] | //*[@id="signin_password"]')))
            time.sleep(1)
            pwField.send_keys(private.pw)
            submitButton = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                       '//*[@id="app-shell:feature-root:auth-ui"]/div/div/div/div[3]/div/div/div/form/div[3]/button | //*[@id="app-shell:feature-root:auth-ui"]/div/div/div[1]/div/div/form/div[3]/button')))
            submitButton.click()
            self.driver.find_element_by_css_selector('body').send_keys(Keys.END)
            time.sleep(5)
        except TimeoutException as ex:
            self.shut_down("Exception during login: " + str(ex))

    def scrap_data(self):
        try:
            project_links = self.driver.find_elements_by_xpath('//a[starts-with(@href, "#/projects/boards/")]')
            urls = [url_link.get_attribute('href') for url_link in project_links]
            unique_urls = set(urls)
            exportedProjects = []
            for url in unique_urls:
                print(url)
                self.driver.get(url)
                time.sleep(2)
                self.process_project(wait=self.wait, url=url, exportedProjects=exportedProjects)
            print(len(exportedProjects))
            print(exportedProjects)
            print("good bye!")
            time.sleep(60)
            self.driver.close()
        except TimeoutException as ex:
            self.shut_down("Exception during data scraping: " + str(ex))

    def process_project(self, wait, url, exportedProjects):
        more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="board_actions"]/span/li[1]/a/div/div')))
        more_btn.click()
        time.sleep(1)
        export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="board_actions"]/span/li[1]/ul/li/a')))
        time.sleep(2)
        export_btn.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/a')))
        download_btn.click()
        time.sleep(10)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        windowTitle = self.driver.execute_script("return document.getElementsByTagName('title')[0].text")
        exportedProjects.append(windowTitle.strip())
        self.driver.refresh()

    def shut_down(self, msg):
        self.driver.close()
        raise SystemExit(msg)

    def scrape_website(self):
        self.set_up()
        self.log_in()
        self.scrap_data()


WebScraper().scrape_website()
