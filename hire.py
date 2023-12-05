import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from resume_gpt_evaluator import evaluate_resume

def start(test):
    # 存储登录后状态的cookie  的文件 cookie.pickle
    cookie_pickle = pickle.load(open('cookie.pickle', 'rb'))

    brower = webdriver.Chrome()
    wait = WebDriverWait(brower, 10)

    url = "https://rd6.zhaopin.com/app/search"
    brower.get(url)
    for cookie in cookie_pickle:
        brower.add_cookie({
            "domain": ".zhaopin.com",
            "name": cookie,
            "value": cookie_pickle[cookie],
            "path": '/'
            # "expires": None
        })

    brower.get(url)

    WebDriverWait(brower, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='search-quick-search-new']"))
    )
    chatBox = brower.find_element(By.XPATH,
                                  "//*[@id='root']/div[3]/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div/div/span")
    chatBox.click()

    WebDriverWait(brower, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='rights-count-number']"))
    )
    remaining_xpath = "//span[@class='rights-count-number']"
    remaining_element = brower.find_element(By.XPATH, remaining_xpath)

    remaining = int(remaining_element.text)
    WebDriverWait(brower, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='talent-basic-info__name--inner' and @title]"))
    )

    nameList = brower.find_elements(By.XPATH, "//div[@class='talent-basic-info__name--inner' and @title]")

    if not test:
        count = remaining
    else:
        count = 10
    firstTime = True
    for element in nameList:
        # WebDriverWait(brower, 10).until(EC.element_to_be_clickable(element))
        # element.click()#点击后打开目标hml
        try:
            element = WebDriverWait(brower, 10).until(
                EC.element_to_be_clickable(element)
            )
            ActionChains(brower).move_to_element(element).perform()  # 滚动到元素
            element.click()
        except ElementClickInterceptedException:
            # 使用JavaScript执行点击操作
            brower.execute_script("arguments[0].click();", element)

        # 定位包含所有相关信息的 'div' 元素
        resume_content_xpath = "//div[@class='resume-content__section']"
        resume_content_element = WebDriverWait(brower, 10).until(
            EC.presence_of_element_located((By.XPATH, resume_content_xpath))
        )

        # 提取整个 'div' 的文本
        resume_content_text = resume_content_element.text

        print(resume_content_text)

        # evaluate resume_content_text
        evaluation = evaluate_resume(resume_content_text)

        if evaluation and not test:
            count -= 1
            # 打招呼
            WebDriverWait(brower, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'resume-sidebar__section')]//button[contains(., '打招呼')]"))
            )
            chatBox = brower.find_element(By.XPATH,
                                          "//div[contains(@class, 'resume-sidebar__section')]//button[contains(., '打招呼')]")
            chatBox.click()

            if firstTime:
                # 设置并发送

                WebDriverWait(brower, 20).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@class='km-ripple' and contains(text(), '设置并发送')]"))
                )
                chatBox = brower.find_element(By.XPATH, "//div[@class='km-ripple' and contains(text(), '设置并发送')]")
                chatBox.click()


            # 请选择职位

            WebDriverWait(brower, 20).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[contains(@class, 'km-control km-input is-normal has-icon-suffix km-select') and @placeholder='请选择职位']"))
            )
            chatBox = brower.find_element(By.XPATH,
                                          "//div[contains(@class, 'km-control km-input is-normal has-icon-suffix km-select') and @placeholder='请选择职位']")
            chatBox.click()

            # 置业顾问经理

            WebDriverWait(brower, 20).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//span[contains(@class, 'jsn-job-selector__option--title') and contains(text(), '置业顾问经理')]"))
            )
            chatBox = brower.find_element(By.XPATH,
                                          "//span[contains(@class, 'jsn-job-selector__option--title') and contains(text(), '置业顾问经理')]")
            chatBox.click()

            # 确定

            WebDriverWait(brower, 20).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[contains(@class, 'km-modal km-modal--open km-modal--normal km-modal--no-icon')]//button[contains(., '确定')]"))
            )
            chatBox = brower.find_element(By.XPATH,
                                          "//div[contains(@class, 'km-modal km-modal--open km-modal--normal km-modal--no-icon')]//button[contains(., '确定')]")
            chatBox.click()

            # 我知道了
            if firstTime:
                WebDriverWait(brower, 20).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@class='set-greet-success-modal__btn']//button[contains(., '我知道了')]"))
                )
                chatBox = brower.find_element(By.XPATH,
                                              "//div[@class='set-greet-success-modal__btn']//button[contains(., '我知道了')]")
                chatBox.click()
                firstTime = False

        # 关闭简历详情
        WebDriverWait(brower, 20).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//div[@class='km-modal km-modal--open km-modal--v-centered km-modal--normal km-modal--no-icon km-modal--scrollable']/div[@class='km-modal__header']/button[@class='km-modal__close-btn km-button km-control km-ripple-off km-button--light km-button--plain is-large km-button--square km-button--circle']"))
        )
        WebDriverWait(brower, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[@class='km-modal km-modal--open km-modal--v-centered km-modal--normal km-modal--no-icon km-modal--scrollable']/div[@class='km-modal__header']/button[@class='km-modal__close-btn km-button km-control km-ripple-off km-button--light km-button--plain is-large km-button--square km-button--circle']"))
        )
        chatBox = brower.find_element(By.XPATH,
                                      "//div[@class='km-modal km-modal--open km-modal--v-centered km-modal--normal km-modal--no-icon km-modal--scrollable']/div[@class='km-modal__header']/button[@class='km-modal__close-btn km-button km-control km-ripple-off km-button--light km-button--plain is-large km-button--square km-button--circle']")
        # chatBox.click()
        brower.execute_script("arguments[0].click();", chatBox)

        if (count == 0):
            return True
    return False


done = False
while not done:
    done = start(False)
