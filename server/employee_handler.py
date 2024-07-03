import datetime

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

    def next_day_menu(self):
        try:
            query = """SELECT f.* FROM food f
                       JOIN vote v ON f.item_id = v.item_id
                       WHERE v.is_selected = 1"""
            dishes = self.db.fetchall(query)
            dishes_list = [{'item_id': dish[0], 'item_name': dish[1], 'meal_type': dish[2], 'availability': dish[3]} for dish in dishes]
            return {'status': 'success', 'dishes': dishes_list}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

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


def show_pending_feedback(self):
    try:

        query = """
                SELECT df.item_id, df.question_id, df.question, f.item_name
                FROM detailed_feedback df
                JOIN food f ON df.item_id = f.item_id
                WHERE df.answer IS NULL
                """
        self.db.db_cursor.execute(query)
        questions = self.db.db_cursor.fetchall()

        if not questions:
            return {'status': 'success', 'message': 'No pending feedback questions.'}

        pending_feedback = [
            {
                'item_id': question[0],
                'question_id': question[1],
                'question': question[2],
                'item_name': question[3]
            }
            for question in questions
        ]

        return {'status': 'success', 'questions': pending_feedback}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def send_detailed_feedback(self, data):
    try:
        item_id = data.get('item_id')
        feedback = data.get('feedback')  # feedback is a list of dictionaries with question_id and answer

        for fb in feedback:
            question_id = fb.get('question_id')
            answer = fb.get('answer')

            query = """
                    UPDATE detailed_feedback
                    SET answer = %s
                    WHERE item_id = %s AND question_id = %s
                    """
            self.db.db_cursor.execute(query, (answer, item_id, question_id))

        self.db.db_conn.commit()

        return {'status': 'success', 'message': 'Feedback submitted successfully'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


