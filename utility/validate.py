def validate_user(user):
    if len(user['name']) > 4 and len(user['email']) > 4:
        return True
    if len(user['psw']) > 4 and user['psw'] == user['psw2']:
        return True
    return False


def validate_post(name, post):
    if len(name) < 4 and len(post) < 10:
        return False

    return True
