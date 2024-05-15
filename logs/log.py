from json import dumps


# Save json to userbooks.log
def save_userbooks_log(json_data):
    open("./logs/userbooks.log", "a+").write(dumps(json_data) + ", ")
