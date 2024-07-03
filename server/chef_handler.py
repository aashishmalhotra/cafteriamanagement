import datetime
from recomm2 import RecommendationSystem

import datetime
from recomm2 import RecommendationSystem

class ChefHandler:
    def __init__(self, db_connection):
        self.db = db_connection

    def view_menu(self):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_recommendation(self, num_items):
        try:
            print("inside chef handler and View_recomm method")
            recommender = RecommendationSystem(self.db)
            recommendations = recommender.get_recommendations(num_items)
            return {'status': 'success', 'dishes': recommendations}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def add_notification(self, message):
        try:
            current_time = datetime.datetime.now()
            query = "INSERT INTO notification (message, date) VALUES (%s, %s)"
            self.db.execute(query, (message, current_time))
            return {'status': 'success', 'message': 'Notification added successfully'}
        except Exception as e:
            print(f"Error adding notification: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def voting_results(self):
        try:
            query = """
                SELECT f.item_id, f.item_name, COUNT(v.vote_id) as total_votes
                FROM vote v
                JOIN food f ON v.item_id = f.item_id
                WHERE v.is_selected = 0
                GROUP BY f.item_id
                ORDER BY total_votes DESC
            """
            results = self.db.fetchall(query)
            results_list = [{'item_id': result[0], 'item_name': result[1], 'total_votes': result[2]} for result in results]
            return {'status': 'success', 'results': results_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def choose_final_menu(self, data):
        try:
            item_ids = data['item_ids']
            query1 = "UPDATE vote SET is_selected = 1 WHERE item_id IN (%s)" % ','.join(map(str, item_ids))
            query2 = "UPDATE vote SET vote_date = CURDATE() WHERE item_id IN (%s)" % ','.join(map(str, item_ids))
            self.db.execute(query1)
            self.db.execute(query2)
            return {'status': 'success', 'message': 'Final menu chosen successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

