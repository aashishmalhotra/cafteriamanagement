def update_item_category():
    return "UPDATE item_categories SET preference = %s, spice_level = %s, sweet_tooth = %s, preferred_cuisine = %s WHERE item_id = %s"

def add_item_category():
    return "INSERT INTO item_categories SET preference = %s, spice_level = %s, sweet_tooth = %s, preferred_cuisine = %s , item_id = %s,item_name=%s"

def get_item_id():
    return """SELECT f.item_id
    FROM food f
    LEFT JOIN item_categories ic ON f.item_id = ic.item_id
    WHERE f.item_name = %s"""
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

def get_food_with_categories():
    return """
    SELECT f.item_id, f.item_name, f.meal_type, f.availability, 
           ic.preference, ic.spice_level, ic.sweet_tooth, ic.preferred_cuisine
    FROM food AS f
    LEFT JOIN item_categories AS ic ON f.item_id = ic.item_id
    """

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

def get_food_item_id():
    return "SELECT item_id FROM food WHERE item_name = %s"