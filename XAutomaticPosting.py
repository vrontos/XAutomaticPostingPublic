from functions import (
    decide_topic,
    decide_prompt_style,
    decide_post_length,
    retrieve_articles,
    call_llm_for_post_creation,
    green_text,
    blue_text,
    post_on_x
)
import random

# 1. Decide if need to use the news API org
use_news_api_org = random.random() < 0.3
print("\n### 1. Use News API Org?:", use_news_api_org)

# 2. Decide topic
topic = decide_topic()
print("\n### 2. Chosen topic:", topic)

# 3. Decide prompt style
prompt_style = decide_prompt_style()
print("\n### 3. Chosen prompt style:", prompt_style)

# 4. Decide post length
post_length = decide_post_length()
print("\n### 4. Chosen post length:", post_length)

# If needed, retrieve articles; otherwise, set articles to None
articles = None
if use_news_api_org:
    articles = retrieve_articles(topic)
    if not articles.strip():
        print("No articles found. Stopping further execution.")
        exit(0)
    print("\n### 5. Retrieved articles:\n", articles)

# 6. Call Gemini LLM to create an X post
prompt, post_created_from_llm = call_llm_for_post_creation(prompt_style, topic, post_length, articles)
print("\nPROMPT:")
blue_text(prompt)
print(f"\n### Generated X post:")
print(f"- TOPIC: {topic}")
print(f"- LENGTH: {post_length}")
print(f"- USED NEWS ARTICLES: {use_news_api_org}")
print(f"- STYLES: {prompt_style}\n")
green_text(post_created_from_llm)

# Post on X
#post_on_x(post_created_from_llm)
#print("Posted successfully on X!🚀")
