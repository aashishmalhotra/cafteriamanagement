import datetime
from recommendation_system import RecommendationSystem
from server.databases import employee_queries

class EmployeeHandler:
    def __init__(self, db_connection):
        self.db = db_connection

    def view_menu(self):
        try:
            query = employee_queries.get_all_dishes()
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def provide_feedback(self, data):
        item_name = data.get('item_name')
        qty = data.get('qty')
        quality = data.get('quality')
        vfm = data.get('vfm')
        comments = data.get('comments')

        if not item_name or not qty or not quality or not vfm or not comments:
            return {'status': 'error', 'message': 'Provide all details for a food item'}

        try:
            query = employee_queries.get_item_id_by_name()
            result = self.db.fetchone(query, (item_name,))

            if not result:
                return {'status': 'error', 'message': 'Item name not found in database'}

            item_id = result[0]

            query = employee_queries.insert_feedback()
            self.db.execute(query, (item_id, item_name, qty, quality, vfm, comments))
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_item_to_vote(self):
        try:
            query = employee_queries.get_items_for_voting()
            self.db.db_cursor.execute(query)
            items = self.db.db_cursor.fetchall()

            if not items:
                return {'status': 'error', 'message': "No items available for voting."}

            print('Items available to vote')
            return {'status': 'success', 'message': [{'item_id': item[1], 'item_name': item[0]} for item in items]}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def vote_item(self, data):
        item_id = data.get('item_id')
        vote = data.get('vote')
        if not item_id or not vote:
            return {'status': 'error', 'message': 'Invalid data'}

        try:
            query = employee_queries.insert_vote()
            self.db.execute(query, (item_id, vote))
            return {'status': 'success', 'message': 'Vote recorded'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def next_day_menu(self):
        try:
            query = employee_queries.get_next_day_menu()
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def show_notification(self, data):
        username = data.get('user_name')

        try:
            query = employee_queries.get_user_id_by_name()
            result = self.db.fetchone(query, (username,))

            if not result:
                return {'status': 'error', 'message': 'User not found'}

            user_id = result[0]

            print("inside try")
            today_date = datetime.date.today()
            date_str = today_date.strftime('%Y-%m-%d')

            query = employee_queries.get_notifications_by_date()
            messages = self.db.fetchall(query, (date_str,))

            messages_list = [{'message': message[0]} for message in messages]

            return {'status': 'success', 'messages': messages_list}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_feedback_questions(self, item_id):
        try:
            query = employee_queries.get_feedback_questions_by_item()
            self.db.db_cursor.execute(query, (item_id,))
            questions = self.db.db_cursor.fetchall()

            if not questions:
                return {'status': 'error', 'message': 'No questions found for the given item ID'}

            questions_list = [{'id': question[0], 'question': question[1]} for question in questions]

            return {'status': 'success', 'questions': questions_list}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_detailed_feedback(self, data):
        try:
            item_id = data.get('item_id')
            feedback = data.get('feedback')

            for fb in feedback:
                question_id = fb.get('id')
                answer = fb.get('answer')

                query_update = employee_queries.update_detailed_feedback()
                self.db.execute(query_update, (answer, item_id, question_id))

            return {'status': 'success', 'message': 'Feedback submitted successfully'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_feedback_items(self):
        try:
            query = employee_queries.get_feedback_items()
            self.db.db_cursor.execute(query)
            feedback_items = self.db.db_cursor.fetchall()

            items_list = [{'item_id': item[0], 'item_name': item[1]} for item in feedback_items]

            return {'status': 'success', 'items': items_list}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def send_detailed_feedback(self, data):
        try:
            item_id = data.get('item_id')
            feedback = data.get('feedback')

            for fb in feedback:
                id = fb.get('id')
                answer = fb.get('answer')

                query = employee_queries.update_detailed_feedback()
                self.db.db_cursor.execute(query, (answer, item_id, id))

            self.db.db_connection.commit()

            return {'status': 'success', 'message': 'Feedback submitted successfully'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_my_profile(self, data):
        try:
            user_id = data.get('user_id')
            preference = data.get('preference')
            spice_level = data.get('spice_level')
            preferred_cuisine = data.get('preferred_cuisine')
            sweet_tooth = data.get('sweet_tooth')

            query_check = employee_queries.get_user_preference()
            self.db.db_cursor.execute(query_check, (user_id, user_id))
            result = self.db.db_cursor.fetchone()

            query = employee_queries.update_or_insert_user_preference(result)
            self.db.db_cursor.execute(query, (preference, spice_level, preferred_cuisine, sweet_tooth, user_id))

            self.db.db_connection.commit()

            return {'status': 'success', 'message': 'Profile updated successfully'}

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

    def sort_next_day_menu(self, data):
        try:
            user_id = data.get('user_id')

            next_day_menu_response = self.next_day_menu()
            if next_day_menu_response['status'] != 'success':
                return next_day_menu_response

            dishes = next_day_menu_response['dishes']

            query_pref = employee_queries.get_user_preference()
            self.db.db_cursor.execute(query_pref, (user_id, user_id))
            user_pref = self.db.db_cursor.fetchone()

            if not user_pref:
                return {'status': 'error', 'message': 'Entered user id is not on the role of an employee'}

            user_preference, user_spice_level, user_cuisine, user_sweet_tooth = user_pref

            item_ids = [dish['item_id'] for dish in dishes]
            if not item_ids:
                return {'status': 'success', 'dishes': []}

            query_categories = employee_queries.get_item_categories(item_ids)
            self.db.db_cursor.execute(query_categories, tuple(item_ids))
            item_categories = self.db.db_cursor.fetchall()

            item_category_list = [{
                'item_id': item[0],
                'preference': item[1],
                'spice_level': item[2],
                'preferred_cuisine': item[3],
                'sweet_tooth': item[4]
            } for item in item_categories]

            preferred_items = [
                dish for dish in dishes
                if any(
                    item['item_id'] == dish['item_id'] and
                    item['preference'] == user_preference and
                    item['spice_level'] == user_spice_level and
                    item['preferred_cuisine'] == user_cuisine and
                    item['sweet_tooth'] == user_sweet_tooth
                    for item in item_category_list
                )
            ]

            other_items = [
                dish for dish in dishes
                if dish not in preferred_items
            ]

            sorted_dishes = preferred_items + other_items

            return {'status': 'success', 'dishes': sorted_dishes}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}