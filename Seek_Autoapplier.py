import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

#search_url = 'https://www.seek.co.nz/developer-jobs/in-All-Auckland?classification=1223%2C6304%2C1209%2C6281&savedsearchid=20302785&sortmode=keywordrelevance&subclassification=6222%2C6220%2C6217%2C6218%2C6215%2C6307%2C6313%2C6314%2C6022%2C6028%2C6287%2C6290%2C6297'
search_url = 'https://www.seek.co.nz/Computer-science-graduate-jobs/in-All-Auckland'
application_count = 0

#get user login details from txt file
print('Fetching your log-in details.')
with open('user_details.txt', 'r') as info_file:
    my_email = info_file.readline()
    my_pass = info_file.readline()

#use Google Chrome for web navigation
driver = webdriver.Chrome()

print('Starting up the browser.')
#sign in to Seek by filling out user login details
driver.get('https://www.seek.co.nz/sign-in?')
print('Logging you in... ', end="")
email_field = driver.find_element_by_name('email')
email_field.send_keys(my_email)
pass_field = driver.find_element_by_name('password')
pass_field.send_keys(my_pass)
pass_field.submit()

#wait until the account dropdown menu loads (so that page completes login)
print('finalising...', end="")
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Eadjc1o")))
print('successfully logged in.')

#repeat until all relevant jobs on current page have been applied for
enough_for_now = False
while enough_for_now == False:
    #go to the search of my choice on Seek
    if driver.current_url != search_url:
        driver.get(search_url)

    #find all job listing link elements
    print('Scanning for job listings...', end='')
    time.sleep(3)
    job_link_elements = driver.find_elements_by_class_name('_2iNL7wI')
    job_status_elements = driver.find_elements_by_class_name('eeB1JqX')
    unapplied_elements = driver.find_elements_by_class_name('_1gtdTGw')
    print('detected', len(job_status_elements), 'jobs on this page.')
    print((len(job_status_elements) - len(unapplied_elements)),
          'of these have already been applied for.')
    
    #sift through all job ads on the current page
    #until a suitable one is found
    i=-1
    for element in job_link_elements:
        i+=1
        #skip current ad if the job title contains the word 'senior'
        if 'senior' in element.text.lower():
            continue
        #skip this ad if the job title contains the word '.net'
        if '.net' in element.text.lower():
            continue
        #skip this ad if the job title contains the word 'lead'
        if 'lead' in element.text.lower():
            continue
        #skip this ad if I've already applied for it
        if job_status_elements[i] not in unapplied_elements:
            continue
        job_title = element.text
        break
    
    #if there are no relevant jobs on page to apply for,
    #go to next page and start the while loop again
    if i+1 == len(job_link_elements):
        next_page_button = driver.find_element_by_class_name('bHpQ-bp')
        prev_url = driver.current_url
        next_page_button.click()
        print('Proceeding to the next page of search results.')
        while prev_url == driver.current_url:
            time.sleep(0.5)
        search_url = driver.current_url
        continue
    
    #begin the application process
    print('Checking job:', job_title)
    prev_url = driver.current_url
    element.click()

    #go to the application url for the current job
    while prev_url == driver.current_url:
        time.sleep(0.5)
    split_url = driver.current_url.split('?')
    split_url[0] += '/apply?'
    apply_url = split_url[0]+split_url[1]
    prev_url = driver.current_url
    driver.get(apply_url)

    #check if we've been sent to an external website. If so,
    #save url and move on to the next application
    while prev_url == driver.current_url:
        time.sleep(0.5)
    time.sleep(2)
    if 'www.seek' not in driver.current_url:
        with open('links_for_manual_application.txt', 'a') as links_file:
            links_file.write(driver.current_url + '\n')
        print('Manual application required for this job.')
        print('Link saved to links_for_manual_application.txt.')
        continue
    
    #wait for the cover-letter-selection elements to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'uploadcoverLetter')))
    
    #click the second radio button to submit a typed cover letter
    radio_buttons = driver.find_elements_by_class_name('_28Xfx_T')
    radio_buttons[1].click()
    
    #load in the cover letter and fill in company name + job title
    with open('cover_letter_template.txt', 'r') as cl_file:
        cl = cl_file.read()
    cl = cl.replace('###', job_title)
    company_name = driver.find_element_by_class_name('_2QG7TNq').text
    #filter out extended parts of company names
    if ' - ' in company_name:
        name_sections = company_name.split(' - ')
        company_name = name_sections[0]
    elif ':' in company_name:
        name_sections = company_name.split(':')
        company_name = name_sections[0]
    print('Typing cover letter for', company_name + '.')
    cl = cl.replace('===', company_name)

    #select all text in textarea and replace it with cover letter
    cover_letter_text_field = driver.find_element_by_id('writtenCoverLetter')
    cover_letter_text_field.send_keys(Keys.CONTROL, 'a')
    cover_letter_text_field.send_keys(cl)
    
    #select the first CV from the list of those that I have uploaded to seek
    print('Selecting CV.')
    cv_selector = Select(driver.find_element_by_id('selectedResume'))
    cv_selector.select_by_value('0')

    #wait for confirmation that CV has been uploaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'selectedResume-message')))
    upload_message = driver.find_element_by_id('selectedResume-message')
    while 'attached' not in upload_message.text.lower():
        time.sleep(0.5)

    #submit the application
    print('Submitting application...', end='')
    submit_button = driver.find_element_by_id('submitButton')
    submit_button.click()

    #wait for confirmation of submission
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'applicationSent')))
        print('sent.')
    #if submission unsuccessful (usually due to extra questions asked)
    #ask user to intervene
    except TimeoutException:
        print('This submission requires manual intervention.')
        print('Please submit the application, then press ENTER to continue.')
        input('Press Enter to continue...')

    #keep track of how many applications we have submitted
    application_count += 1
    print()
    print('Application count:', application_count)
    print()

    #un-comment this region to set a maximum number of applications sent:
    #if application_count == 100:
        #enough_for_now = True
        #driver.close()
