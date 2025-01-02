from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import random
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

def login_to_twitter(driver, email, username, password):
    driver.get("https://x.com/login")
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
    email_field.send_keys(email)
    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="İleri"]')))
    next_button.click()
    time.sleep(1)
    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(username)
        next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="İleri"]')))
        next_button.click()
        time.sleep(1)
    except:
        print("Username field not found, moving to password entry")
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)
    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Giriş yap"]')))
    login_button.click()
    time.sleep(5)
    print("Logged into Twitter successfully!")

def get_mentions(driver):
    driver.get("https://x.com/home")
    time.sleep(5)
    mentions = []
    try:
        mentions_containers = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='cellInnerDiv']")))
        for container in mentions_containers:
            try:
                user_link_element = container.find_element(By.XPATH, ".//a[contains(@href,'/status')]")
                tweet_id = user_link_element.get_attribute('href').split('/')[-1]
                user_element = container.find_element(By.XPATH, ".//span[contains(text(),'@')]")
                user_name = user_element.text
                if user_name != f"@{os.getenv('TWITTER_USERNAME')}":
                    # Tweetin metnini al
                    tweet_text_element = container.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
                    tweet_text = tweet_text_element.text
                    mentions.append({'user': user_name, 'id': tweet_id, 'tweet_text': tweet_text})
            except NoSuchElementException:
                print("Skipping mention without tweet link.")
    except Exception as e:
        print(f"Error getting mentions: {e}")
    return mentions

def get_shortened_url(url):
    api_url = f"https://ay.live/api/?api=b43ef575350a7ac2100a85da8c1a1104f2e7e7e8&url={url}"
    payload = {}
    headers = {}
    
    try:
        # Send the POST request to the API
        response = requests.post(api_url, headers=headers, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            shortened_url = response_data.get("shortenedUrl", "https://siteadi.com/")
            return shortened_url
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "An error occurred while shortening the URL."
    except requests.RequestException as e:
        print(f"Error sending request to API: {e}")
        return "An error occurred while communicating with the API."
    

def createReply(tweet_text):
    # Define the API endpoint
    api_url = "https://siteadi.com/api.php"
    
    # Prepare the data to be sent in the POST request
    data = {'tweet': tweet_text}
    
    try:
        # Send the POST request to the API
        response = requests.post(api_url, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the response message from the API response
            response_data = response.json()
            message = response_data.get("message", "Ai Yükleniyor...")
            link = response_data.get("link", "https://siteadi.com/")
            return {"message": message, "link": link}

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return "An error occurred while generating a response."
    except requests.RequestException as e:
        print(f"Error sending request to API: {e}")
        return "An error occurred while communicating with the API."
    
replied_tweets = {}

def reply_to_mention(driver, user_name, tweet_id, tweet_text):
    if tweet_id in replied_tweets:
        return
    
    tweet_url = f"https://x.com/{user_name}/status/{tweet_id}"
    driver.get(tweet_url)
    try:
        # Reply button'ı bul
        reply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='r-4qtqp9 r-yyyyoo r-dnmrzs r-bnwqim r-lrvibr r-m6rgpd r-50lct3 r-1srniue'])[1]"))
        )
        reply_button.click()

        # API'den yanıt mesajını al
        reply_message = createReply(tweet_text)
        reply_message_message = reply_message['message']
        reply_message_link = reply_message['link']
        shortened_url = get_shortened_url(reply_message_link)
        new_tweet = reply_message_message+' || DETAY : '+shortened_url

        # Yanıt mesajını tweet'e yaz
        reply_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
        )
        reply_field.send_keys(new_tweet)

        # Tweet gönder butonunu bul ve tıkla
        tweet_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@data-testid='tweetButton'])[1]"))
        )
        tweet_button.click()
        replied_tweets[tweet_id] = True
    except Exception as e:
        print(f"Error replying to tweet: {e}")


def main():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        login_to_twitter(driver, 'AccountMail', 'AccountUsername', 'AccountPassword')
        time.sleep(5)
        while True:
            try:
                mentions = get_mentions(driver)
                for mention in mentions:
                    user_name = mention['user'].replace("@","")
                    tweet_id = mention['id']
                    tweet_text = mention['tweet_text']
                    target_url = f"https://x.com/{user_name}"
                    reply_to_mention(driver, user_name, tweet_id, tweet_text)
                    random_sleep_time = random.randint(10, 58)
                    time.sleep(random_sleep_time)
            except Exception as e:
                print(f"Inner loop Exception: {e}")
            random_sleep_time = random.randint(200, 400)
            time.sleep(random_sleep_time)
    except Exception as e:
        print(f"Main exception: {e}")
    finally:
        driver.quit()
  

if __name__ == "__main__":
    main()
