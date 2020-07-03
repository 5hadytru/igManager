from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from secrets import *
import time
import math

class igbot:

    PATH = 'D:/thick/ProgramFiles/chromedriver.exe'

    def __init__(self, email, password):
        self.driver = webdriver.Chrome(self.PATH)
        self.email = email
        self.password = password

    def sign_in(self):
        self.driver.get('https://www.instagram.com/')

        time.sleep(5)

        inputs = self.driver.find_elements_by_css_selector("input")

        emailInput = inputs[0]
        pwInput = inputs[1]

        emailInput.send_keys(self.email)
        pwInput.send_keys(self.password)
        pwInput.send_keys(Keys.ENTER)

        time.sleep(2)

    def follow(self, yourUsername, username, numFollows):

        self.driver.get(f'https://www.instagram.com/{yourUsername}')
        time.sleep(1)
        initialFollowing = int(self.driver.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span'
        ).get_attribute('innerText'))
        
        self.driver.get(f'https://www.instagram.com/{username}')

        time.sleep(2)

        followersButton = self.driver.find_element_by_partial_link_text('followers')
        followersButton.click()

        time.sleep(3)

        # Scroll thru followers to load them
        fBody = self.driver.find_element_by_css_selector("div[class='isgrP']")
        scrolling_times= 10
        scroll=0
        scroll_count = scrolling_times + 5
        while scroll < scroll_count:
            self.driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
            fBody)
            time.sleep(2)
            scroll += 1

        followButtons = self.driver.find_elements_by_tag_name('ul div li div div button')

        privateAcctTally = 0
        nonFollowButtons = 0
        alreadyRequested = 0
        alreadyFollowing = 0

        for i in range(numFollows):
            time.sleep(1)

            if (followButtons[i].get_attribute('innerText') == 'Follow'):

                # Not followed already
                followButtons[i].click()
                time.sleep(1)

                # Log private acct encounter
                if (followButtons[i].get_attribute('innerText') == 'Requested'):
                    privateAcctTally += 1

                ''' Private acct; unfollow
                if (followButtons[i].get_attribute('innerText') == 'Requested'):
                    followButtons[i].click()
                    time.sleep(1)
                    unfollowButton = self.driver.find_element_by_css_selector(
                        'body > div:nth-child(19) > div > div > div > div.mt3GC > button.aOOlW.-Cab_')
                    unfollowButton.click()
                    time.sleep(1)
                    privateAcctTally += 1
                # Not private
                else:
                    successfulFollows += 1
                '''

            # Already requested in the past
            elif (followButtons[i].get_attribute('innerText') == 'Requested'):
                alreadyRequested += 1
                time.sleep(1)
                continue
                '''
                followButtons[i].click()
                time.sleep(1)
                unfollowButton = self.driver.find_element_by_css_selector(
                    'body > div:nth-child(19) > div > div > div > div.mt3GC > button.aOOlW.-Cab_')
                unfollowButton.click()
                time.sleep(1)
                alreadyRequested += 1
                '''

            # Already following
            elif (followButtons[i].get_attribute('innerText') == 'Following'):
                alreadyFollowing += 1
                time.sleep(1)
                continue

            # innerText is not 'Follow' or 'Requested' or 'Following'
            else:
                nonFollowButtons += 1
                time.sleep(1)

        exitButton = self.driver.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button')

        exitButton.click()

        time.sleep(1)

        self.driver.get(f'https://www.instagram.com/{yourUsername}')
        time.sleep(1)
        newFollowing = int(self.driver.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span'
        ).get_attribute('innerText'))
        
        successfulFollows = newFollowing - initialFollowing

        print(f'\n------------------STATS FOR FOLLOW ROUND----------------')
        print(f'{successfulFollows} successful follows')
        print(f'{privateAcctTally} private accounts encountered')
        print(f'{nonFollowButtons} non follow buttons encountered')
        print(f'{alreadyRequested} accounts already requested')
        print(f'{alreadyFollowing} accounts already followed')
        
        time.sleep(3)
    
    def unfollow(self, yourUsername, numUnfollows):

        self.driver.get(f'https://www.instagram.com/{yourUsername}')

        initialFollowing = int(self.driver.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span'
        ).get_attribute('innerText'))

        time.sleep(2)

        followersButton = self.driver.find_element_by_partial_link_text('following')
        followersButton.click()

        time.sleep(3)

        # Scroll thru following to load
        fBody = self.driver.find_element_by_css_selector("div[class='isgrP']")
        scrolling_times = math.ceil(numUnfollows / 10)
        scroll = 0
        scroll_count = scrolling_times + 5
        while scroll < scroll_count:
            self.driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
            fBody)
            time.sleep(2)
            scroll += 1

        unfollowButtons = self.driver.find_elements_by_tag_name('ul div li div div button')

        nonUnfollowButtons = 0

        print(f'\n-----------------STATS FOR UNFOLLOW ROUND---------------')
        print(f'Scrolled {scrolling_times} times')
        print(f'{len(unfollowButtons)} unfollow buttons in view')


        for i in range(numUnfollows):
            if (unfollowButtons[i].get_attribute('innerText') == 'Following'):
                unfollowButtons[i].click()
                time.sleep(1)
                finalUfButton = self.driver.find_element_by_css_selector(
                    'body > div:nth-child(19) > div > div > div > div.mt3GC > button.aOOlW.-Cab_')
                finalUfButton.click()
                time.sleep(1)
            else:
                nonUnfollowButtons += 1
        
        exitButton = self.driver.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button')
        
        exitButton.click()

        time.sleep(1)

        self.driver.refresh()

        newFollowing = int(self.driver.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > span'
        ).get_attribute('innerText'))
        
        successes = newFollowing - initialFollowing

        print(f'{successes} successful unfollows')
        print(f'{nonUnfollowButtons} non unfollow buttons encountered')

        time.sleep(3)


bot = igbot(email=cosmic[0], password=cosmic[1])
bot.sign_in()
bot.unfollow(cosmic[0], 30)
bot.follow(cosmic[0], 'astronomy_eye', 20)
bot.driver.quit()

bot = igbot(email=honua[0], password=honua[1])
bot.sign_in()
bot.unfollow(honua[0], 30)
bot.follow(honua[0], 'nature', 20)
bot.driver.quit()

bot = igbot(email=whips[0], password=whips[1])
bot.sign_in()
bot.unfollow(whips[0], 30)
bot.follow(whips[0], 'cars', 20)
bot.driver.quit()

''' NOTES
  Next steps: test! really don't know why unfollows don't go thru but maybe time will heal
  Starting regular use on Monday 7/6 and creating a bunch of content on Sunday :D
  Cul beanz
'''