# Project Idea: Automated News Sentiment Tracker

# Overview:

The Automated News Sentiment Tracker is a data pipeline designed to extract articles from a news website, analyze the sentiment of each article, and provide real-time visual insights through an interactive dashboard. The pipeline is fully automated, ensuring that data is collected, processed, and visualized at scheduled intervals without manual intervention.

# Key Features:

1. Web Scraping:
   * Extract articles, publication dates, and authors from a target news website.
* Store the scraped data in a structured format for further processing.

2. Sentiment Analysis:
   * Use Natural Language Processing (NLP) techniques to classify the sentiment of each article as positive, negative, or neutral.
* Add sentiment scores to the dataset for deeper analysis.

3. Database Integration:
   * Load the cleaned and analyzed data into a cloud-hosted MySQL database.
* Implement deduplication to ensure no redundant data is stored.

5. Automation:
   Schedule the entire Extract-Transform-Load (ETL) process using GitHub Actions for efficient, hands-free data processing.

6. Data Visualization:
   * Build an interactive dashboard in Power BI to showcase:
     * Sentiment trends over time.
     * Articles categorized by sentiment.
     * Author contributions and their sentiment distribution.
* Enable automatic dashboard refresh to ensure the latest data is always displayed.

* Challenge: Implementing automation with GitHub Actions instead of traditional tools like Airflow.
    * Solution: Leverage GitHub Actions’ flexibility to write a robust workflow for scheduling and executing scripts.
* Challenge: Cleaning unstructured text data for accurate sentiment analysis.
    * Solution: Use preprocessing techniques like removing stopwords, punctuation, and irrelevant characters.

# Technologies and Tools:

* Python: For scripting and ETL processes.
BeautifulSoup & Requests: For web scraping.
* NLTK: For sentiment analysis.
* PyMySQL: For database operations.
* GitHub Actions: For pipeline automation.
* Power BI: For creating an interactive dashboard.

# Outcomes:

* A scalable and fully automated solution for tracking news sentiment.
* Insights into how sentiment varies over time and across topics or authors.
* Practical experience in using modern data engineering tools and techniques.

