def validate_user(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blanc"
    return errors


def validate_post(name, post):
    if len(name) < 4 and len(post) < 10:
        return False

    return True
