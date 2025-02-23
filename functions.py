import random
from networkx import dedensify
import requests
from textwrap import dedent
import google.generativeai as genai

import os
import json
from requests_oauthlib import OAuth1Session
from config import NEWS_API_ORG_KEY, GEMINI_API_KEY, X_API_KEY, X_API_SECRET_KEY


def decide_topic():
    # Dictionary with topics and their corresponding weights
    rand_topics = {"bitcoin": 3,
                   "inflation": 3, 
                   "starlink": 3,
                   "polymarket": 3,
                   "interest rates": 2, 
                   "llm": 2,
                   "ai": 2, 
                   "musk": 2,
                   "trump": 2,
                   "nvidia": 2,
                   "tesla": 2,
                   "blockchain": 1,
                   "dogecoin": 1,
                   "humanoid robots": 1,
                   "federal reserve": 1,
                   }
    
    # Randomly choose a topic based on its weight
    chosen_topic = random.choices(list(rand_topics.keys()), weights=list(rand_topics.values()), k=1)[0]
    
    return chosen_topic

def retrieve_articles(topic):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{topic}"',
        "language": "en",
        "sortBy": "popularity",  # "popularity" or "publishedAt" for chronological sorting
        "pageSize": 5,
        "apiKey": NEWS_API_ORG_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        total_results = data.get("totalResults", 0)
        print("\nTotal articles found:", total_results)
        
        articles_data = data.get("articles", [])
        articles = ""
        for idx, article in enumerate(articles_data, start=1):
            title = article.get("title", "N/A")
            published_at = article.get("publishedAt", "N/A")
            source_name = article.get("source", {}).get("name", "N/A")
            description = article.get("description", "N/A")
            content = article.get("content", "N/A")
            
            articles += f"{idx})\n"
            articles += f"Title: {title} (published: {published_at})\n"
            articles += f"Source: {source_name}\n"
            articles += f"Description: {description}\n"
            articles += f"Content: {content}\n\n"
        return articles
    else:
        error_message = f"Error fetching articles: {response.status_code}"
        return error_message

def decide_prompt_style():
    # Dictionary with prompt styles and their corresponding weights
    prompt_styles = {
        "posing an engaging question": 4,
        "use one or two difficult words but do not overdo it": 4,
        "use three or four lines of text with each separated from one another with an empty line": 3,
        "edgy": 3,
        "positive and optimistic": 3,
        "a little bit provoking": 3,
        "funny": 3,
        "inspirational": 3,
        "witty": 2,
        "posing a simple and straigtforward super-engaging question in a rather short post": 2,
        "a little bit aggressive": 1,
        "sarcastic": 1,
        "whimsical": 1,
        "ironeous": 1,
        "a bit pessimistic": 1
    }
    
    # Pick three unique styles based on their weights
    chosen_styles = set()
    while len(chosen_styles) < 3:
        style = random.choices(
            list(prompt_styles.keys()),
            weights=list(prompt_styles.values()),
            k=1
        )[0]
        chosen_styles.add(style)
        
    # Return the styles as a comma-separated string
    return ", ".join(chosen_styles)

def get_good_x_post_examples():
    good_x_post_examples = [
        "The souls of people are incredible, it's the interface that's manipulated",
        "We live in the best timeline",
        "BREAKING: Elon Musk has just confirmed that he will take a more aggressive approach with DOGE, following a request from President Trump earlier today.",
        "JUST IN: President Trump says he is going with Elon Musk to inspect Fort Knox gold reserves to ensure it's still there.",
        "Some wins are so big that everybody wins, even if they're unaware.",
        "Going for a walk or pacing while on a phone call is a major cognitive power up",
        "The woke mind virus is an insidious capturer of minds and destroyer of connections to good friends and reality.",
        "Shall there never be a tyranny such as the one brought about by the Covid “response” measures ever again.",
        "Many are ignorant of cognitive security because they mistake their arrogance or ego for security until it is beaten by the cognitively secure.",
        "What’s one quote from Elon Musk that changed your life?",
        "You only feel life when you share life.\n\nYou don’t even feel rich unless you share being rich.",
        dedent("""\
            Be Stephen King:

            > Constantly makes negative posts
            > Gets trolled because of it
            > Then complains about negativity
            > Leaves
            > Comes back
            > Asks if people missed him
            > Makes more negative posts

            Rinse and repeat.""")
    ]
    return good_x_post_examples



def call_llm_for_post_creation(articles, prompt_style, good_examples):
    # Configure the Gemini API key
    genai.configure(api_key=GEMINI_API_KEY)

    prompt = f"""
Generate an engaging and creative X post (tweet) using the following input:

I will provide you with some fresh articles so you can get inspiration.
Generally, try to be based and not woke.
There is not need to add hashtags to the post.

News Articles:
{articles}

Prompt Style: {prompt_style}

Good X Post Examples:
{good_examples}

Based on the above, create a unique X post.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

def post_on_x(text):
    # Dynamically locate the directory where *this* file is located
    current_dir = os.path.dirname(os.path.realpath(__file__))
    token_file = os.path.join(current_dir, "tokens.json")
    
    # Read tokens from the JSON file
    with open(token_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
    
    # Create an OAuth1 session
    oauth = OAuth1Session(
        X_API_KEY,
        client_secret=X_API_SECRET_KEY,
        resource_owner_key=tokens["oauth_token"],
        resource_owner_secret=tokens["oauth_token_secret"]
    )
    
    # Post the tweet
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 201:
        raise Exception(f"Error: {response.status_code} {response.text}")