from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setup Chrome options
options = webdriver.ChromeOptions()

# Launch Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://open.spotify.com/playlist/5opNhqZvwrNuez7XPvaHtv?si=de4bea15ecbd4b28"
driver.get(url)

# Wait for initial load
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tracklist-row"]'))
)

# Scroll step-by-step after each new song is found
seen_titles = set()
songs = []
last_count = 0
attempts = 0

while attempts <2:  # Avoid infinite loop
    rows = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
    for row in rows:
        try:
            title_elem = row.find_element(By.CSS_SELECTOR, '[data-testid="internal-track-link"] div')
            title = title_elem.text.strip()
            artist = row.find_element(By.CSS_SELECTOR, 'a[href^="/artist/"]').text.strip()
            if title+""+artist in seen_titles:
                continue  # Skip duplicates

            album = row.find_element(By.CSS_SELECTOR, 'a[href^="/album/"]').text.strip()
            release_date = row.find_element(By.CSS_SELECTOR, '[aria-colindex="4"]').text.strip()
            duration = row.find_element(By.CSS_SELECTOR, '[aria-colindex="5"] div').text.strip()
            image_url = row.find_element(By.TAG_NAME, 'img').get_attribute('src')

            songs.append({
                "Title": title,
                "Artist": artist,
                "Album": album,
                "Release Date": release_date,
                "Duration": duration,
                "Image URL": image_url
            })
            seen_titles.add(title+""+artist)

            # Scroll after adding each new song
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", title_elem)
            time.sleep(0.001)
        except Exception as e:
            continue

    # Stop if no new songs are added
    if len(songs) == last_count:
        attempts += 1
        time.sleep(0.5)
    else:
        last_count = len(songs)
        attempts = 0

driver.quit()

# Save to CSV
if songs:
    with open("feelings_on_loop.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=songs[0].keys())
        writer.writeheader()
        writer.writerows(songs)
    print(f"✅ Saved {len(songs)} songs to Feelings on Loop.csv")
else:
    print("❌ No songs extracted.")
