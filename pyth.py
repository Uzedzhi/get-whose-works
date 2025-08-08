import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import sys

# Настройки
TARGET_URL = "https://1.shkolkovo.online/admin/homework/users"
MAX_NUM=2400
timeout=3

TOKEN = "<my-token>"
CHAT_ID = "<my-chat-id>"


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    response = requests.post(url, params=params)
    return response.json()


def main():
    driver = webdriver.Chrome()

    try:
        driver.get(TARGET_URL)
        cnt = int(input('сколько работ вы хотите взять?\n'))
        count, xprev, x = 0, 0, 0

        while count != MAX_NUM:
            print(f"Попытка #{count}: Проверка обновлений, Статус: ", end='')

            #clicking on filter button
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1)
            current_content = driver.find_element(By.CLASS_NAME, "ant-pagination-total-text").get_attribute('outerHTML')

            a = current_content.split(" ")
            x = int(a[-2])
            if x > 0 and xprev!=x:
                print(f"Обнаружена непроверенная работа!(всего {x} работ)")
                print(f"Беру её к себе через {timeout} секунд")
                send_telegram_message(f"Возьму новую работу через {timeout} секунд")
                time.sleep(timeout)
                try:
                    button = driver.find_element(By.XPATH, "//div[@aria-rowindex='2']//div[@aria-colindex='2']//button")
                    button.click()
                    time.sleep(1)
                    button2 = driver.find_element(By.XPATH, "//div[@role='tabpanel']//div//div//button//span[contains(text(), 'Взять')]")
                    button2.click()
                    print(f"Успешно взял работу, осталось еще {cnt} работы")
                    cnt-=1
                    send_telegram_message(f"Успешно взял работу, осталось еще {cnt} работы")
                except Exception as e:
                    send_telegram_message(f"Ойойой, что-то пошло не так")
                    print(e)
            else: #
                print(f'Работы не обнаружено')
            time.sleep(3)
            xprev = x
            count += 1
            if cnt == 0:
                send_telegram_message("Все работы собраны, завершаю процесс")
                sys.exit(0)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()