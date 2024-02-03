from selenium import webdriver
from seleniumbase import Driver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from telegram import Bot
from telegram import InputMediaPhoto
import schedule
import json

def job_share():
    bot = Bot(token='Your_Bot_Token')
    group_id = 'CHAT_ID'
  # 
    categories = {"Category_1":"img/finance.png","Category_2":"img/marketing.png","Category_3":"img/IT.png","Category_4":"img/administrative.png","Category_5":"img/sales.png","Category_6":"img/design.png",
                "Category_7":"img/law.png","Category_8":"img/education.png","Category_9":"img/industry.png","Category_10":"img/service.png","Category_11":"img/medicine.png","Category_12":"img/different.png"}

    timeSleep = 2
    image_path = 'img/job.png'
    driver = uc.Chrome()
    all_links = []
    old_links= []
    with open('links.json', 'r') as f:
        old_links = json.load(f)
    # 1. STEP Get links
    for i in range(1,3):
        with driver:
            driver.get(f"https://example.com//category?page={i}")
        time.sleep(timeSleep)

        elements = driver.find_elements(By.XPATH, "//a[@class='results-i-link']")
        if not elements:
            break
        for element in elements:
            link = element.get_attribute("href")
            if link in old_links:
                continue
            else:
                all_links.append(link)
    for j in all_links:
        with driver:
            driver.get(j)
        
        category_title = driver.find_element(By.XPATH,"//h1[@class='post-title']").text
        city = driver.find_element(By.XPATH,"//div[contains(@class,'region params-i-val')]").text
        age = driver.find_element(By.XPATH,"//div[contains(@class,'age params-i-val')]").text
        education = driver.find_element(By.XPATH,"//div[contains(@class,'education params-i-val')]").text
        experience = driver.find_element(By.XPATH,"//div[contains(@class,'experience params-i-val')]").text
        email = driver.find_element(By.XPATH,"//div[@class='email params-i-val']/a[contains(text(),'@')]").text
        salary = driver.find_element(By.XPATH,"//span[@class='post-salary salary']").text
        phone_numbers_elements = driver.find_elements(By.XPATH, "//div[@class='phone params-i-val']/a[@class='phone']")
        phone_numbers = "  ".join([phone.text for phone in phone_numbers_elements])

        category_description = driver.find_element(By.XPATH, "//div[@class='post-col']/dd[@class='job_description params-i-val']/p").text
        requirements_elements = driver.find_elements(By.XPATH, "//div[@class='post-col']/dd[@class='requirements params-i-val']/p")
        requirements_text = "\n".join([req.text for req in requirements_elements])
        
        category_name = driver.find_element(By.XPATH,"//div[@class='breadcrumbs']/a[1]").text
        hash_tag_list = category_name.split()
        hash_tag = "#"
        for i in hash_tag_list:
            hash_tag+=i
        
        job_summary = f"<b>{job_title}</b>\n<b>Salary:</b> {salary}\n<b>City:</b> {city} <b>Age:</b> {age} <b>Education:</b> {education}\n<b>Phone:</b> {phone_numbers} <b>Email:</b> {email}  <b>Experience:</b> {experience}\n{hash_tag}"
        job_description_text = f"<b>About</b> \n{job_description}"
        job_requirements_text = f"<b>Requirements</b>\n{requirements_text}"
    
        image_path = categories[category_name]
        with open(image_path, 'rb') as image:
            bot.send_photo(chat_id=group_id, photo=image, caption=job_summary,parse_mode='HTML')
        bot.send_message(chat_id=group_id, text=job_description_text,parse_mode='HTML')
        bot.send_message(chat_id=group_id, text=job_requirements_text,parse_mode='HTML')
        time.sleep(timeSleep)
        old_links.append(j)
    with open('links.json', "w") as outfile:
        json.dump(old_links, outfile)
    driver.quit()
job_share()
def main():
    schedule.every(60).minutes.do(job_share)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
