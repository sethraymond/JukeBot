from gmusicapi import Mobileclient
import getpass

class GpmSession(object):
    # Private Variables

    # Public Variables
    api = None
    logged_in = False
    songs = None
    playlists = None

    def __init__(self):
        self.api = Mobileclient()
        email = input("Please enter an email address tied to a GPM account: ")
        pw = getpass.getpass("Please enter the password associated with %s " % email)
        self.logged_in = self.api.login(email, pw, Mobileclient.FROM_MAC_ADDRESS) # As per api protocol
        if self.logged_in:
            print("Login successful")
        else:
            print("Login failed")

    def init(self, songs = True, playlists = True):
        if songs:
            self.songs = self.api.get_all_songs()
        if playlists:
            self.playlists = self.api.get_all_playlists()

    def get_song(self, title, artist=None):
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
            result = result & (song_obj["title"] == search_title)
        if search_artist:
            result = result & (song_obj["artist"] == search_artist)
        return result

def main():
    session = GpmSession()
    while not session.logged_in:
        session = GpmSession()
    session.init()
    print(session.get_song("Dirty Laundry", "Bitter Sweet"))
    print(session.get_song("1940"))

if __name__ == "__main__":
    main()