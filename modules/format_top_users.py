from typing import List, Dict, Any
from models.User import User

def format_top_users(users: List[User]) -> List[Dict[str, Any]]:
    """
    Format the top user data.

    Args:
        users (List[User]): The list of top users.

    Returns:
        List[Dict[str, Any]]: The formatted user data.
    """
    formatted_users = []
    for user in users:
        formatted_user = {
            'username': user.username,
            'email': user.email,
            'name_length': len(user.username)
        }
        formatted_users.append(formatted_user)
    return formatted_users