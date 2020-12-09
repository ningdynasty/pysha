class Track(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.midi_device_out = None
        self.midi_channel_out = None
        self.midi_device_in = None
        self.midi_channel_in = None
        self.midi_through = None
        self.grid_layout = None
        self.notes_being_played = []
        self.root_midi_note = 64
        self.fixed_velocity_mode = False
        self.use_poly_at = True
        self.channel_at_range_start = 401
        self.channel_at_range_end = 800
        self.poly_at_max_range = 40
        self.poly_at_curve_bending = 50
        self.latest_channel_at_value = (0, 0)
        self.latest_poly_at_value = (0, 0)
        self.latest_velocity_value = (0, 0)
        self.last_time_at_params_edited = None
        self.modulation_wheel_mode = False

    def __str__(self):
        return self.name

    def set_channel_at_range_start(self, value):
        # Parameter in range [401, channel_at_range_end - 1]
        if value < 401:
            value = 401
        elif value >= self.channel_at_range_end:
            value = self.channel_at_range_end - 1
        self.channel_at_range_start = value
        self.last_time_at_params_edited = time.time()

    def set_channel_at_range_end(self, value):
        # Parameter in range [channel_at_range_start + 1, 2000]
        if value <= self.channel_at_range_start:
            value = self.channel_at_range_start + 1
        elif value > 2000:
            value = 2000
        self.channel_at_range_end = value
        self.last_time_at_params_edited = time.time()

    def set_poly_at_max_range(self, value):
        # Parameter in range [0, 127]
        if value < 0:
            value = 0
        elif value > 127:
            value = 127
        self.poly_at_max_range = value
        self.last_time_at_params_edited = time.time()

    def set_poly_at_curve_bending(self, value):
        # Parameter in range [0, 100]
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.poly_at_curve_bending = value
        self.last_time_at_params_edited = time.time()

    def get_poly_at_curve(self):
        pow_curve = [pow(e, 3*self.poly_at_curve_bending/100)
                     for e in [i/self.poly_at_max_range for i in range(0, self.poly_at_max_range)]]
        return [int(127 * pow_curve[i]) if i < self.poly_at_max_range else 127 for i in range(0, 128)]

    def add_note_being_played(self, midi_note, source):
        self.notes_being_played.append({'note': midi_note, 'source': source})

    def remove_note_being_played(self, midi_note, source):
        self.notes_being_played = [
            note for note in self.notes_being_played if note['note'] != midi_note or note['source'] != source]

    def remove_all_notes_being_played(self):
        self.notes_being_played = []

    def is_midi_note_being_played(self, midi_note):
        for note in self.notes_being_played:
            if note['note'] == midi_note:
                return True
        return False

    def set_root_midi_note(self, note_number):
        self.root_midi_note = note_number
        if self.root_midi_note < 0:
            self.root_midi_note = 0
        elif self.root_midi_note > 127:
            self.root_midi_note = 127
