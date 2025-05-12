# notes.py
import pandas as pd

class NoteManager:
    def __init__(self, notes_file):
        self.notes = self.load_notes(notes_file)

    def load_notes(self, file):
        try:
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            print("Error loading notes:", e)
            return pd.DataFrame()

    def get_note_text(self, note_id):
        note = self.notes[self.notes['Note_ID'] == int(note_id)]
        if not note.empty:
            return note['Note_text'].values[0]
        return "Note text not found."
