from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import time, random, datetime

prev_emails = 435

# input() for security / data protection reasons
my_email = input("Please enter your email address:")
my_pw = input("Please enter your password:") 

noti_email = input("Please enter your notification email address:") 
noti_pw = input("Please enter your notification email password:") 

recipient_email = input("Please enter the recipient's email address:") 
subject = "**NEW WORK EMAIL"

# specify the time until the script should run
stop_year = 2022
stop_month = 1
stop_day = 1
stop_hour = 18
stop_min = 21


class Ice_Login:

    def __init__(self, email_id, pw, prev_emails):
        self.email = email_id 
        self.pw = pw
        self.prev_emails = prev_emails

    def get_no_of_emails(self):
        # Step1: get website
        driver = webdriver.Chrome(executable_path="C:/Users/joell/Desktop/chromedriver_win32/chromedriver.exe")
        driver.get("https://mail1.csg-worldwide.com/webmail/#login")

        wait = WebDriverWait(driver, 15)

        # Step2: enter email
        wait.until(EC.element_to_be_clickable((By.NAME, 'email-address'))).send_keys(self.email)  
        # click next
        driver.find_element(By.NAME, "next").click()

        # Step3: enter pw
        wait.until(EC.element_to_be_clickable((By.NAME, 'password'))).send_keys(self.pw)  
        # click next
        driver.find_element(By.NAME, "next").click()

        # Step4: scrape html title from logged in page
        try:
            WebDriverWait(driver, 30).until(EC.title_contains("Inbox"))
            self.title = driver.title
            print(self.title)
        except TimeoutException:
            print("Loading took too long.")
            self.title = None

        # Step5: close browser and terminate the WebDriver session 
        """
        If we do not use quit() at the end of program, the WebDriver session will not be closed properly and
        the files will not be cleared off memory. This may result in memory leak errors.
        """
        driver.quit()

        return int(self.title.split()[1][3:-1])

    # Step6: Check if email count increased
    def check_email_count(self, new_email_count):
        if self.title:
            if new_email_count > self.prev_emails:
                return True
            else:
                return False
        else:
            return False


class Gmail_Login:

    def __init__(self, noti_email, noti_pw, subject, recipient_email):
        self.noti_email = noti_email
        self.noti_pw = noti_pw
        self.subject = subject
        self.recipient_email = recipient_email

    # Step7: if new email came in notify me
    def send_notification(self):
        try:
            driver = webdriver.Chrome(executable_path="C:/Users/joell/Desktop/chromedriver_win32/chromedriver.exe")
            driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
            'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1'+\
            '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')

            driver.implicitly_wait(15)

            # enter username
            loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
            loginBox.send_keys(noti_email)
        
            nextButton = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
            nextButton[0].click()
            
            # enter pw
            passWordBox = driver.find_element_by_xpath(
                '//*[@id ="password"]/div[1]/div / div[1]/input')
            passWordBox.send_keys(noti_pw)
        
            nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
            nextButton[0].click()
        
            # implicity wait after login so everything can load properly
            time.sleep(3)

            # click on compose button
            driver.find_element_by_xpath("//*[contains(text(),'Compose')]").click()
            
            # enter recipient email
            wait = WebDriverWait(driver, 15)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//textarea[1]'))).send_keys(self.recipient_email) 

            # enter subject line
            wait.until(EC.element_to_be_clickable((By.NAME, 'subjectbox'))).send_keys(self.subject) 

            time.sleep(1)
            
            # send notification
            send_button = driver.find_elements_by_class_name("dC")
            send_button[0].click()

            # wait until email is sent
            time.sleep(2)
        except:
            print('Login / sending email failed.')

        driver.quit()
        
# ----------------------------------------------------------------------------------------------------------------------- #
if __name__ == "__main__":
    I = Ice_Login(my_email, my_pw, prev_emails)
    G = Gmail_Login(noti_email, noti_pw, subject, recipient_email)
    idle_time = [25, 27, 33, 35]#[60, 55, 47, 45, 51, 40] # in seconds
    idle_time = [i * 60 for i in idle_time] # convert to minutes
    print(I.prev_emails)

    RUNNING = True

    while RUNNING:    
        new_email_count = I.get_no_of_emails()
        email_received = I.check_email_count(new_email_count)
        if email_received:
            G.send_notification()
            I.prev_emails = new_email_count
            print(I.prev_emails)

        current_time = datetime.datetime.now()
        print(f"Last checked: {current_time.hour}:{current_time.minute}:{current_time.second}")
        
        if current_time > datetime.datetime(year=stop_year, month=stop_month, day=stop_day, hour=stop_hour, minute=stop_min):
            RUNNING = False
            print("Auto notifications script stopped running.")
        else:
            # take a break and check again in 20-30mins
            time.sleep(random.choice(idle_time))
