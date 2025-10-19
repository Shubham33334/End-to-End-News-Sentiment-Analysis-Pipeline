from bs4 import BeautifulSoup
import requests
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from datetime import datetime, timedelta
import pymysql
import re
import os 

def scrapped_data():
    url = 'https://punchng.com/topics/news/'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    article_container = soup.find_all('h1', class_='post-title')

    links = [container.find('a')['href'] for container in article_container]

    article_link = []
    writers_name = []
    title = []
    date_posted = []
    article = []

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        article_link.append(link)
        writers_name.append(soup.find('span', class_='post-author').get_text(strip=True))
        title.append(soup.find('h1', class_='post-title').get_text(strip=True))
        date_str = soup.find('span', class_='post-date').get_text(strip=True)
        # Remove ordinal suffixes
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
        # convert the date format
        date = datetime.strptime(date_str, '%d %B %Y')
        date_posted.append(date.strftime('%Y-%m-%d'))
        article.append(soup.find('div', class_='post-content').get_text(strip=True))

    article_data = pd.DataFrame({
        'article_link' : article_link,
        'writers_name' : writers_name,
        'title' : title,
        'date_posted' : date_posted,
        'article' : article
    })
    
    # article_data.to_csv('punchNews.csv', index=False) 
    return article_data
article_data = scrapped_data()

from nltk.corpus import stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('punkt_tab')
    
def sentiment_analysis(article_data):
    def preprocessed_text(text):
        # tokenize the text
        tokens = word_tokenize(text.lower())
        
        # remover stop words
        filtered_token = [token for token in tokens if token not in stopwords.words('english')]

        # lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_token]

        # join the tokens back to str
        processed_text = ' '.join(lemmatized_tokens)
        return processed_text
    
    # apply it to the dataframe
    article_data['review_text'] = article_data['article'].apply(preprocessed_text)

    # initiate sentimental analyzer
    analyzer = SentimentIntensityAnalyzer()
    
    # create get_sentiment function
    def get_sentiment(text):
        scores = analyzer.polarity_scores(text)
        # sentiment = 1 if scores['compound'] > 0 else 0
        if scores['compound'] >= 0.05:
            return 'positive'
        elif scores['compound'] <= 0.05:
            return 'negative'
        else:
            return 'neutral'
        # return sentiment
    
    # apply get sentiment function to dataframe
    article_data['sentiment'] = article_data['review_text'].apply(get_sentiment)


    # article_data.to_csv(r'C:\Users\martha\OneDrive\Python\punch_article.csv', index=False)
    article_data.to_csv('punchNews.csv', index=False)
sentiment_analysis(article_data)

# scrapped_data() 

# article_data = scrapped_data() 

# save to a database
def save_to_db():
    timeout = 10
    conn = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="punchNewsDb",
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        read_timeout=timeout,
        port=14484,
        user=os.getenv("DB_USER"),
        write_timeout=timeout,
    )
    cur = conn.cursor()
    
    for row in article_data.itertuples(index=False):
        cur.execute(
            '''
            INSERT INTO punch_news (article_link, writers_name, title,date_posted , article, review_text, sentiment) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)  
            ON DUPLICATE KEY UPDATE
                writers_name=VALUES(writers_name),
                title=VALUES(title),
                date_posted= VALUES(date_posted),
                article=VALUES(article),
                review_text=VALUES(review_text),
                sentiment=VALUES(sentiment)
            ''', (row.article_link, row.writers_name, row.title, row.date_posted, row.article, row.review_text, row.sentiment)
        )
    conn.commit()
    cur.close()
    conn.close()
save_to_db()
