import mysql.connector
import math

def preprocess_employee_comments(comment):
    if "Excellent" in comment or "High quality" in comment:
        return 1
    else:
        return 0  #

def train_naive_bayes(food_items):
    num_items = len(food_items)
    num_features = 4
    num_classes = 2

    class_counts = [0] * num_classes
    feature_counts = [[0.0] * num_features for _ in range(num_classes)]

    X = []
    y = []
    for item in food_items:
        X.append([float(item["price"]), float(item["avg_rating"]), float(item["quality"]), float(item["quantity"])])
        y.append(preprocess_employee_comments(item["employee_comments"]))
        class_counts[y[-1]] += 1
        for i in range(num_features):
            feature_counts[y[-1]][i] += X[-1][i]


    min_value = 0.1

    if num_items == 0:
        num_items = min_value

    prior = [max(class_counts[i] / num_items, min_value) for i in range(num_classes)]

    # Likelihoods
    smoothing_factor = 1  # Laplace smoothing factor
    likelihoods = [
        [max((feature_counts[c][f] + smoothing_factor) / (class_counts[c] + smoothing_factor * num_features), min_value)
         for f in range(num_features)]
        for c in range(num_classes)]

    return prior, likelihoods
def predict_naive_bayes(item, prior, likelihoods):
    num_features = len(item)
    num_classes = len(prior)

    posteriors = [0] * num_classes

    for c in range(num_classes):
        posterior = math.log(prior[c])
        for f in range(num_features):
            posterior += math.log(likelihoods[c][f]) if item[f] > 0 else 0
        posteriors[c] = posterior

    return posteriors.index(max(posteriors))


# Connect to MySQL database and fetch data from the feedback table
def fetch_food_items_from_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Admin@!2345",
        database="fd"
    )
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        feedback_id as id,
        item_id,
        item_name as name,
        qty as quantity,
        quality,
        vfm,
        comments as employee_comments
    FROM
        feedback
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    food_items = []
    for row in rows:
        food_item = {
            "id": row["id"],
            "name": row["name"],
            "price": row["vfm"],  # Assuming price can be inferred from vfm (Value for Money)
            "avg_rating": row["quality"],  # Assuming avg_rating can be inferred from quality
            "quality": row["quality"],
            "quantity": row["quantity"],
            "employee_comments": row["employee_comments"]
        }
        food_items.append(food_item)

    return food_items


# Fetch food items from the database
food_items = fetch_food_items_from_db()

# Training Naive Bayes model
prior, likelihoods = train_naive_bayes(food_items)

# Example of a new food item to predict
new_food_item = {"name": "Pasta", "price": 10, "avg_rating": 4.6, "quality": 9, "quantity": 1,
                 "employee_comments": "Very tasty"}

# Predict using Naive Bayes model
X_new = [float(new_food_item["price"]), float(new_food_item["avg_rating"]), float(new_food_item["quality"]),
         float(new_food_item["quantity"])]
predicted_class = predict_naive_bayes(X_new, prior, likelihoods)

# Determine recommendation based on predicted class
if predicted_class == 1:
    recommendation = "Recommended"
else:
    recommendation = "Not Recommended"

print(f"Food item '{new_food_item['name']}' is {recommendation}")
