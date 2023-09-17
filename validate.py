def validate(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blanc"
    return errors
#test
