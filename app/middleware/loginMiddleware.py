def check_login_customer(user, level):
    if user is None:        
        return True

    if level is None or level.lower() != "customer":        
        return True

    return False


def check_login_merchant(user, level):
    if user is None:        
        return True

    if level is None or level.lower() != "merchant":        
        return True
    
    return False


def check_login(user):
    if not user:        
        return False

    return True
