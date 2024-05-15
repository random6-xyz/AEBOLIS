from json import dumps, loads


# Save json to userbooks.log
def save_userbooks_log(json_data):
    open("./logs/userbooks.log", "a+").write(dumps(json_data) + ", ")


# reset log file
def reset_uesrbooks_log(json_data):
    open("./logs/userbooks.log", "w+").write(dumps(json_data))


# Load json from userbooks.log
def load_userbooks_log():
    return loads("[" + open("./logs/userbooks.log", "r").read().rstrip(", ") + "]")
