# 🎵 Spotify Playlist Scraper GUI

This Python application allows you to **extract metadata from public Spotify playlists** (like song title, artist, album, release date, and duration) and **save it as a CSV file** — all via an intuitive graphical interface built with Tkinter.

---

## ✨ Features

-   🖱️ Simple GUI to input:
    -   Spotify playlist URL
    -   Desired filename
    -   Destination folder
-   ⚙️ Uses Selenium WebDriver (headless Chrome)
-   💾 Saves the playlist metadata in CSV format
-   🔄 Shows loading dialog while scraping in the background
-   ✅ Alerts on success or failure

---


## 📦 Requirements

Install dependencies using the following:

```bash
pip install -r requirements.txt
```

## requirements.txt

```text
selenium
webdriver-manager
```


## 🚀 How to Run

1. Make sure you have Python 3.7+
2. Clone or download this repository
3. Install dependencies
4. Run the app:
   ``` bash
   python main.py
   ```

---

## 📝 How It Works

1. The GUI collects user input (URL, file name, save path)
2. Launches a headless Chrome browser using Selenium
3. Scrapes song info from the Spotify playlist page
4. Writes the data to a CSV file in the selected location

---

## 🛑 Limitations

-   Only works with **public playlists**
-   May break if Spotify updates its layout (due to reliance on CSS selectors)
-   No authentication – no support for private playlists

---

## 📁 Output Example

```csv
Title,Artist,Album,Release Date,Duration,Image URL
"Let It Happen","Tame Impala","Currents","2015","4:31","https://..."
...
```

---

## 🙋‍♂️ Need Help?

Feel free to open an issue or ask for improvements like:

-   API-based version (Spotify Web API)
-   Advanced filtering or track preview
-   JSON export option

---
# 🎵 Spotify Playlist Song Extractor (Basic Script)

This is a **basic Python script** that uses Selenium to extract song data from a **public Spotify playlist** and saves it to a CSV file.

---

## 🔍 What It Does

- Opens a public Spotify playlist URL using Selenium
- Extracts details for each track:
  - Title
  - Artist
  - Album
  - Release Date
  - Duration
  - Album Art URL
- Saves the extracted data as `feelings_on_loop.csv`


---

## 🚀 How to Use

1. Make sure Python 3.7+ is installed.
2. Install the requirements.
3. Run the script:

```bash
python extract_song.py
```

4. The CSV file `feelings_on_loop.csv` will be saved in the same directory.


---


# 📺 YouTube Playlist Creator from Spotify CSV

This script reads a CSV file (exported from a Spotify playlist) and uses the **YouTube Data API** to:

- Create a new **YouTube playlist**
- Search for each song (by title and artist)
- Add the first matching result (video) to the new playlist

---

## 📦 Features

- Authenticates with your Google account via OAuth 2.0
- Searches and adds up to **50 songs** to a new private YouTube playlist
- Pulls song metadata from a `spotify_playlist_songs.csv` file

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```text
pandas
google-auth-oauthlib
google-api-python-client
```

---

## 🗂 Required Files

* `spotify_playlist_songs.csv`: CSV file with columns: `Title`, `Artist`
* `key.json`: OAuth client secrets file (download from [Google Cloud Console](https://console.cloud.google.com/))

---

## 🚀 How to Run

```bash
python youtube_playlist_importer.py
```

* Authorizes Google account via browser popup.
* Creates a YouTube playlist titled **"Imported Spotify Playlist"**.
* Searches YouTube and adds up to 50 songs.

---

## 📌 Notes

* Make sure the YouTube Data API is **enabled** in your Google Cloud project.
* Playlist privacy is set to `private` by default — you can change this in the code.
* Rate limits and API quota usage are respected by adding a `sleep(1)` between inserts.

