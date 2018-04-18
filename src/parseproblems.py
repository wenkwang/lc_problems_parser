import os
from src.common import *
from src.util import *
from selenium import webdriver


def files_exist(path):
    if os.listdir(path) == "":
        return False
    return True


def parse_ladders(browser, files, links_folder, problems_folder):
    print("[In Progress] Start parsing ladders.")
    for file_name in files:
        if file_name[:1] == '.':
            continue
        file_path = links_folder + '/' + file_name
        ladder_folder = problems_folder + '/' + file_name[:-4]
        parse_problems(browser, file_path, ladder_folder)
        # --Test Start--
        break
        # --Test End--


# Parse out the problems of a ladder
def parse_problems(driver, fpath, ladder_root):
    print("[In Progress] Parse the file: " + fpath)
    if not os.path.isdir(ladder_root):
        os.mkdir(ladder_root)
    file = open(fpath, 'r')
    # --Test Start--
    test_count = 0
    # --Test End--
    for line in file:
        # --Test Start--
        test_count += 1
        if test_count > 15:
            break
        # --Test End--
        if line[:1] == '#':
            # Create a sub-folder for each lesson under the ladder
            sub_folder = ladder_root + '/' + line[2:].strip()
            if not os.path.isdir(sub_folder):
                os.mkdir(sub_folder)
            continue
        parse_problem(driver, sub_folder, line)


# Parse out a problem
def parse_problem(driver, folder, link):
    driver.get(link)
    time.sleep(3)
    problem_name = driver.find_element_by_xpath("//a[@id='star']//..").text
    file_path = folder + '/' + problem_name + '.txt'
    # Quit if the problem file exists
    if os.path.isfile(file_path):
        # print("[Warning] File exists already: " + file_path)
        return
    problem_file = open(file_path, 'w')
    extract_problem_desc(problem_file, driver)
    problem_file.write('\n')
    extract_problem_code(problem_file, driver)
    problem_file.close()


# Extract the problem description
def extract_problem_desc(file, driver):
    desc_sec = driver.find_elements_by_xpath("//div[@id='description']/div")
    # If the problem has Challenge section, click it to display the content
    challenge = driver.find_elements_by_css_selector("a[href='#challenge']")
    if len(challenge) > 0:
        challenge[0].click()
    file.write("# Problem Description #\n")
    # Loop each sections of description and write into file
    for index in range(len(desc_sec) - 2):
        if index == 0:
            section = desc_sec[index].find_element_by_tag_name('div')
        else:
            section = desc_sec[index]
        file.write(section.text + '\n')


# Extract the latest accepted code
def extract_problem_code(file, driver):
    file.write("# Solution Code #\n")
    submission_icon = driver.find_element_by_css_selector("a[href^='/submission/?problem_id']")
    submission_icon.click()
    time.sleep(2)
    accepted_link = driver.find_elements_by_link_text('Accepted')
    # Quit if no accepted submission found
    if len(accepted_link) == 0:
        file.write("No accepted code found.\n")
        return
    accepted_link[0].click()
    time.sleep(2)
    code_sections = driver.find_element_by_tag_name('code')
    file.write(code_sections.text + '\n')


def parse_problems_entry():
    if not files_exist(OUTPUT_LINKS_FOLDER):
        print("[Error] No file found under output folder.")
        exit()
    print("[In Progress] Initialize web driver.")
    chrome_browser = webdriver.Chrome(WEB_DRIVER_PATH)
    chrome_browser.implicitly_wait(10)
    chrome_browser.get(LINT_CODE_SIGNIN_SITE)
    time.sleep(5)
    if not is_logged_in(chrome_browser):
        login(chrome_browser, LINT_CODE_USER, LINT_CODE_PASS)
    ladder_files = os.listdir(OUTPUT_LINKS_FOLDER)
    parse_ladders(ladder_files, OUTPUT_LINKS_FOLDER, OUTPUT_PROBLEMS_FOLDER)
    chrome_browser.close()

