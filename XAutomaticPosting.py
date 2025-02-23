from functions import (
    decide_topic,
    retrieve_articles,
    decide_prompt_style,
    get_good_x_post_examples,
    call_llm_for_post_creation,
    post_on_x
)

# 1. Decide topic
topic = decide_topic()
print("### 1. Chosen topic:", topic)

# 2. Call News API Org to retrieve 5 articles: language=en, sortBy=popularity
articles = retrieve_articles(topic)
# If no articles are found, stop further execution
if not articles.strip():
    print("No articles found. Stopping further execution.")
    exit(0)
print("### 2. Retrieved articles:\n", articles)

# 3.1 Decide prompt style
prompt_style = decide_prompt_style()
print("### 3.1 Chosen prompt style:", prompt_style)

# 3.2 Good X post examples
good_x_post_examples = get_good_x_post_examples()
print("### 3.2 Good X post examples:\n", good_x_post_examples)

# 4. Call Gemini LLM to create an X post
post_created_from_llm = call_llm_for_post_creation(articles, prompt_style, good_x_post_examples)
print(f"\n### 4. Generated X post (Topic: {topic}, Style: {prompt_style}):\n", post_created_from_llm)

# 5. Post on X
post_on_x(post_created_from_llm)
print("Posted successfuly on X!🚀")
