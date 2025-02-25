import random
import requests
from textwrap import dedent
import google.generativeai as genai

from requests_oauthlib import OAuth1Session
import os
NEWS_API_ORG_KEY = os.environ.get("NEWS_API_ORG_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET_KEY = os.environ.get("X_API_SECRET_KEY")
OAUTH_TOKEN = os.environ.get("OAUTH_TOKEN")
OAUTH_TOKEN_SECRET = os.environ.get("OAUTH_TOKEN_SECRET")

def green_text(text):
    # Wrap the text in green ANSI escape codes
    print(f"\033[32m{text}\033[0m")

def blue_text(text):
    # Wrap the text in blue ANSI escape codes
    print(f"\033[34m{text}\033[0m")

def decide_topic():
    # List of topics with equal probability
    topics = [
"bitcoin", "starlink", "polymarket", "solar energy", "renewables", "interest rates",
        "llm", "ai", "musk", "trump", "nvidia", "tesla", "inflation",
        "blockchain", "dogecoin", "humanoid robots", "federal reserve", "europe",
        "recession", "quantum computing", "space travel", "ethereum",
        "hyperloop", "crypto regulation", "artificial general intelligence",
        "gold prices", "neuralink", "tech stocks", "energy crisis", "decentralized finance",
        "web3", "metaverse", "self-driving cars", "fusion energy", "cybersecurity",
        "spacex launches", "central bank digital currencies", "robotics automation",
        "genetic engineering", "elon’s mars plan", "mars", "xrp", "tech layoffs",
        "hydrogen power", "privacy coins", "gamestop", "augmented reality",
        "supply chain tech", "biden’s economic policy", "apple’s next big thing",
        "5G", "climate tech", "moon mining", "nano technology", "canada", "russia", "greece", "poland", "germany", "france", "plane"
        "elon vs. zuck", "cardano", "physics", "mathematics", "smart cities",
        "defi hacks", "battery breakthroughs", "crypto", "melania", "virtual reality", "augemented reality",
        "playstation", "xbox", "6G", "fusion", "battery", "lithium", "grok", "gemini", "chatgpt", "openai", "google", "apple"
    ]
    
    # Randomly choose a topic with equal probability
    chosen_topic = random.choice(topics)
    
    return chosen_topic

def decide_prompt_style():
    # List of prompt styles with equal probability
    prompt_styles = [
        "posing an engaging question",
        "use one or maximal two difficult words do not overdo it",
        "use three or four lines of text with each separated from one another with an empty line",
        "edgy",
        "use casual slang lightly like bruh or fam",
        "write as a character with > before actions like Be Elon > Builds rocket > Flies to Mars",
        "positive and optimistic",
        "a little bit provoking",
        "funny",
        "add one emoji",
        "inspirational",
        "witty",
        "posing a simple and straightforward super-engaging question in a rather short post",
        "a little bit aggressive",
        "sarcastic",
        "whimsical",
        "ironeous",
        "a bit pessimistic",
        "confidently bold",
        "subtly mocking",
        "futuristic and visionary",
        "dry humor",
        "curious and probing",
        "slightly exaggerated",
        "matter-of-fact",
        "rebellious tone",
    ]
    
    # Pick three unique styles randomly with equal probability
    chosen_styles = random.sample(prompt_styles, k=3)
    
    # Return the styles as a comma-separated string
    return ", ".join(chosen_styles)

def decide_post_length():
    # List of post lengths with equal probability
    lengths = [
        "short (under 100 characters)",
        "medium (100-200 characters)",
        "long (200-280 characters)"
    ]
    
    # Randomly choose a length with equal probability
    chosen_length = random.choice(lengths)
    
    return chosen_length

def retrieve_articles(topic):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": f'"{topic}"',
        "language": "en",
        "sortBy": "publishedAt",  # "popularity" or "publishedAt" for chronological sorting
        "pageSize": 8,
        "searchIn": "title,description",  # Restrict search to title and description only
        "apiKey": NEWS_API_ORG_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        total_results = data.get("totalResults", 0)
        print("Total articles found:", total_results)
        
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

# Define good examples at module level
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

def call_llm_for_post_creation(prompt_style, topic, post_length, articles=None):
    genai.configure(api_key=GEMINI_API_KEY)

    # If "articles" exist
    if articles:
        input_section = f"""
I will provide you with some fresh articles. Choose randomly one of them as a source of inspiration for creating the X post.

News Articles:
{articles}
"""
    # If "articles" don't exist
    else:
        input_section = f"""
I will provide you with a topic. Use this topic as the source of inspiration for creating the X post.

Topic: {topic}
"""
    prompt = f"""
Generate an engaging and creative X post (tweet) using the following input:
{input_section}
Generally, try to be based and not woke.
There is no need to add hashtags to the post.
At the end, give me only the text that I can post on X, without any comments or stuff that shouldn’t be posted.

Prompt Style: {prompt_style}
Length: {post_length}

Good X Post Examples:
{good_x_post_examples}

Based on the above, create a unique X post.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")        
    blue_text(prompt)
    response = model.generate_content(prompt)
    return response.text

def post_on_x(text):
    # Use credentials directly from config.py
    oauth = OAuth1Session(
        X_API_KEY,
        client_secret=X_API_SECRET_KEY,
        resource_owner_key=OAUTH_TOKEN,
        resource_owner_secret=OAUTH_TOKEN_SECRET
    )
    
    # Post the tweet
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 201:
        raise Exception(f"Error: {response.status_code} {response.text}")
