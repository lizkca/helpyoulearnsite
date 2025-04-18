from django.core.management.base import BaseCommand
from quiz.models import QuizImage
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Command(BaseCommand):
    help = '从百度图片导入常用英语单词的图片'

    def handle(self, *args, **options):
        # 常用100个英语单词
        common_words = [
            "time", "person", "year", "way", "day",
            "thing", "man", "world", "life", "hand",
        ]

        # 设置 requests 的重试策略
        session = requests.Session()
        retries = Retry(total=5,
                       backoff_factor=1,
                       status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # 设置 Chrome 选项
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 直接指定 ChromeDriver 路径
        service = Service('/opt/homebrew/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            for word in common_words:
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        # 访问百度图片
                        driver.get('https://image.baidu.com/')
                        
                        # 等待搜索框出现并输入单词
                        search_box = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.NAME, "word"))
                        )
                        search_box.clear()
                        search_box.send_keys(word)
                        search_box.send_keys(Keys.RETURN)

                        # 等待图片加载
                        time.sleep(3)

                        # 获取第六张图片
                        images = driver.find_elements(By.CSS_SELECTOR, '.imgitem')
                        if len(images) >= 6:
                            img_element = images[5]
                            img_url = img_element.get_attribute('data-thumburl')
                            
                            if img_url:
                                response = session.get(img_url, timeout=10)
                                if response.status_code == 200:
                                    # 创建 QuizImage 对象
                                    quiz_image = QuizImage(
                                        title=word.capitalize(),
                                        description=f"This is a picture of {word}"
                                    )
                                    
                                    # 保存图片
                                    image_name = f"{word}.jpg"
                                    quiz_image.image.save(
                                        image_name,
                                        ContentFile(response.content),
                                        save=True
                                    )
                                    
                                    self.stdout.write(
                                        self.style.SUCCESS(f'Successfully imported image for "{word}"')
                                    )
                        break  # 成功后跳出重试循环
                        
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            self.stdout.write(
                                self.style.ERROR(f'Failed to process "{word}" after {max_retries} attempts: {str(e)}')
                            )
                        else:
                            time.sleep(5)  # 失败后等待更长时间
                
                time.sleep(3)  # 每个单词处理完后的延迟
                
        finally:
            driver.quit()