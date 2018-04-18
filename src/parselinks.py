from selenium import webdriver
from src.common import *
from src.util import *


def parse_ladders(driver, ladder_root, ladder_array, ladder_map, data_questions_maps):
    print("[In Progress] Start parsing the ladders.")
    for index in ladder_array:
        ladder_site = ladder_root + "/" + str(index)
        ladder_name = ladder_map[index]
        questions_links = {}
        parse_ladder_questions(ladder_site, ladder_name, driver, questions_links)
        data_questions_maps[index] = questions_links


def parse_ladder_questions(site, ladder_name, driver, question_links):
    print("[In Progress] Parsing out the ladder: " + ladder_name)
    driver.get(site)
    time.sleep(5)
    sections = driver.find_elements_by_class_name("ant-card-body")
    required = driver.find_elements_by_xpath("//*[contains(text(), 'Required')]")
    optional = driver.find_elements_by_xpath("//*[contains(text(), 'Optional')]")
    related = driver.find_elements_by_xpath("//*[contains(text(), 'Related')]")
    # Click over Optional/Related tabs to load those question links on the page
    for index in range(len(required)):
        optional[index].click()
        related[index].click()
    # Loop each section to retrieve the links, last two sections are not questions
    for index in range(len(sections) - 2):
        section_name = sections[index].find_element_by_tag_name('h2').text
        links = sections[index].find_elements_by_tag_name('a')
        link_array = []
        for link in links:
            link_array.append(link.get_attribute('href'))
        question_links[section_name] = link_array


def export_links(question_maps, output_path, ladder_names):
    print("[In Progress] Export the question links to files.")
    for index, dict in question_maps.items():
        ladder_name = ladder_names[index]
        file_name = output_path + '/' + ladder_name.strip() + '.txt'
        file = open(file_name, 'w')
        for section, links in dict.items():
            file.write("# " + section + "\n")
            for link in links:
                file.write(link + "\n")
        file.close()


def parse_links_entry():
    chrome_browser = webdriver.Chrome(WEB_DRIVER_PATH)
    chrome_browser.implicitly_wait(10)
    chrome_browser.get(LINT_CODE_SIGNIN_SITE)
    time.sleep(5)
    if not is_logged_in(chrome_browser):
        login(chrome_browser, LINT_CODE_USER, LINT_CODE_PASS)
    data_questions_maps = {}
    parse_ladders(chrome_browser, LINT_CODE_LADDERS_ROOT, LADDERS_ARRAY, LADDERS_NAME, data_questions_maps)
    # export_links(data_questions_maps, OUTPUT_PATH, LADDERS_NAME)
    chrome_browser.close()

