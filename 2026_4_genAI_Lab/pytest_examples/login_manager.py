def authenticate(username, password):
    if username == "admin" and password == "password":
        return True
    else:
        return False


if __name__ == "__main__":
    username = "admin"
    password = "password"
    expected_result = True
    result = authenticate(username, password)
    
    if result == expected_result:
        print("Test passed")
    else:
        print("Test failed: expected {expected_result} but got {result}")