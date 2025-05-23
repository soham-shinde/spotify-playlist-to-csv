import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from threading import Thread
import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Scraper logic
def scrape_spotify_playlist(url, playlist_name, save_path, callback):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tracklist-row"]'))
        )

        seen_titles = set()
        songs = []
        last_count = 0
        attempts = 0

        while attempts < 2:
            rows = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
            for row in rows:
                try:
                    title_elem = row.find_element(By.CSS_SELECTOR, '[data-testid="internal-track-link"] div')
                    title = title_elem.text.strip()
                    artist = row.find_element(By.CSS_SELECTOR, 'a[href^="/artist/"]').text.strip()
                    if title + artist in seen_titles:
                        continue

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
                    seen_titles.add(title + artist)

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", title_elem)
                    time.sleep(0.001)
                except Exception:
                    continue

            if len(songs) == last_count:
                attempts += 1
                time.sleep(0.5)
            else:
                last_count = len(songs)
                attempts = 0

        driver.quit()

        if songs:
            file_path = os.path.join(save_path, f"{playlist_name}.csv")
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=songs[0].keys())
                writer.writeheader()
                writer.writerows(songs)
            callback(True, f"✅ Saved {len(songs)} songs to {file_path}")
        else:
            callback(False, "❌ No songs found.")
    except Exception as e:
        callback(False, f"Error: {e}")

# GUI
def create_gui():
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            entry_path.delete(0, tk.END)
            entry_path.insert(0, folder)

    def on_submit():
        url = entry_url.get().strip()
        name = entry_name.get().strip()
        path = entry_path.get().strip()

        if not url or not name or not path:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        loading = tk.Toplevel(root)
        loading.title("Loading")
        tk.Label(loading, text="Scraping playlist, please wait...").pack(padx=20, pady=20)

        def task():
            scrape_spotify_playlist(url, name, path, lambda success, msg: on_done(success, msg, loading))

        Thread(target=task).start()

    def on_done(success, message, dialog):
        dialog.destroy()
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Failed", message)

    root = tk.Tk()
    root.title("Spotify Playlist Scraper")

    tk.Label(root, text="Playlist URL:").grid(row=0, column=0, sticky="e")
    entry_url = tk.Entry(root, width=50)
    entry_url.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Playlist Name:").grid(row=1, column=0, sticky="e")
    entry_name = tk.Entry(root, width=50)
    entry_name.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Save Path:").grid(row=2, column=0, sticky="e")
    entry_path = tk.Entry(root, width=40)
    entry_path.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    browse_btn = tk.Button(root, text="Browse", command=browse_folder)
    browse_btn.grid(row=2, column=2, padx=5)

    submit_btn = tk.Button(root, text="Submit", command=on_submit)
    submit_btn.grid(row=3, column=1, pady=10)

    root.mainloop()

create_gui()
