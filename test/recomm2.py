import mysql.connector
import re

# MySQL databases connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Admin@!2345',
    'database': 'fd'  # Corrected key name to 'database'
}

# Positive and negative word weights (you can adjust weights as needed)
word_weights = {
    "excellent": 2, "highly recommended": 2, "highly satisfied": 2, "great": 1.5, "good": 1.5, "delicious": 2,
    "amazing": 2, "wonderful": 1.5, "fantastic": 2, "love": 2, "perfect": 2, "outstanding": 1.5, "pleased": 1.5,
    "enjoyed": 1.5, "recommended": 1.5, "impressive": 1.5, "superb": 1.5, "fabulous": 1.5, "awesome": 2,
    # Add more positive words with their weights
}

negative_word_weights = {
    "poor": -2, "disappointing": -2, "not recommend": -2, "bad": -1.5, "horrible": -2, "terrible": -2, "too hard": -1.5,
    "overcooked": -1.5, "disgusting": -2, "awful": -2, "disappoint": -1.5, "unpleasant": -1.5, "unsatisfactory": -2,
    "regret": -1.5, "cold": -1.5, "not fresh": -1.5, "disliked": -1.5, "negative": -1.5, "avoid": -1.5,
    # Add more negative words with their weights
}

# Function to connect to MySQL databases and fetch feedback data
def fetch_feedback_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch item names from feedback table
        cursor.execute("SELECT item_name FROM feedback2")
        feedback_data = cursor.fetchall()

        conn.close()
        return feedback_data

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return []


# Function to calculate sentiment score for an item name
def calculate_sentiment_score(item_name):
    normalized_item_name = item_name.lower()

    # Remove punctuation except for commas, periods, apostrophes, and exclamation marks
    normalized_item_name = re.sub(r'[^\w\s,.\'!]', '', normalized_item_name)

    # Split item name into words
    words = normalized_item_name.split()
    total_words = len(words)

    # Initialize score
    sentiment_score = 0

    # Calculate sentiment score based on word weights
    for word in words:
        if word in word_weights:
            sentiment_score += word_weights[word]
        elif word in negative_word_weights:
            sentiment_score += negative_word_weights[word]

    # Normalize sentiment score based on total words
    if total_words > 0:
        sentiment_score /= total_words
    else:
        sentiment_score = 0  # Handle case where there are no words in the item name

    return sentiment_score


# Main function to determine sentiment for food item names
def determine_item_sentiments():
    feedback_data = fetch_feedback_data()

    if not feedback_data:
        print("No feedback data available.")
        return

    for record in feedback_data:
        item_name = record['item_name']
        sentiment_score = calculate_sentiment_score(item_name)

        print(f"Item Name: {item_name} - Sentiment Score: {sentiment_score:.2f}")

# Execute main function
if __name__ == '__main__':
    determine_item_sentiments()
