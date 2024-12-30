import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import time
import threading
from tkinter import PhotoImage
import webbrowser

LOG_FILE = "edl_detection_gui.log"

def log_message(message):
    """Log messages to a file and update the log display."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    log_text.insert(tk.END, f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    log_text.see(tk.END)

def check_edl_mode():
    """Continuously check for Xiaomi device in EDL mode."""
    def worker():
        while edl_check_running:
            try:
                result = subprocess.check_output("lsusb", shell=True, text=True)
                if "05c6:9008" in result.lower():
                    messagebox.showinfo("Device Found", "🎉 Xiaomi device found in EDL mode! 🚀")
                    log_message("EDL mode device detected.")
                    break
                else:
                    log_message("No EDL device found. Retrying...")
            except Exception as e:
                log_message(f"Error checking EDL mode: {e}")
            time.sleep(3)
        toggle_buttons(True)

    global edl_check_running
    edl_check_running = True
    toggle_buttons(False)
    threading.Thread(target=worker, daemon=True).start()

def list_devices():
    """List all connected USB devices."""
    try:
        result = subprocess.check_output("lsusb", shell=True, text=True)
        log_message("Listing connected USB devices:")
        log_message(result)
        messagebox.showinfo("USB Devices", f"Connected devices:\n{result}")
    except Exception as e:
        log_message(f"Error listing USB devices: {e}")
        messagebox.showerror("Error", "Failed to list devices. Make sure 'lsusb' is installed.")

def restart_adb():
    """Restart the ADB server."""
    try:
        subprocess.run("adb kill-server", shell=True, check=True)
        subprocess.run("adb start-server", shell=True, check=True)
        log_message("ADB server restarted successfully.")
        messagebox.showinfo("Success", "ADB server restarted.")
    except Exception as e:
        log_message(f"Error restarting ADB: {e}")
        messagebox.showerror("Error", "Failed to restart ADB server.")

def fastboot_to_edl():
    """Reboot device to EDL mode via Fastboot."""
    try:
        subprocess.run("fastboot oem edl", shell=True, check=True)
        log_message("Device rebooted into EDL mode via Fastboot.")
        messagebox.showinfo("Success", "Device rebooted into EDL mode.")
    except Exception as e:
        log_message(f"Error rebooting to EDL: {e}")
        messagebox.showerror("Error", "Failed to reboot device to EDL mode. Ensure it's in Fastboot mode.")

def view_log():
    """Open the log file in a scrollable text window."""
    log_window = tk.Toplevel(root)
    log_window.title("Log File")
    log_window.geometry("600x400")
    log_text_widget = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
    log_text_widget.pack(expand=True, fill=tk.BOTH)
    try:
        with open(LOG_FILE, "r") as log_file:
            log_text_widget.insert(tk.END, log_file.read())
    except FileNotFoundError:
        log_text_widget.insert(tk.END, "No logs available yet.")

def toggle_buttons(state):
    """Enable or disable buttons."""
    btn_check_edl.config(state=tk.NORMAL if state else tk.DISABLED)
    btn_list_devices.config(state=tk.NORMAL if state else tk.DISABLED)
    btn_restart_adb.config(state=tk.NORMAL if state else tk.DISABLED)
    btn_fastboot_to_edl.config(state=tk.NORMAL if state else tk.DISABLED)
    btn_view_log.config(state=tk.NORMAL if state else tk.DISABLED)

def stop_checking():
    """Stop continuous checking for EDL mode."""
    global edl_check_running
    edl_check_running = False
    log_message("Stopped EDL mode checking.")
    toggle_buttons(True)

def open_link(url):
    """Open the URL in a web browser."""
    webbrowser.open(url)

def show_about():
    """Show About window with credit and project info."""
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("450x450")
    about_window.resizable(False, False)

    # Create frame to provide padding
    frame = tk.Frame(about_window, padx=15, pady=15, bg="#f9f9f9", relief="solid", bd=1)
    frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    about_text = """
    Xiaomi EDL Tool

    This tool helps you manage Xiaomi devices in EDL mode. You can check if a device is in EDL mode, list connected USB devices, 
    restart the ADB server, and reboot the device into EDL mode via Fastboot.

    Developer:
    Nishchal Acharya
    """

    # Text widget to display the content
    text_widget = tk.Text(frame, wrap=tk.WORD, height=12, width=50, bd=0, font=("Helvetica", 11), bg="#f9f9f9", fg="#333")
    text_widget.insert(tk.END, about_text)
    text_widget.config(state=tk.DISABLED)  # Set the text to read-only

    text_widget.pack(expand=True, fill=tk.BOTH)

    # Links section
    links_frame = tk.Frame(frame, bg="#f9f9f9")
    links_frame.pack(pady=10)

    links = {
        "Twitter": "https://twitter.com/nishchal_acc",
        "LinkedIn": "https://www.linkedin.com/in/nishchalacharya",
        "GitHub": "https://github.com/Nischal-Acharya",
        "Portfolio": "https://nishchalacharya.com.np"
    }

    # Loop to create clickable buttons for each link
    for link_text, url in links.items():
        link_button = tk.Button(links_frame, text=link_text, font=("Helvetica", 12), fg="blue", bg="#f9f9f9", relief="flat", cursor="hand2", command=lambda u=url: open_link(u))
        link_button.pack(pady=5)

    # Close button
    btn_close = tk.Button(about_window, text="Close", command=about_window.destroy, bg="#f9f9f9", fg="black", font=("Helvetica", 12), relief="flat")
    btn_close.pack(pady=15)

# Create the GUI
root = tk.Tk()
icon = PhotoImage(file="icon.png")  
root.tk.call('wm', 'iconphoto', root._w, icon)

root.title("Xiaomi EDL Tool")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#f9f9f9")  # Light background color

# Modern Header
header_label = tk.Label(root, text="Xiaomi EDL Tool", font=("Helvetica", 18, "bold"), fg="#ff7300", bg="#f9f9f9")
header_label.pack(pady=15)

# Define a light color for buttons
button_bg = "#ffc799"  # Light background color for buttons
button_fg = "black"  # Black text for contrast

# Buttons for functionality
btn_check_edl = tk.Button(root, text="Check EDL Mode Continuously", command=check_edl_mode, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_check_edl.pack(pady=5)

btn_list_devices = tk.Button(root, text="List Connected USB Devices", command=list_devices, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_list_devices.pack(pady=5)

btn_restart_adb = tk.Button(root, text="Restart ADB Server", command=restart_adb, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_restart_adb.pack(pady=5)

btn_fastboot_to_edl = tk.Button(root, text="Reboot Device to EDL Mode (Fastboot)", command=fastboot_to_edl, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_fastboot_to_edl.pack(pady=5)

btn_view_log = tk.Button(root, text="View Log File", command=view_log, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_view_log.pack(pady=5)

btn_stop = tk.Button(root, text="Stop Checking", command=stop_checking, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_stop.pack(pady=15)

# About button
btn_about = tk.Button(root, text="About", command=show_about, width=30, bg=button_bg, fg=button_fg, font=("Helvetica", 12), relief="flat")
btn_about.pack(pady=5)

# Log area
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Helvetica", 10))
log_text.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

log_message("Tool started. Ready for action!")

root.mainloop()
