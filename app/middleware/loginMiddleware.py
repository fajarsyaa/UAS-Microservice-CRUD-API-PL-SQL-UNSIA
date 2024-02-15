def check_login_customer(username, level):
    if user is None:        
        return False

    if level is None:        
        return False

    if level != "customer":
        return False
    
    return True


def check_login_merchant(username, level):
    if user is None:        
        return False

    if level is None:        
        return False

    if level != "merchant":
        return False
    
    return True


def check_login(username):
    if user is None:        
        return True

    return False