import random

def generate_message(article_url):
    templates = [
        "Check out this awesome post: {url}",
        "You don’t want to miss this: {url}",
        "What do you think about this article? {url}",
        "Loved reading this one! {url}",
        "This was interesting: {url}"
    ]
    return random.choice(templates).format(url=article_url)
