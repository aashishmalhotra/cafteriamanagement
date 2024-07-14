def get_all_dishes():
    return "SELECT item_id, item_name, meal_type, availability FROM food"

def insert_notification():
    return "INSERT INTO notification (message, date) VALUES (%s, %s)"

def get_vote_results():
    return """
                SELECT f.item_id, f.item_name, COUNT(v.vote_id) as total_votes
                FROM vote v
                JOIN food f ON v.item_id = f.item_id
                WHERE v.is_selected = 0
                GROUP BY f.item_id
                ORDER BY total_votes DESC
            """

def insert_final_menu():
    return "INSERT INTO vote (item_id, is_selected, vote_date) VALUES {}"