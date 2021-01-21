import tkinter as tk
import tkinter.ttk as ttk

from usb_led import USBLed

def main():
    led = USBLed()
    led.open()

    window = tk.Tk()

    def sliderupdate(*args):
        color = (redslider.get(), greenslider.get(), blueslider.get())
        led.set_color(color)
        Canvas.config(bg="#{:02x}{:02x}{:02x}".format(*color))

    redslider = tk.Scale(window, from_=0, to=255, command=sliderupdate)
    greenslider = tk.Scale(window, from_=0, to=255, command=sliderupdate)
    blueslider = tk.Scale(window, from_=0, to=255, command=sliderupdate)
    Canvas = tk.Canvas(window, width=200, height=200)

    redslider.grid(row=1, column=1)
    greenslider.grid(row=1, column=2)
    blueslider.grid(row=1, column=3)
    Canvas.grid(row=2, column=1, columnspan=3)
    sliderupdate()

    window.mainloop()
    led.close()

if __name__ == "__main__":
    main()
