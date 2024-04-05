#!/usr/bin/python3
import os

import tkinter as tk
import tkinter.filedialog

import numpy as np

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.margins(x=1, y=1, tight=True)

matplotlib.rc('font', size=8)
matplotlib.rc('lines', linewidth=0.5)

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from emotiv.file import EmotivFile, CHANNELS, FS


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        # Variables

        self.data_file_path = tk.StringVar('')
        self.loaded_data = None
        self.active_channel_data = None

        self.active_channel = tk.StringVar()

        self.window_size = tk.IntVar(value=1)
        self.window_offset = tk.IntVar(value=0)

        # Figures

        # Main Frame setup

        self.title("EEG plot")
        # self.resizable(False, False)

        # File selection frame

        frame = tk.Frame(self)

        file_path_entry = tk.Entry(frame, textvariable=self.data_file_path)
        file_path_entry.configure(state="readonly", width=100)
        file_path_entry.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        open_button = tk.Button(frame, text="Open", command=self.select_file)
        open_button.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        active_channel_combobox = tk.OptionMenu(frame, self.active_channel, *CHANNELS)
        active_channel_combobox.configure(width=max([len(c) for c in CHANNELS]))
        active_channel_combobox.pack(side=tk.LEFT, padx=5.0, pady=5.0)
        self.active_channel.trace_add("write", lambda *xargs: self.select_channel())

        frame.pack()

        # Window control frame

        frame = tk.Frame(self)

        back_button = tk.Button(frame, text="<", command=lambda: self.move_window(False))
        back_button.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        next_button = tk.Button(frame, text=">", command=lambda: self.move_window(True))
        next_button.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        window_size_label = tk.Label(frame, text='Window size: ')
        window_size_label.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        window_size_spinbox = tk.Spinbox(frame, from_=1, to=10, textvariable=self.window_size)
        window_size_spinbox.configure(width=3)
        window_size_spinbox.pack(side=tk.LEFT, padx=5.0, pady=5.0)
        # self.window_size.trace_add("write", lambda **xargs: self.update_feature_plots())

        window_size_lebel_sec = tk.Label(frame, text='seconds')
        window_size_lebel_sec.pack(side=tk.LEFT, padx=5.0, pady=5.0)

        frame.pack()

        # Data view frame

        frame = tk.Frame(self)

        figure = Figure(figsize=(20, 4), dpi=80)

        self.file_plot = figure.add_subplot(211)

        # self.area_ptr = Rectangle((0, 0), 128, 6000, color='purple', alpha=0.5)
        # self.area_ptr.set_visible(False)

        # self.file_plot.add_patch(self.area_ptr)

        self.file_spec_plot = figure.add_subplot(212)

        self.file_figure = FigureCanvasTkAgg(figure, frame)
        self.file_figure.get_tk_widget().pack(side=tk.LEFT)
        self.file_figure.draw()

        frame.pack()

        # Feature view frame

        # frame = tk.Frame(self)
        #
        # figure = Figure(figsize=(14, 6), dpi=90)
        # figure.set_tight_layout(True)
        #
        # self.window_plot = figure.add_subplot(321)
        # self.window_fft_plot = figure.add_subplot(322)
        # self.window_div_max_plot = figure.add_subplot(323)
        # self.window_div_sum_plot = figure.add_subplot(324)
        # self.window_var_plot = figure.add_subplot(313)
        #
        # self.window_figure = FigureCanvasTkAgg(figure, frame)
        # self.window_figure.get_tk_widget().pack(side=tk.LEFT)
        # self.window_figure.draw()
        #
        # frame.pack()

        # Start procedure

        # self.select_file()

    def select_file(self):
        init_dir = os.path.dirname(os.path.realpath(__file__))

        if self.data_file_path.get():
            init_dir = os.path.dirname(self.data_file_path.get())

        f = tk.filedialog.askopenfilename(initialdir=init_dir, title="Select file", filetypes=(("csv files", "*.csv"),
                                                                                               ("all files", "*.*")))
        if not f:
            return

        print("loading data")

        self.data_file_path.set(f)

        self.loaded_data = EmotivFile(self.data_file_path.get())
        self.active_channel.set(CHANNELS[0])

        self.active_channel_data = self.loaded_data[self.active_channel.get()]

        # self.area_ptr.set_width(FS * self.window_size.get())
        # self.area_ptr.set_visible(True)

        self.update_file_plot()

    def select_channel(self):
        if self.loaded_data:
            self.active_channel_data = self.loaded_data[self.active_channel.get()]
            self.update_file_plot()

    def move_window(self, increase=True):
        if not self.data_file_path:
            return

        offset = 1 if increase else -1
        offset *= FS

        if not(self.window_pos + offset >= 0
               and self.window_pos + offset + FS * 10 <= len(self.data_file.data)):
            return

        self.window_pos += offset
        self.update_feature_plots()

    def update_file_plot(self):
        # clear plots
        self.file_plot.clear()
        self.file_spec_plot.clear()

        self.file_plot.plot(np.arange(0, len(self.active_channel_data)), self.active_channel_data)
        self.file_plot.set_title("Electroencephalogram", loc="left")

        self.file_spec_plot.specgram(self.active_channel_data, Fs=FS, scale='dB', NFFT=int(FS/2), noverlap=int(FS/4))
        self.file_spec_plot.set_title("Spectrogram", loc="left")

        self.file_figure.figure.tight_layout()
        self.file_figure.draw()

    # def update_feature_plots(self):
    #     if not self.data_file_path:
    #         return
    #
    #     self.file_figure.draw()
    #
    #     channel_idx = CHANNELS.index(self.active_channel.get())
    #     data = self.data_file.data[self.window_pos:self.window_pos + FS * self.window_size.get(), channel_idx]
    #
    #     self.window_plot.clear()
    #     self.window_plot.plot(data)
    #     self.window_plot.set_xlim((0, len(data)))
    #     self.window_plot.set_title("Sygnał okna")
    #
    #     fft_data = extract_fft(data)
    #     self.window_fft_plot.clear()
    #     self.window_fft_plot.plot(fft_data)
    #     self.window_fft_plot.set_xlim((0, len(fft_data)))
    #     self.window_fft_plot.set_yscale('log')
    #     self.window_fft_plot.set_title("Widmo okna")
    #     formatter = matplotlib.ticker.FormatStrFormatter('%d Hz')
    #     self.window_fft_plot.xaxis.set_major_formatter(formatter)
    #
    #     labels = tuple(WAVES_RANGES.keys())
    #     rang = np.arange(len(labels))
    #
    #     self.window_div_max_plot.clear()
    #     self.window_div_max_plot.bar(rang, extract_wrange_max(data))
    #     self.window_div_max_plot.set_xticks(rang)
    #     self.window_div_max_plot.set_xticklabels(labels)
    #     self.window_div_max_plot.set_title("Wartość maksymalna na przedziałach rytmów")
    #
    #     self.window_div_sum_plot.clear()
    #     self.window_div_sum_plot.bar(rang, extract_wrange_sum(data))
    #     self.window_div_sum_plot.set_xticks(rang)
    #     self.window_div_sum_plot.set_xticklabels(labels)
    #     self.window_div_sum_plot.set_title("Suma na przedziałach rytmów")
    #
    #     self.window_var_plot.clear()
    #     self.window_var_plot.boxplot(data, vert=False)
    #     self.window_var_plot.set_title("Parametry statystyczne")
    #
    #     self.area_ptr.set_xy((self.window_pos, 0))
    #     self.area_ptr.set_width(FS * self.window_size.get())
    #     self.file_figure.draw()
    #
    #     self.window_figure.draw()


if __name__ == '__main__':
    MainFrame().mainloop()
