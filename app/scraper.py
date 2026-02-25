from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time


def scrape_phone(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)  # allow JS + Cloudflare to load

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        name_tag = soup.select_one("h1.specs-phone-name-title")
        if not name_tag:
            print(f"❌ Blocked even with Selenium: {url}")
            driver.quit()
            return None

        model_name = name_tag.get_text(strip=True)

        specs_section = soup.find("div", id="specs-list")
        if not specs_section:
            driver.quit()
            return None

        release_date = ""
        display = ""
        battery = ""
        camera = ""
        ram = ""
        storage = ""
        price = 0.0

        current_section = ""

        for row in specs_section.find_all("tr"):

            if row.find("th"):
                current_section = row.find("th").get_text(strip=True)
                continue

            key_tag = row.find("td", class_="ttl")
            value_tag = row.find("td", class_="nfo")

            if not key_tag or not value_tag:
                continue

            key = key_tag.get_text(strip=True)
            value = value_tag.get_text(strip=True)

            if current_section == "Launch" and key == "Announced":
                release_date = value

            if current_section == "Display" and key == "Size":
                display = value

            if current_section == "Battery" and key == "Type":
                battery = value

            if current_section == "Memory" and key == "Internal":
                storage = value
                ram_match = re.search(r"(\d+GB)\s*RAM", value)
                if ram_match:
                    ram = ram_match.group(1)

            if current_section == "Main Camera":
                if key.lower() in ["single", "dual", "triple", "quad", "penta"]:
                    camera = value

            if current_section == "Misc" and key == "Price":
                price_match = re.search(r"\$?([\d,]+)", value)
                if price_match:
                    price = float(price_match.group(1).replace(",", ""))

        driver.quit()

        return {
            "model_name": model_name,
            "release_date": release_date,
            "display": display,
            "battery": battery,
            "camera": camera,
            "ram": ram,
            "storage": storage,
            "price": price
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        driver.quit()
        return None