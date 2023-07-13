from datetime import datetime, timedelta
from models.User import User

def count_recent_users():
    """
    Count the number of users registered in the last 7 days.

    Returns:
        int: The number of recent users.
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = User.query.filter(User.registration_date >= seven_days_ago).count()
    return recent_users