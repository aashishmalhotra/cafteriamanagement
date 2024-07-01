import re

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

# Sample comments
sample_comments = [
    "The food was excellent and highly recommended.",
    "Great service and good food.",
    "I love their pasta, it's delicious!",
    "The steak was amazing, cooked perfectly.",
    "The desserts were wonderful.",
    "Fantastic experience, highly satisfied.",
    "Not recommend this restaurant, terrible service.",
    "The pizza was cold and disappointing.",
    "Avoid this place, awful food.",
    "The sushi was superb!",
    "The burger was good but the fries were too hard.",
    "Had a bad experience, the waiter was rude.",
    "The salad was not fresh, very unpleasant.",
    "The soup was outstanding.",
    "The chicken was overcooked and dry.",
    "They serve disgusting food.",
    "The ambiance was superb, enjoyed the evening.",
    "Regret coming here, terrible food.",
    "The wine selection was excellent.",
    "The service was poor, won't recommend."
]

# Function to calculate sentiment score for a given item name or comment
def calculate_sentiment_score(comment):
    normalized_comment = comment.lower()

    # Remove punctuation except for commas, periods, apostrophes, and exclamation marks
    normalized_comment = re.sub(r'[^\w\s,.\'!]', '', normalized_comment)

    # Split comment into words
    words = normalized_comment.split()
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
        sentiment_score = 0  # Handle case where there are no words in the comment

    return sentiment_score

# Analyze sentiment for each sample comment
for index, comment in enumerate(sample_comments):
    sentiment_score = calculate_sentiment_score(comment)
    print(f"Comment {index + 1}: {comment} - Sentiment Score: {sentiment_score:.2f}")
