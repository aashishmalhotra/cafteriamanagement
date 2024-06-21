import mysql.connector
import math

# MySQL databases connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Admin@!2345',
    'databases': 'fd'
}


# Function to connect to MySQL databases and fetch feedback data
def fetch_feedback_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch all records from feedback table
        cursor.execute("SELECT food_id, rating, quantity, quality, vfm, comments FROM feedback")
        feedback_data = cursor.fetchall()

        conn.close()
        return feedback_data

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return []


# Function to preprocess comments (normalize and remove stop words)
def preprocess_comments(comment):
    # Remove punctuation and convert to lowercase
    normalized_comment = comment.lower().replace(',', '').replace('.', '')
    return normalized_comment


# Function to train Naive Bayes model for recommendation
# Function to train Naive Bayes model for recommendation with Laplace smoothing
def train_naive_bayes(feedback_data, alpha=1):
    num_items = len(feedback_data)
    num_features = 4  # (rating, quantity, quality, vfm)
    num_classes = 2  # (recommended or not recommended)

    # Initialize counts for likelihoods
    class_counts = [0] * num_classes
    feature_counts = [[0] * num_features for _ in range(num_classes)]

    # Collect data
    X = []
    y = []
    for record in feedback_data:
        rating = record['rating']
        quantity = record['quantity']
        quality = record['quality']
        vfm = record['vfm']
        comment = record['comments']

        # Preprocess comments
        normalized_comment = preprocess_comments(comment)

        # Determine recommendation class based on comments (1 for positive, 0 for negative)
        if "excellent" in normalized_comment or "high quality" in normalized_comment:
            y.append(1)  # Recommended
        else:
            y.append(0)  # Not Recommended

        class_counts[y[-1]] += 1
        X.append([rating, quantity, quality, vfm])
        for i in range(num_features):
            feature_counts[y[-1]][i] += X[-1][i]

    # Prior probabilities with Laplace smoothing
    prior = [(class_counts[c] + alpha) / (num_items + alpha * num_classes) for c in range(num_classes)]

    # Likelihoods (using Laplace smoothing)
    likelihoods = [[(feature_counts[c][f] + alpha) / (class_counts[c] + alpha * num_features)
                    for f in range(num_features)]
                   for c in range(num_classes)]

    return prior, likelihoods


# Function to predict using Naive Bayes model
def predict_naive_bayes(item, prior, likelihoods):
    num_features = len(item)
    num_classes = len(prior)

    posteriors = [0] * num_classes

    for c in range(num_classes):
        posterior = math.log(prior[c])
        for f in range(num_features):
            posterior += math.log(likelihoods[c][f]) if item[f] > 0 else 0
            posteriors[c] = posterior

    # Predict the class with maximum posterior probability
    return posteriors.index(max(posteriors))


# Main function to determine recommended food items using Naive Bayes
# Main function to determine recommended food items using Naive Bayes with Laplace smoothing
def determine_recommended_food_items():
    feedback_data = fetch_feedback_data()

    if not feedback_data:
        print("No feedback data available.")
        return

    # Train Naive Bayes model with Laplace smoothing
    prior, likelihoods = train_naive_bayes(feedback_data)

    # Example of a new food item to predict
    new_food_item = {"rating": 5, "quantity": 1, "quality": 8, "vfm": 4, "comments": "Very tasty and high quality"}

    # Predict using Naive Bayes model
    X_new = [new_food_item["rating"], new_food_item["quantity"], new_food_item["quality"], new_food_item["vfm"]]
    predicted_class = predict_naive_bayes(X_new, prior, likelihoods)

    # Determine recommendation based on predicted class
    if predicted_class == 1:
        recommendation = "Recommended"
    else:
        recommendation = "Not Recommended"

    print(f"Food item is {recommendation}")


# Execute main function
if __name__ == '__main__':
    determine_recommended_food_items()

