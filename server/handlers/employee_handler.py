import datetime
from recomm2 import RecommendationSystem

class EmployeeHandler:
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

    def provide_feedback(self, data):
        item_name = data.get('item_name')
        qty = data.get('qty')
        quality = data.get('quality')
        vfm = data.get('vfm')
        comments = data.get('comments')

        if not item_name or not qty or not quality or not vfm or not comments:
            return {'status': 'error', 'message': 'Provide all details for a food item'}

        try:
            query = "SELECT item_id FROM food WHERE item_name = %s"
            result = self.db.fetchone(query, (item_name,))

            if not result:
                return {'status': 'error', 'message': 'Item name not found in database'}

            item_id = result[0]

            query = """INSERT INTO feedback (item_id, item_name, qty, quality, vfm, comments) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            self.db.execute(query, (item_id, item_name, qty, quality, vfm, comments))
            return {'status': 'success', 'message': 'Feedback submitted'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_item_to_vote(self):
        try:
            query = """
                    SELECT f.item_name, f.item_id
                    FROM vote v
                    JOIN food f ON v.item_id = f.item_id
                    WHERE v.is_selected = 1
                    """
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
            query = "INSERT INTO vote (item_id, vote) VALUES (%s, %s)"
            self.db.execute(query, (item_id, vote))
            return {'status': 'success', 'message': 'Vote recorded'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # def next_day_menu(self):
    #     try:
    #         query = """SELECT f.* FROM food f
    #                    JOIN vote v ON f.item_id = v.item_id
    #                    WHERE v.is_selected = 1"""
    #         dishes = self.db.fetchall(query)
    #         dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
    #         return {'status': 'success', 'dishes': dishes_list}
    #     except Exception as e:
    #         return {'status': 'error', 'message': str(e)}

    def show_notification(self, data):
        # user_id = data.get('user_id')
        username = data.get('user_name')

        try:
            query = "SELECT id FROM users WHERE username = %s"
            result = self.db.fetchone(query, (username,))

            if not result:
                return {'status': 'error', 'message': 'User not found'}

            user_id = result[0]

            print("inside try")
            today_date = datetime.date.today()
            date_str = today_date.strftime('%Y-%m-%d')

            query = "SELECT message FROM notification WHERE date = %s"
            messages = self.db.fetchall(query, (date_str,))

            messages_list = [{'message': message[0]} for message in messages]

            return {'status': 'success', 'messages': messages_list}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_feedback_questions(self, item_id):
        try:
            query_questions = """
                              SELECT id, question 
                              FROM detailed_feedback
                              WHERE item_id = %s
                              """
            self.db.db_cursor.execute(query_questions, (item_id,))
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

                query_update = """
                               UPDATE detailed_feedback
                               SET answer = %s
                               WHERE item_id = %s AND id = %s
                               """
                self.db.execute(query_update, (answer, item_id, question_id))

            return {'status': 'success', 'message': 'Feedback submitted successfully'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_feedback_items(self):
        try:
            query = """
                    SELECT df.item_id, f.item_name
                    FROM detailed_feedback df
                    JOIN food f ON df.item_id = f.item_id
                    GROUP BY df.item_id
                    """
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

                query = """
                        UPDATE detailed_feedback
                        SET answer = %s
                        WHERE item_id = %s AND id = %s
                        """
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

            # Check if the user already has a preference record
            query_check = """
                          SELECT id FROM user_preference WHERE user_id = %s
                          """
            self.db.db_cursor.execute(query_check, (user_id,))
            result = self.db.db_cursor.fetchone()

            if result:
                # Update existing preference record
                query_update = """
                               UPDATE user_preference
                               SET preference = %s, spice_level = %s, preferred_cuisine = %s, sweet_tooth = %s
                               WHERE user_id = %s
                               """
                self.db.db_cursor.execute(query_update,
                                          (preference, spice_level, preferred_cuisine, sweet_tooth, user_id))
            else:
                # Insert new preference record
                query_insert = """
                               INSERT INTO user_preference (user_id, preference, spice_level, preferred_cuisine, sweet_tooth)
                               VALUES (%s, %s, %s, %s, %s)
                               """
                self.db.db_cursor.execute(query_insert,
                                          (user_id, preference, spice_level, preferred_cuisine, sweet_tooth))

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

            # Get the next day's menu items
            next_day_menu_response = self.next_day_menu()
            if next_day_menu_response['status'] != 'success':
                return next_day_menu_response

            dishes = next_day_menu_response['dishes']

            # Fetch user's preferences
            query_pref = """
                         SELECT preference, spice_level, preferred_cuisine, sweet_tooth 
                         FROM user_preference 
                         WHERE user_id = %s AND EXISTS 
                            (SELECT 1 FROM users WHERE id = %s AND role = 'employee')
                         """
            self.db.db_cursor.execute(query_pref, (user_id, user_id))
            user_pref = self.db.db_cursor.fetchone()

            if not user_pref:
                return {'status': 'error', 'message': 'Entered user id is not on the role of an employee'}

            user_preference, user_spice_level, user_cuisine, user_sweet_tooth = user_pref

            # Fetch item categories to get the categories for each item
            item_ids = [dish['item_id'] for dish in dishes]
            if not item_ids:
                return {'status': 'success', 'dishes': []}

            format_strings = ','.join(['%s'] * len(item_ids))
            query_categories = f"""
                                SELECT item_id, preference, spice_level, preferred_cuisine, sweet_tooth 
                                FROM item_categories 
                                WHERE item_id IN ({format_strings})
                                """
            self.db.db_cursor.execute(query_categories, tuple(item_ids))
            item_categories = self.db.db_cursor.fetchall()

            # Create a list of items with their categories
            item_category_list = [{
                'item_id': item[0],
                'preference': item[1],
                'spice_level': item[2],
                'preferred_cuisine': item[3],
                'sweet_tooth': item[4]
            } for item in item_categories]

            # Sort items based on user preference
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

    # def sort_next_day_menu(self, user_id):
    #     try:
    #         # Get the next day's menu items using next_day_menu
    #         next_day_menu_response = self.next_day_menu()
    #         if next_day_menu_response['status'] != 'success':
    #             return next_day_menu_response
    #
    #         dishes = next_day_menu_response['dishes']
    #
    #         # Fetch user's preferences
    #         query_pref = "SELECT preference FROM user_preference WHERE user_id = %s and "
    #         self.db.db_cursor.execute(query_pref, (user_id,))
    #         user_pref = self.db.db_cursor.fetchone()
    #
    #         if not user_pref:
    #             return {'status': 'error', 'message': 'User preferences not found'}
    #
    #         preference = user_pref[0]
    #
    #         # Fetch item categories to get the categories for each item
    #         item_ids = [dish['item_id'] for dish in dishes]
    #         format_strings = ','.join(['%s'] * len(item_ids))
    #         query_categories = f"SELECT item_id, category FROM item_categories WHERE item_id IN ({format_strings})"
    #         self.db.db_cursor.execute(query_categories, tuple(item_ids))
    #         item_categories = self.db.db_cursor.fetchall()
    #
    #         # Create a dictionary to map item_id to category
    #         item_category_dict = {item[0]: item[1] for item in item_categories}
    #
    #         # Sort items based on user preference
    #         preferred_items = [dish for dish in dishes if item_category_dict[dish['item_id']] == preference]
    #         other_items = [dish for dish in dishes if item_category_dict[dish['item_id']] != preference]
    #
    #         sorted_dishes = preferred_items + other_items
    #
    #         return {'status': 'success', 'dishes': sorted_dishes}
    #
    #     except Exception as e:
    #         return {'status': 'error', 'message': str(e)}






