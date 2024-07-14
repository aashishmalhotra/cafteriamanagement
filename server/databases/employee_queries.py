# database/queries.py

def get_all_dishes():
    return "SELECT item_id, item_name, meal_type, availability FROM food"

def get_item_id_by_name():
    return "SELECT item_id FROM food WHERE item_name = %s"

def insert_feedback():
    return """INSERT INTO feedback (item_id, item_name, qty, quality, vfm, comments) 
              VALUES (%s, %s, %s, %s, %s, %s)"""

def get_items_for_voting():
    return """
           SELECT f.item_name, f.item_id
           FROM vote v
           JOIN food f ON v.item_id = f.item_id
           WHERE v.is_selected = 1
           """
def insert_vote():
    return "INSERT INTO vote (item_id, vote) VALUES (%s, %s)"

def get_next_day_menu():
    return """SELECT f.* FROM food f
              JOIN vote v ON f.item_id = v.item_id
              WHERE v.is_selected = 1"""

def get_user_id_by_name():
    return "SELECT id FROM users WHERE username = %s"

def get_notifications_by_date():
    return "SELECT message FROM notification WHERE date = %s"

def get_feedback_questions_by_item():
    return """
           SELECT id, question 
           FROM detailed_feedback
           WHERE item_id = %s
           """

def update_detailed_feedback():
    return """
           UPDATE detailed_feedback
           SET answer = %s
           WHERE item_id = %s AND id = %s
           """

def get_feedback_items():
    return """
           SELECT df.item_id, f.item_name
           FROM detailed_feedback df
           JOIN food f ON df.item_id = f.item_id
           GROUP BY df.item_id
           """

def update_or_insert_user_preference(user_has_preference):
    if user_has_preference:
        return """
               UPDATE user_preference
               SET preference = %s, spice_level = %s, preferred_cuisine = %s, sweet_tooth = %s
               WHERE user_id = %s
               """
    else:
        return """
               INSERT INTO user_preference (user_id, preference, spice_level, preferred_cuisine, sweet_tooth)
               VALUES (%s, %s, %s, %s, %s)
               """

def get_user_preference():
    return """
           SELECT preference, spice_level, preferred_cuisine, sweet_tooth 
           FROM user_preference 
           WHERE user_id = %s AND EXISTS 
              (SELECT 1 FROM users WHERE id = %s AND role = 'employee')
           """

def get_item_categories(item_ids):
    format_strings = ','.join(['%s'] * len(item_ids))
    return f"""
           SELECT item_id, preference, spice_level, preferred_cuisine, sweet_tooth 
           FROM item_categories 
           WHERE item_id IN ({format_strings})
           """
