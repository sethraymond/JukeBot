from gmusicapi import Mobileclient
import getpass

class GpmSession(object):
    # Private Variables

    # Public Variables
    api = None
    logged_in = False
    songs = None
    playlists = None
    current_queue = list() 
    non_lib_played_queue = list()

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

    def get_all_library_music(self, songs = True, playlists = True):
        if songs:
            self.songs = self.api.get_all_songs() #all songs from library
        if playlists:
            self.playlists = self.api.get_all_playlists() #all playlists from library

    def get_song_stream(self, song):
        print(song)
        return self.api.get_stream_url(song["id"])

    def search_store(self, search_title, search_artist = None, search_album = None):
        hits = self.api.search(search_title)["song_hits"]
        print("Searching for :", search_title, "by: ", search_artist, "From album: ", search_album)
        if search_artist is not None:
            print("searching by artist")
            for song in hits:
                if song["track"]["artist"] == search_artist:
                    print(song["track"]["artist"], "is equal to ", search_artist)
                    my_song = song["track"]
        if search_album is not None:
            print("searching by album")
            for song in hits:
                if song["track"]["album"] == search_album:
                    my_song = song["track"]

        if search_artist is None or search_album is None:
            return my_song
        else:
            return hits

    def add_song_to_library(self, song):
        lib_track = self.api.add_store_track(song["storeId"])
        return lib_track

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
    session.get_all_library_music()
    print(session.search_store("Mother May I", "Coheed and Cambria"))

if __name__ == "__main__":
    main()
