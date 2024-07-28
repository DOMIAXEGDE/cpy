import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import wave
import os

class AudioTrack:
    def __init__(self, name, duration, start_time):
        self.name = name
        self.duration = duration
        self.start_time = start_time
        self.audio = None

    def set_audio(self, audio):
        self.audio = audio

    def process_audio(self, volume_change=None, pitch_change=None, reverse=False):
        if volume_change is not None:
            self.audio = self.audio + volume_change
        if pitch_change is not None:
            rate = self.audio.frame_rate * (2.0 ** (pitch_change / 12.0))
            self.audio = self.audio._spawn(self.audio.raw_data, overrides={'frame_rate': int(rate)}).set_frame_rate(self.audio.frame_rate)
        if reverse:
            self.audio = self.audio.reverse()

class AudioEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Audio Editor")
        self.sample_rate = 44100
        self.tracks = []
        self.track_count = 0

        self.create_widgets()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Add Track", command=self.add_track_form)
        options_menu.add_command(label="Process and Save", command=self.process_and_save)

        # Track frame
        self.track_frame = tk.Frame(self.master)
        self.track_frame.pack(fill=tk.BOTH, expand=True)

        # Control frame
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack()

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_audio)
        self.play_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_audio)
        self.stop_button.pack(side=tk.LEFT)

    def add_track_form(self):
        self.track_form = tk.Toplevel(self.master)
        self.track_form.title("Add Track")

        tk.Label(self.track_form, text="Track Name:").pack()
        self.track_name_entry = tk.Entry(self.track_form)
        self.track_name_entry.pack()

        tk.Label(self.track_form, text="Duration (seconds):").pack()
        self.duration_entry = tk.Entry(self.track_form)
        self.duration_entry.pack()

        tk.Label(self.track_form, text="Start Time (seconds):").pack()
        self.start_time_entry = tk.Entry(self.track_form)
        self.start_time_entry.pack()

        tk.Button(self.track_form, text="Submit", command=self.add_track).pack()

    def add_track(self):
        track_name = self.track_name_entry.get()
        track_duration = float(self.duration_entry.get())
        track_start_time = float(self.start_time_entry.get()) * 1000

        track = AudioTrack(track_name, track_duration, track_start_time)
        self.tracks.append(track)

        self.record_audio(track_duration, f"{track_name}.wav")
        track.set_audio(self.load_audio(f"{track_name}.wav"))

        self.add_track_widgets(track)
        self.track_form.destroy()

    def add_track_widgets(self, track):
        track_frame = tk.Frame(self.track_frame, relief=tk.RAISED, borderwidth=1)
        track_frame.pack(fill=tk.X, padx=5, pady=5)

        track_label = tk.Label(track_frame, text=track.name)
        track_label.pack(side=tk.LEFT, padx=5)

        volume_label = tk.Label(track_frame, text="Volume:")
        volume_label.pack(side=tk.LEFT, padx=5)

        volume_combo = ttk.Combobox(track_frame, values=[-10, -5, 0, 5, 10])
        volume_combo.pack(side=tk.LEFT, padx=5)
        volume_combo.current(2)

        pitch_label = tk.Label(track_frame, text="Pitch:")
        pitch_label.pack(side=tk.LEFT, padx=5)

        pitch_combo = ttk.Combobox(track_frame, values=[-12, -6, 0, 6, 12])
        pitch_combo.pack(side=tk.LEFT, padx=5)
        pitch_combo.current(2)

        reverse_var = tk.BooleanVar()
        reverse_check = tk.Checkbutton(track_frame, text="Reverse", variable=reverse_var)
        reverse_check.pack(side=tk.LEFT, padx=5)

        process_button = tk.Button(track_frame, text="Process", command=lambda: self.process_track(track, volume_combo, pitch_combo, reverse_var))
        process_button.pack(side=tk.LEFT, padx=5)

    def record_audio(self, duration, filename):
        print(f"Recording {filename} for {duration} seconds...")
        recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()
        print(f"Recording {filename} finished")

        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.sample_rate)
            wf.writeframes(recording.tobytes())

    def load_audio(self, file_path):
        return AudioSegment.from_file(file_path)

    def save_audio(self, audio, file_path):
        audio.export(file_path, format="wav")

    def process_track(self, track, volume_combo, pitch_combo, reverse_var):
        volume_change = int(volume_combo.get())
        pitch_change = int(pitch_combo.get())
        reverse = reverse_var.get()

        track.process_audio(volume_change, pitch_change, reverse)
        messagebox.showinfo("Info", f"{track.name} processed")

    def layer_audios(self, tracks):
        combined_duration = max(track.start_time + len(track.audio) for track in tracks)
        combined = AudioSegment.silent(duration=combined_duration)
        for track in tracks:
            combined = combined.overlay(track.audio, position=track.start_time)
        return combined

    def process_and_save(self):
        if not self.tracks:
            messagebox.showerror("Error", "No tracks added.")
            return

        layered_audio = self.layer_audios(self.tracks)
        save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
        if save_path:
            self.save_audio(layered_audio, save_path)
            messagebox.showinfo("Info", f"Final audio saved as {save_path}")

            # Clean up temporary files
            for track in self.tracks:
                os.remove(f"{track.name}.wav")

    def play_audio(self):
        if not self.tracks:
            messagebox.showerror("Error", "No tracks to play.")
            return

        layered_audio = self.layer_audios(self.tracks)
        samples = np.array(layered_audio.get_array_of_samples())
        play_obj = sd.play(samples, samplerate=layered_audio.frame_rate)
        sd.wait()

    def stop_audio(self):
        sd.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioEditorApp(root)
    root.mainloop()
