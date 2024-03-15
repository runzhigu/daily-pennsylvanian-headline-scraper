Adjusted the basic scraping template to:

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
