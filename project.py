import os
import json
import track


class Project(object):

    def __init__(self, name):
        self.name = None
        self.filename = None
        self.tracks = [track.Track(0, "New Track")]
        self.target_frame_rate = 60
        self.use_push2_display = True

    def __str__(self):
        return self.name

    def addTrack(self, name):
        track_id = len(self.tracks)
        self.tracks.append(track.Track(track_id, name))

    def removeTrack(self, track_id):
        # check if more than 1 track exists
        if(len(self.tracks) > 1):
            self.tracks.pop(track_id)
        else:
            # replace last track instead of removing it
            self.tracks = [track.Track(0, "New Track")]

    def save(self, filename):
        pass

    def load(self, filename):
        try:
            loaded_file = json.load(open(filename))
            self.name = loaded_file.get('name')
            self.filename = filename
            self.tracks = loaded_file.get('tracks')
        except:
            print("File Error")
