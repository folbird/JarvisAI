import json
from datetime import date
import logging
import feedparser
import html2text
import concurrent.futures
from langdetect import detect
import validators
import hashlib
from llama_index import GPTSimpleVectorIndex

with open("app/data/hot_news_rss.json", "r") as f:
    rss_urls = json.load(f)

TODAY = today = date.today()
MAX_DESCRIPTION_LENGTH = 300
MAX_POSTS = 3


def cut_string(text):
    words = text.split()
    new_text = ""
    count = 0
    for word in words:
        if len(new_text + word) > MAX_DESCRIPTION_LENGTH:
            break
        new_text += word + " "
        count += 1

    return new_text.strip() + '...'


def get_summary_from_gpt_thread(url):
    news_summary_prompt = '请用中文简短概括这篇文章的内容。'
    gpt_response, total_llm_model_tokens, total_embedding_model_tokens = get_answer_from_llama_web(
        [news_summary_prompt], [url])
    logging.info(
        f"=====> GPT response: {gpt_response} (total_llm_model_tokens: {total_llm_model_tokens}, total_embedding_model_tokens: {total_embedding_model_tokens}")
    return str(gpt_response)


def get_summary_from_gpt(url):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_summary_from_gpt_thread, url)
        return future.result(timeout=300)


def get_description(entry):
    gpt_answer = None
    try:
        gpt_answer = get_summary_from_gpt(entry.link)
    except Exception as e:
        logging.error(e)
    if gpt_answer is not None:
        summary = 'AI: ' + gpt_answer
    else:
        summary = cut_string(get_text_from_html(entry.summary))
    return summary


def get_text_from_html(html):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_tables = False
    text_maker.ignore_images = True
    return text_maker.handle(html)


def get_post_urls_with_title(rss_url):
    feed = feedparser.parse(rss_url)
    updated_posts = []

    for entry in feed.entries:
        published_time = entry.published_parsed if 'published_parsed' in entry else None
        # published_date = date(published_time.tm_year,
        #                       published_time.tm_mon, published_time.tm_mday)
        updated_post = {}
        updated_post['title'] = entry.title
        updated_post['summary'] = get_description(entry)
        updated_post['url'] = entry.link
        updated_post['publish_date'] = published_time
        updated_posts.append(updated_post)
        if len(updated_posts) >= MAX_POSTS:
            break

    return updated_posts

def format_dialog_messages(messages):
    return "\n".join(messages)

def get_language_code(text):
    try:
        return detect(text).split('-')[0]
    except Exception as e:
        logging.error(e)
        return 'zh'

def get_urls(urls):
    rss_urls = []
    page_urls = []
    phantomjscloud_urls = []
    youtube_urls = []
    for url in urls:
        if validators.url(url):
            feed = feedparser.parse(url)
            if hasattr(feed, 'version') and feed.version:
                rss_urls.append(url)
            else:
                page_urls.append(url)
    return {'rss_urls': rss_urls, 'page_urls': page_urls, 'phantomjscloud_urls': phantomjscloud_urls, 'youtube_urls': youtube_urls}

def remove_prompt_from_text(text):
    return text.replace('chatGPT:', '').strip()

def get_unique_md5(urls):
    urls_str = ''.join(sorted(urls))
    hashed_str = hashlib.md5(urls_str.encode('utf-8')).hexdigest()
    return hashed_str

def get_index_from_web_cache(name):
    web_cache_file = index_cache_web_dir / name
    if not web_cache_file.is_file():
        return None
    index = GPTSimpleVectorIndex.load_from_disk(web_cache_file)
    logging.info(
        f"=====> Get index from web cache: {web_cache_file}")
    return index

def get_answer_from_llama_web(messages, urls):
    dialog_messages = format_dialog_messages(messages)
    lang_code = get_language_code(remove_prompt_from_text(messages[-1]))
    combained_urls = get_urls(urls)
    logging.info(combained_urls)
    index_file_name = get_unique_md5(urls)
    index = get_index_from_web_cache(index_file_name)
    if index is None:
        logging.info(f"=====> Build index from web!")
        documents = get_documents_from_urls(combained_urls)
        logging.info(documents)
        index = GPTSimpleVectorIndex(documents)
        logging.info(
            f"=====> Save index to disk path: {index_cache_web_dir / index_file_name}")
        index.save_to_disk(index_cache_web_dir / index_file_name)
    prompt = get_prompt_template(lang_code)
    logging.info('=====> Use llama web with chatGPT to answer!')
    logging.info('=====> dialog_messages')
    logging.info(dialog_messages)
    logging.info('=====> text_qa_template')
    logging.info(prompt.prompt)
    answer = index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=prompt)
    total_llm_model_tokens = llm_predictor.last_token_usage
    total_embedding_model_tokens = index.embed_model.last_token_usage
    return answer, total_llm_model_tokens, total_embedding_model_tokens