from recomm2 import RecommendationSystem
class ChefHandler:
    def __init__(self, db_connection):
        self.db_obj = db_connection
        self.db_cursor = self.db_obj.db_cursor
        self.db_connection = self.db_obj.db_connection
    def view_menu(self):
        try:
            query = "SELECT item_id, item_name, meal_type, availability FROM food"
            self.db_cursor.execute(query)
            dishes = self.db_cursor.fetchall()
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_recommendation(self, num_items):
        try:
            print("inside chef handler and View_recomm method")
            recommender = RecommendationSystem(self.db_obj)
            recommendations = recommender.get_recommendations(num_items)
            # print(recommendations)
            # recommendations = recommendations[:int(num_items)]
            return {'status': 'success', 'dishes': recommendations}

        except Exception as e:
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
            self.db_cursor.execute(query)
            results = self.db_cursor.fetchall()
            results_list = [{'item_id': result[0], 'item_name': result[1], 'total_votes': result[2]} for result in results]
            return {'status': 'success', 'results': results_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def choose_final_menu(self, data):
        try:
            item_ids = data['item_ids']
            # Update the vote table to set is_selected to 1 for the chosen items
            query1 = "UPDATE vote SET is_selected = 1 WHERE item_id IN (%s)" % ','.join(map(str, item_ids))
            query2 = "UPDATE vote SET vote_date = CURDATE() WHERE item_id IN (%s)" % ','.join(map(str, item_ids))
            self.db_cursor.execute(query1)
            self.db_cursor.execute(query2)
            self.db_connection.commit()
            return {'status': 'success', 'message': 'Final menu chosen successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
