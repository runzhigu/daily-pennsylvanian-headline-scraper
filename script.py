"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor
from bs4 import BeautifulSoup
import requests
import loguru


def scrape_data_point():
    """
    Scrapes headline for the news, sports, and opinion section for the daily pennsylvanian website.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    print('hello')
    req = requests.get("https://www.thedp.com")
    loguru.logger.info(f"Request URL2: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    # Select One title
    if req.ok:
        soup=BeautifulSoup(req.text, "html.parser")

        #using the selector to find the heading for each segment
        selected_news = soup.select_one("#content > div:nth-child(5) > div.col-sm-6.section-news > a.frontpage-link.medium-link.newstop")
        selected_sports = soup.select_one("#content > div:nth-child(5) > div:nth-child(3) > div.row.homepage-row > div:nth-child(1) > div:nth-child(2) > a.frontpage-link.medium-link.font-regular")
        selected_opinion= soup.select_one("#content > div:nth-child(5) > div:nth-child(3) > div.row.homepage-row > div:nth-child(2) > div:nth-child(2) > a.frontpage-link.medium-link.font-regular")

        # join the previous selection together as with a heading and formate
        formatted_text = f"News: {selected_news.text.strip() if selected_news else ''}\n" \
                     f"Sports: {selected_sports.text.strip() if selected_sports else ''}\n" \
                     f"Opinion: {selected_opinion.text.strip() if selected_opinion else ''}"

    return formatted_text

if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
