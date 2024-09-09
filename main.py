from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import requests
import os

def download_image(url, save_as):
    os.makedirs('public', exist_ok=True)
    
    file_path = os.path.join('public', save_as)
    
    if os.path.exists(file_path):
        return
    
    response = requests.get(url)
    with open(os.path.join('public', save_as), 'wb') as file:
        file.write(response.content)

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)


driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")


all_films = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

print(len(all_films))

films_links = []

for film in all_films:
    title = film.find_element(By.CLASS_NAME, "ipc-title__text").text
    durations = film.find_element(By.CLASS_NAME, "cli-title-metadata-item").text
    rating = film.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text
    
    poster_img_url = film.find_element(By.CLASS_NAME, "ipc-image").get_attribute("src")
    download_image(poster_img_url, title + ".jpg")

    film_link = film.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute("href")
    films_links.append({
        "title": title,
        "rating": rating,
        "durations": durations,
        "film_link": film_link,
        "poster_img": title + ".jpg"
    })
    print(f"{title} - {rating} - {durations} - {film_link}")


for film in films_links:
    driver.get(film["film_link"])
    film["popularity_rating"] = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid="hero-rating-bar__popularity__score"]'))).text
    stars_wrapper = driver.find_elements(By.CLASS_NAME, 'sc-bfec09a1-5')
    film["stars"] = []
    for star in stars_wrapper:
        film["stars"].append({
            "actor_name": star.find_element(By.CLASS_NAME, 'sc-bfec09a1-1').text,
            "role_name": star.find_element(By.CLASS_NAME, 'title-cast-item__characters-list').text,
        })
    print(film["popularity_rating"])
    print(film["stars"])


with open("films.json", "w") as file:
    json.dump(films_links, file)


driver.quit()