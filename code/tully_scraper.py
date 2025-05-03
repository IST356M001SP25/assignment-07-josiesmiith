import re
from playwright.sync_api import Playwright, sync_playwright
from code.menuitemextractor import extract_menu_item
from code.menuitem import MenuItem
import pandas as pd
# This is a web scraper for Tully's Good Times menu using Playwright.
# It extracts menu items from the website and saves them to a CSV file.
# The script uses the Playwright library to automate the browser and scrape the data.
# The script is designed to work with the web archive version of the Tully's Good Times menu page.
# The script uses the `extract_menu_item` function to clean and extract relevant information from the scraped text.

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    '''
    Here's a working strategy for the scraper:

  go to 'https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/''
  for each `title` (menu section) selected on the page
    go down two elements to get the element that contains the menu items (its a `<div class="row">` tag)
    for each item in the all the selected `menu` items
      get the text of the item
      call `extract_menu_items` to get a `MenuItem` object
      add the dict version `MenuItem` to a list

   after the for loops, you have a list of dict for all the menu items on the page.
   create a pandas dataframe from the list of dict
   write the dataframe to a CSV file `cache/tullys_menu.csv`
   '''
    extracted_items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_text = title.inner_text()
        print("MENU SECTION:", title_text)
        row = title.query_selector("~ *").query_selector("~ *")
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            extracted_item = extract_menu_item(title_text, item_text)
            print(f"  MENU ITEM: {extracted_item.name}")
            extracted_items.append(extracted_item.to_dict())
    df = pd.DataFrame(extracted_items)
    df.to_csv("cache/tullys_menu.csv", index=False)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)


