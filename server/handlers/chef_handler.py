import datetime
from server.databases import chef_queries
from recommendation_system import RecommendationSystem

class ChefHandler:
    def __init__(self, db_connection):
        self.db = db_connection

    def view_menu(self):
        try:
            query = chef_queries.get_all_dishes()
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for
                           dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def view_recommendation(self, num_items):
        try:
            recommender = RecommendationSystem(self.db)
            recommendations = recommender.get_recommendations(num_items)
            return {'status': 'success', 'dishes': recommendations}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def add_notification(self, message):
        try:
            current_time = datetime.datetime.now()
            query = chef_queries.insert_notification()
            self.db.execute(query, (message, current_time))
            return {'status': 'success', 'message': 'Notification added successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def voting_results(self):
        try:
            query = chef_queries.get_vote_results()
            results = self.db.fetchall(query)
            results_list = [{'item_id': result[0], 'item_name': result[1], 'total_votes': result[2]} for result in
                            results]
            return {'results': results_list}
        except Exception as e:
            return {'message': str(e)}

    def choose_final_menu(self, data):
        try:
            item_ids = data['item_ids']

            # Prepare placeholders for the query
            placeholders = ', '.join(['(%s, 1, CURDATE())'] * len(item_ids))

            # Prepare the values to be inserted
            values = tuple(item_ids)

            # Construct the SQL query
            query = chef_queries.insert_final_menu().format(placeholders)

            # Execute the query
            self.db.execute(query, values)

            return {'status': 'success', 'message': 'Final menu chosen successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
