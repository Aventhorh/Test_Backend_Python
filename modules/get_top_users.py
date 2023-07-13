from models.User import db, User

def get_top_users():
    """
    Get the top 5 users with the longest usernames.

    Returns:
        List[User]: The list of top users.
    """
    top_users = User.query.order_by(db.func.length(User.username).desc()).limit(5).all()
    return top_users