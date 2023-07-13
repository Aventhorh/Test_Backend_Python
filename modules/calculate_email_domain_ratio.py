from models.User import User

def calculate_email_domain_ratio(domain):
    """
    Calculate the ratio of users with the specified email domain.

    Args:
        domain (str): The email domain to calculate the ratio for.

    Returns:
        float: The ratio of users with the specified email domain.
    """
    total_users = User.query.count()
    domain_users = User.query.filter(User.email.ilike(f"%@{domain}")).count()
    ratio = domain_users / total_users
    return ratio