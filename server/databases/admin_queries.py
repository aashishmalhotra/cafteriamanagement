def insert_food():
    return "INSERT INTO food (item_name, meal_type, availability) VALUES (%s, %s, %s)"

def update_food():
    return "UPDATE food SET item_name = %s, meal_type = %s, availability = %s WHERE item_id = %s"

def delete_food():
    return "DELETE FROM food WHERE item_id = %s"

def delete_feedback_by_item():
    return "DELETE FROM feedback WHERE item_id = %s"

def get_food_details():
    return "SELECT item_id, item_name, meal_type, availability FROM food"

def insert_notification():
    return "INSERT INTO notification (message, date) VALUES (%s, %s)"

def get_low_rated_items():
    return """
           SELECT f.item_id, f.item_name,
           AVG((COALESCE(fb.qty, 0) + COALESCE(fb.quality, 0) + COALESCE(fb.vfm, 0)) / 5) AS avg_rating
           FROM food f
           JOIN feedback fb ON f.item_id = fb.item_id
           GROUP BY f.item_id
           HAVING avg_rating < 2
           """

def insert_detailed_feedback():
    return "INSERT INTO detailed_feedback (item_id, question) VALUES (%s, %s)"

def insert_detailed_feedback_with_answer():
    return "INSERT INTO detailed_feedback (item_id, question, answer) VALUES (%s, %s, %s)"
