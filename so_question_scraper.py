"""
Project  : StackOverflow Scraper
Author   : Ajeet
Created  : August22023
Description
-----------
Scrapes the first page of StackOverflow questions for a given *tag* and
returns a list of dictionaries, each describing one question.

For every question the scraper collects:

* questionID, title and direct link
* vote, answer and view counts
* tag list
* author information (userID, name, profile link)
* post time
* boolean flag indicating whether an accepted answer exists
"""
from datetime import datetime
from typing import Dict, List
import requests
import bs4

# Constants
BASE_URL = "https://stackoverflow.com"


# Helper Functions
def parse_question(question: bs4.element.Tag) -> Dict[str, str]:
    """
    Convert a single *question summary* block into a dictionary.

    Parameters
    ----------
    question : bs4.element.Tag
        The BeautifulSoup <div> that contains one question on the tag page.

    Returns
    -------
    Dict[str, str]
        Parsed attributes for the question.
    """

    # Unique identifier of the question
    question_id = question.get('data-post-id')

    # Vote / answer / view counts (they come in a fixed order)
    stats_container = question.select('span.s-post-summary--stats-item-number')
    vote_count = stats_container[0].get_text()
    answer_count = stats_container[1].get_text()
    view_count = stats_container[2].get_text()

    # Title text and permalink
    title_tag = question.select_one("h3.s-post-summary--content-title")
    title = title_tag.get_text(strip=True)
    question_link = BASE_URL + question.select_one('h3.s-post-summary--content-title>a').get('href')

    # Tags applied to the question
    tags = [i.get_text() for i in question.select_one('div.s-post-summary--meta-tags').select('li')]

    # Author information
    user_anchor = question.select_one("div.s-user-card--info > div > a")
    user_id = user_anchor.get("href").split("/")[2]
    user_profile = BASE_URL + user_anchor.get("href")
    user_name = user_anchor.get_text(strip=True)

    # Posted date–time (ISO 8601 format in the title attribute)
    post_time = question.select_one('time.s-user-card--time>span').get('title')

    # Whether the question already has an accepted answer
    accepted_answer = bool(
        question.select_one(
            "div.s-post-summary--stats-item.has-answers.has-accepted-answer"
        )
    )

    return {
        "question_id": question_id,
        "vote_count": vote_count,
        "answer_count": answer_count,
        "view_count": view_count,
        "title": title,
        "question_link": question_link,
        "tags": tags,
        "user_id": user_id,
        "user_profile": user_profile,
        "user_name": user_name,
        "post_time": post_time,
        "accepted_answer": accepted_answer,
    }


# Public API
def scrape_questions(tag: str, count=5) -> List[Dict[str, str]]:
    """
        Scrape the first results page for a given StackOverflow *tag*.

        Parameters
        ----------
        tag : str
            The tag to search for (e.g., ``"selenium"``).
        count : trim the number of questions to scrape by count (default is 5)

        Returns
        -------
        List[Dict[str, str]]
            A list of dictionaries—one per question.
        """
    url = f"{BASE_URL }/questions/tagged/{tag}"
    response = requests.get(url)
    response.raise_for_status()  # raise if HTTP status is not 200

    soup = bs4.BeautifulSoup(response.content, features='html.parser')
    questions = soup.select('#questions>div')
    if count:
        questions = questions[:count]

    # Parse every question block into a dictionary
    return [parse_question(q_html) for q_html in questions]


if __name__ == "__main__":
    # Example run: scrape questions tagged "selenium"
    results = scrape_questions("selenium")
    print(results)


