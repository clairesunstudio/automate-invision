from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import downloads
import private

DRIVER_PATH='/usr/local/bin/chromedriver'
#URL = 'https://'+private.org+'.invisionapp.com/spaces/'+private.space
#URL = 'https://projects.invisionapp.com/d/main?origin=v7#/projects'
URL = 'https://login.invisionapp.com/auth/sign-in?redirectTo=&redirHash=&origin=v6'

service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : private.downloadDir}
options.add_experimental_option('prefs', prefs)

#ChromeDriverManager
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Updated
driver = webdriver.Chrome(options=options)

# timeout after 20 seconds
wait  = WebDriverWait(driver, 30)
actions = ActionChains(driver)
driver.set_window_position(0, 0)
driver.set_window_size(2000, 1200)

try:
    driver.get(URL)
    #emailField = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_email"]')))
    emailField = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_email"] | //*[@id="emailAddress"]')))
    emailField.send_keys(private.username)
    #pwField = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_password"]')))
    pwField = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"] | //*[@id="signin_password"]')))
    pwField.send_keys(private.pw)
    #submitButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:auth-ui"]/div/div/div[1]/div/div/form/div[3]/button')))
    submitButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:auth-ui"]/div/div/div/div[3]/div/div/div/form/div[3]/button | //*[@id="app-shell:feature-root:auth-ui"]/div/div/div[1]/div/div/form/div[3]/button')))
    submitButton.click()

    #sort = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[3]/div/div/div/div[2]/div/span')))
    #sort.click()
    #sortAZ = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[3]/div/div/div/div[2]/div/div/div/ul/li[4]/div/div')))
    #sortAZ.click()

    first = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion"]/inv-react-component/div/div/div['
                                                             '2]/div[1]/a[1]')))
    wait = WebDriverWait(driver, timeout=3)
    original_window = driver.current_window_handle
    first.click()

    more_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="board_actions"]/span/li[1]/a/div/div')))
    more_btn.click()
    wait = WebDriverWait(driver, timeout=3)
    export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="board_actions"]/span/li[1]/ul/li/a')))
    wait = WebDriverWait(driver, timeout=3)
    export_btn.click()
    wait = WebDriverWait(driver, timeout=3)
    driver.switch_to.new_window('tab')
    download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/a')))
    wait = WebDriverWait(driver, timeout=3)
    download_btn.click()
    wait = WebDriverWait(driver, timeout=330)
    #windowHomeName = driver.execute_script("return document.getElementsByTagName('title')[0].text")
    #print('window name: '+windowHomeName)



    def exportProject(i):
        project = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[4]/div/div/div/div[1]/div/div/div['+str(i)+']/div/div/article/a')))
        projectURL = project.get_attribute('href')
        projectName = project.get_attribute('aria-label')
        driver.get(projectURL)
        more = lambda: wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/span/button')))
        more().click()
        export = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/div/div/ul/li[5]/div/button')))
        export.click()
        download = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/div/div/ul/li[5]/div/ul/li[3]/div/button')))
        downloadable = download.is_enabled()
        if downloadable:
            ##images zip
            downloadOption = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/div/div/ul/li[5]/div/ul/li[3]/div/button')))
            ##HTML
            # downloadOption = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/div/div/ul/li[5]/div/ul/li[2]/div/button')))
            ##PDF
            # downloadOption = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:prototype-overview"]/div/div/div[1]/div/div[1]/div/section/div[2]/div[1]/div/div/div/ul/li[5]/div/ul/li[1]/div/button')))
            downloadOption.click()
            #downloadHTML.click()
            print("downloaded project_"+str(i) +': '+ projectName)
        else:
            print("Not downloadable project_"+str(i) +': '+ projectName)

        time.sleep(2)
        driver.back()
        time.sleep(2)
        # switch_to_window to the intial window or switch_to default content both didn't work as the current window is not actually active. This fixed the issue
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)



    def getProject(i):
        project =  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[4]/div/div/div/div[1]/div/div/div['+str(i)+']/div')))
        return project

    def getProjectName(i):
        project = getProject(i)
        projectName = project.get_attribute('data-title')
        return projectName

    def archiveProject(i):
        projectMore = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[4]/div/div/div/div[1]/div/div/div['+str(i)+']/div/div/article/div/div[2]')))
        projectMore.click()
        archiveButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[4]/div/div/div/div[1]/div/div/div['+str(i)+']/div/div/article/div/div[2]/div/div/ul/li[4]/div/button')))
        archiveButton.click()
        time.sleep(1)
        confirmButton = driver.find_element_by_xpath('//button[text()="Archive"]')
        confirmButton.click()

    def getProjectType(i):
        project = getProject(i)
        projectType = project.get_attribute('data-type')
        return projectType

    exportedProjects = []

    def checkProject(i, index):
        projectName = getProjectName(i)
        isPrototype = getProjectType(i) == 'prototype'
        # only export the projects that has been exported
        projectNameClean = ''.join(filter(str.isalpha, projectName))
        projectList = downloads.getFileList(private.downloadDir)
        if projectNameClean in projectList or projectName in exportedProjects:
            print(str(index) +': '+ projectName + ' has already been saved.')
            archiveProject(i)
        elif isPrototype:
            exportProject(i)
            exportedProjects.append(projectName)
            print(str(index) +': '+ projectName)
        else:
            print(str(index) +': '+ projectName + ' skipping not prototype')
            archiveProject(i)


    # Set the upper bound to at least twice as many as the estimated total count of the projects.
    for i in range(1, 240):
        project = lambda: wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app-shell:feature-root:home"]/div/section/div[4]/div[4]/div/div/div/div[1]/div/div/div['+str(1)+']/div/div/article/a')))
        projectLink = project()
        driver.execute_script("arguments[0].focus()", projectLink)
        time.sleep(1)
        checkProject(1, i)
        driver.get(driver.current_url)
        time.sleep(2)
        driver.refresh()

    print(len(exportedProjects))
    print(exportedProjects)
    print("good bye!")
    driver.close()

except TimeoutException as ex:
    print(len(exportedProjects))
    print(exportedProjects)
    print("Exception has been thrown." + str(ex))
    driver.close()
