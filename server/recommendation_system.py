

class RecommendationSystem:
    def __init__(self, db):
        self.db = db

    def extract_comments(self):
        try:
            query = "SELECT item_id, comments FROM feedback"
            feedback = self.db.fetchall(query)
            return feedback
        except Exception as e:
            print(f"Error extracting comments: {str(e)}")
            return []

    def analyze_comments(self, feedback):
        print("Inside analyze_comments")
        positive_keywords = ['good', 'great', 'excellent', 'tasty', 'delicious', 'amazing', 'nice', 'perfect', 'best',
                             'enjoyed']
        negative_keywords = ['bad', 'terrible', 'awful', 'tasteless', 'poor', 'disgusting', 'worst', 'horrible',
                             'unpleasant', 'not good']
        item_mentions = {}

        for item_id, comment in feedback:
            comment = comment.lower()
            positive_count = sum(1 for keyword in positive_keywords if keyword in comment)
            negative_count = sum(1 for keyword in negative_keywords if keyword in comment)

            if item_id not in item_mentions:
                item_mentions[item_id] = 0

            item_mentions[item_id] += positive_count
            item_mentions[item_id] -= negative_count

        return item_mentions

    def get_top_items(self, item_mentions, num_items):
        sorted_items = sorted(item_mentions.items(), key=lambda x: x[1], reverse=True)
        num_items = num_items['num_items']
        return sorted_items[:num_items]

    def recommend_items(self, item_mentions, num_items):
        print("Inside recommend_items")
        print(item_mentions)
        print(num_items)
        if not item_mentions:
            print("Not able to recommend due to insufficient data")
            return []

        recommended_items = self.get_top_items(item_mentions, num_items)
        print("Got recommended items")

        try:
            item_ids = [item_id for item_id, _ in recommended_items]
            format_strings = ','.join(['%s'] * len(item_ids))
            query = f"SELECT item_id, item_name, meal_type FROM food WHERE item_id IN ({format_strings})"
            self.db.db_cursor.execute(query, tuple(item_ids))
            items = self.db.db_cursor.fetchall()

            recommendations = [
                {'item_id': item[0], 'item_name': item[1], 'meal_type': item[2]} for
                item in items
            ]
            print("Getting recommendations list")
            print(recommendations)
            return recommendations
        except Exception as e:
            print(f"Error fetching item details: {str(e)}")
            return []

    def get_recommendations(self, num_items):
        print("Inside get_recommendations")
        feedback = self.extract_comments()
        if not feedback:
            print("No data found in feedback table")
            return []
        item_mentions = self.analyze_comments(feedback)
        recommendations = self.recommend_items(item_mentions, num_items)
        return recommendations

