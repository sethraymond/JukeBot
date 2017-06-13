from gmusicapi import Mobileclient
import getpass

class GpmSession(object):
    # Private Variables

    # Public Variables
    api = None
    logged_in = False

    def __init__(self):
        self.api = Mobileclient()
        email = input("Please enter an email address tied to a GPM account: ")
        pw = getpass.getpass("Please enter the password associated with %s " % email)
        self.logged_in = self.api.login(email, pw, Mobileclient.FROM_MAC_ADDRESS) # As per api protocol
        if self.logged_in:
            print("Login successful")
        else:
            print("Login failed")

def main():
    print("main does nothing")

if __name__ == "__main__":
    main()