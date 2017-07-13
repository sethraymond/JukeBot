from gmusicapi import Mobileclient
import getpass

class GpmSession(object):
    # Private Variables

    # Public Variables
    api = None
    logged_in = False
    songs = None
    playlists = None

    # Constructor with optionally passed credentials
    # Omit credentials if you want to handle login, include for prompts from this module
    def __init__(self, email=None, pw=None):
        self.api = Mobileclient()
        if not email and not pw:
            email = input("Please enter an email address tied to a GPM account: ")
            pw = getpass.getpass("Please enter the password associated with %s: " % email)
        self.logged_in = self.api.login(email, pw, Mobileclient.FROM_MAC_ADDRESS) # As per api protocol
        if self.logged_in:
            print("Google Play Music login successful")
        else:
            print("Google Play Music login failed")

    def init(self, songs = True, playlists = True):
        if songs:
            self.songs = self.api.get_all_songs()
        if playlists:
            self.playlists = self.api.get_all_playlists()

    def get_song_stream(self, title, artist=None):
        print(not self.songs)
        if not self.songs:
            self.init(True, False)
        song = next(iter((track for track in self.songs if self._filter_condition(track, title, artist)) or []), None)
        if song:
            return self.api.get_stream_url(song["id"])
        else:
            return None


    def _filter_condition(self, song_obj, search_title, search_artist):
        result = True
        if search_title:
            result = result & (song_obj["title"].lower().strip() == search_title.lower().strip())
        if search_artist:
            result = result & (song_obj["artist"].lower().strip() == search_artist.lower().strip())
        return result

def main():
    session = GpmSession()
    while not session.logged_in:
        session = GpmSession()
    session.init()
    print(session.get_song_stream("Dirty Laundry", "Bitter Sweet"))
    print(session.get_song_stream("1940"))

if __name__ == "__main__":
    main()
