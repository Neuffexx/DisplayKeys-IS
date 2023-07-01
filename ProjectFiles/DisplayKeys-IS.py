## Image Splitter made by Neuffexx
## This image splitter was made to allow people to take images they want displayed across their Mountain DisplayPad keys.
## Who asked for this? Me. I did. Because it's a workaround to a problem that shouldn't exist in the first place.
## And I was too lazy to do this to each image manually.
## Was this more effort? Yes. You are welcome.


from PIL import Image, ImageSequence, ImageTk
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


####################################################################################################################
#                                                   Split Image
####################################################################################################################


def get_supported_types():
    # The supported file formats:
    sup_image_formats = [".png", ".jpg", ".jpeg", ".bmp"]
    sup_animated_formats = [".gif"]
    return sup_image_formats, sup_animated_formats


def determine_split_type(file_path, output_dir, rows, cols, gap_horizontal, gap_vertical):
    print("Determening File Type")
    
    # The supported file formats:
    image_formats = get_supported_types()[0]
    animated_formats = get_supported_types()[1]
   
    print("File Types are: ")
    print(get_supported_types()[0])
    print(get_supported_types()[1])
    
    try:
        # Check if image format is supported
        with Image.open(file_path) as image:
            print("Image can be opened: " + ("True" if image else "False") + "\n   Image format is: " + "." + image.format.lower())
            # Is Image
            if "." + image.format.lower() in image_formats:
                split_image(file_path, output_dir, rows, cols, gap_horizontal, gap_vertical)
                return True
            # Is Animated
            elif "." + image.format.lower() in animated_formats:
                split_gif(file_path, output_dir, rows, cols, gap_horizontal, gap_vertical)
                return True
            else:
                print("No formats matched")
                
    # Is not of a supported image format
    except TypeError:
        # In the future simply open a Pop-Up Window with an error message:
        # |----------------------------------------|
        # | File Format not supported \n           |
        # | Currently supported formats are: \n    |
        # | - Image     | get_supported_types()[0] |
        # | - Animated  | get_supported_types()[1] |
        # |----------------------------------------|
        # Do nothing for now
        print("Wrong File Type")
        return None


def split_image(image_path, output_dir, rows, cols, gap_horizontal, gap_vertical):
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Calculate the width and height of each image-cell
    width, height = image.size
    cell_width = (width - (cols - 1) * gap_horizontal) // cols
    cell_height = (height - (rows - 1) * gap_vertical) // rows
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
   
    # Determine the maximum cell size (to maintain square shape)
    max_cell_size = min(cell_width, cell_height)
    
    # Calculate the horizontal and vertical offsets for cropping
    horizontal_offset = (cell_width - max_cell_size) // 2
    vertical_offset = (cell_height - max_cell_size) // 2
   
    # Determine the longest dimension (width or height)
    longest_dimension = "width" if cell_width > cell_height else "height"
    
    # Split the image and save each image-cell
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates for cropping
            left = col * (cell_width + gap_horizontal) + horizontal_offset
            upper = row * (cell_height + gap_vertical) + vertical_offset
            
            # Remove rows/columns only if they are the outermost rows/columns
            if row == 0:
                upper += vertical_offset
            elif row == rows - 1:
                upper -= vertical_offset
            if col == 0:
                left += horizontal_offset
            elif col == cols - 1:
                left -= horizontal_offset
            if longest_dimension == "width":
                right = left + max_cell_size
                lower = upper + cell_height
            else:
                right = left + cell_width
                lower = upper + max_cell_size
            
            # Crop the image-cell
            image_cell = image.crop((left, upper, right, lower))
            
            # Generate the output file path
            output_path = os.path.join(output_dir, f"image_cell_{row}_{col}.png")
            
            # Save the image-cell
            image_cell.save(output_path)
            
            print(f"Saved {output_path}")


def split_gif(gif_path, output_dir, rows, cols, gap_horizontal, gap_vertical):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the image using PIL
    gif = Image.open(gif_path)
    print("GIF Frame Count: " + str(gif.n_frames))
    
    # Extract frames from .gif file
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frames.append(frame.copy())
    
    # Get duration of each frame
    frame_durations = []
    for frame in range(0, gif.n_frames):
        gif.seek(frame)
        try:
            duration = int(gif.info['duration'])
            if duration > 0:
                frame_durations.append(duration)
            else:
                frame_durations.append(0)
        except(KeyError, TypeError):
            print("No frame durations present")
            
            # Add default time in case no frame duration is provided by .gif
            frame_durations.append(0)
    
    # Calculate average duration
    non_zero_durations = [d for d in frame_durations if d > 0]
    if len(non_zero_durations) > 0:
        default_duration = sum(non_zero_durations) // len(non_zero_durations)
    else:
        default_duration = 100
    
    # Replace missing values with average duration
    for i in range(len(frame_durations)):
        if frame_durations[i] == 0:
            frame_durations[i] = default_duration
    print("Frame Durations: \n" + frame_durations.__str__())
    
    # Calculate the width and height of each image-cell
    width, height = frames[0].size
    cell_width = (width - (cols - 1) * gap_horizontal) // cols
    cell_height = (height - (rows - 1) * gap_vertical) // rows
    
    # Determine the maximum cell size (to maintain square format)
    max_cell_size = min(cell_width, cell_height)
    
    # Calculate the horizontal and vertical offsets for cropping
    horizontal_offset = (cell_width - max_cell_size) // 2
    vertical_offset = (cell_height - max_cell_size) // 2
   
    # Determine the longest dimension (width or height)
    longest_dimension = "width" if cell_width > cell_height else "height"
    
    # Split Frames
    modified_frames = []
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates for cropping
            left = col * (cell_width + gap_horizontal) + horizontal_offset
            upper = row * (cell_height + gap_vertical) + vertical_offset
            
            # Remove rows/columns only if they are the outermost rows/columns
            if row == 0:
                upper += vertical_offset
            elif row == rows - 1:
                upper -= vertical_offset
            if col == 0:
                left += horizontal_offset
            elif col == cols - 1:
                left -= horizontal_offset
            if longest_dimension == "width":
                right = left + max_cell_size
                lower = upper + cell_height
            else:
                right = left + cell_width
                lower = upper + max_cell_size
            
            # Perform operation on each frame, for each row/column split image-cell
            for frame in frames:
                # Crop the current frame
                image_cell = frame.crop((left, upper, right, lower))
                # Hold onto cropped image-cell
                modified_frames.append(image_cell)
            
            # Generate the output file path
            output_path = os.path.join(output_dir, f"gif_cell_{row}_{col}.gif")
            print("Num of Modified Frames: " + str(modified_frames.__sizeof__()))
            
            # Save all frames of the image-cell into a single .gif file
            modified_frames[0].save(
                output_path,
                save_all=True,
                append_images=modified_frames[1:],
                duration=frame_durations, # Might make this a user definable variable in the future
                loop=0
            )
            modified_frames = []
            print(f"gif_cell_{row}_{col} has this many frames: " + str(Image.open(output_path).n_frames))
            print(f"Saved {output_path}")


####################################################################################################################
#                                                    GUI Window
####################################################################################################################


### GUI Classes ###


class ImageSplitterGUI:
    def __init__(self, entries):
        #GUI window
        self.window = tk.Tk()
        icon_path = sys._MEIPASS + "./DisplayKeys-IS.ico"
        #app_dir = os.path.dirname(os.path.abspath(__file__))
        #icon_path = os.path.join(app_dir, "./assets/DisplayKeys-IS.ico")
        self.window.iconbitmap(icon_path)
        self.window.title("DisplayKeys-IS")
        self.window.geometry("600x500")
        
        # Configure grid to center horizontally
        self.window.grid_columnconfigure(0, weight=1)  # Set the weight of the first column to expand
        self.window.grid_columnconfigure(1, weight=1)
       
        # User parameter entry widgets
        self.entries = []
        self.create_entries(entries)
        
        # Split Images Button
        self.process_button = tk.Button(
            self.window, text = "Split Image", command=lambda: process_image(self.entries)
        )
        self.process_button.grid(sticky="n")

        # Image Preview
        self.image_previewer = ImagePreviewer(self.window)

        # Hide the Horizontal/Vertical Gap entries initially
        self.update_option_entries()
    
    def create_entries(self, entries):
        created_entries = []
        
        for entry_params in entries:
            entry = EntryWithLabel(
                self.window,
                label_text=entry_params["label"],
                has_textbox=entry_params.get("has_textbox", False),
                has_dropdown=entry_params.get("has_dropdown", False),
                dropdown_label=entry_params.get("dropdown_label", False),
                dropdown_options=entry_params.get("dropdown_options"),
                default_dropdown_option=entry_params.get("default_dropdown_option"),
                button_text=entry_params.get("button_text"),
                button_command=entry_params.get("button_command"),
                tooltip_text=entry_params.get("tooltip", ""),
            )
            entry_params["entry"] = entry
            
            #Create Delegate to for the Gap Drodpwon Options
            if entry_params.get("has_dropdown", False):
                dropdown_options = entry_params.get("dropdown_options")
                if dropdown_options:
                    entry.dropdown_var.trace("w", self.update_option_entries)
            created_entries.append(entry_params)
        self.entries.extend(created_entries)
    
    #Shows / hides the Gap Textboxes that let the user enter the Horizontal/Vertical Gap in pixels
    def update_option_entries(self, *args):
        gap_options_entry = next((entry for entry in self.entries if entry["label"] == "Image Options:"), None)
        horizontal_gap_entry = next((entry for entry in self.entries if entry["label"] == "Horizontal Gap:"), None)
        vertical_gap_entry = next((entry for entry in self.entries if entry["label"] == "Vertical Gap:"), None)
        spacer_entry = next((entry for entry in entries if entry["label"] == "--------------------"), None)
        rows_entry = next((entry for entry in entries if entry["label"] == "Rows:"), None)
        cols_entry = next((entry for entry in entries if entry["label"] == "Columns:"), None)
        
        if gap_options_entry and horizontal_gap_entry and vertical_gap_entry:
            selected_option = gap_options_entry["entry"].dropdown_var.get()
            if selected_option == "Defaults":
                horizontal_gap_entry["entry"].label.grid_remove()
                horizontal_gap_entry["entry"].entry.grid_remove()
                
                vertical_gap_entry["entry"].label.grid_remove()
                vertical_gap_entry["entry"].entry.grid_remove()
                
                spacer_entry["entry"].label.grid_remove()
                
                rows_entry["entry"].label.grid_remove()
                rows_entry["entry"].entry.grid_remove()
                
                cols_entry["entry"].label.grid_remove()
                cols_entry["entry"].entry.grid_remove()
            elif selected_option == "User Defined":
                horizontal_gap_entry["entry"].label.grid()
                horizontal_gap_entry["entry"].entry.grid()
                
                vertical_gap_entry["entry"].label.grid()
                vertical_gap_entry["entry"].entry.grid()
                
                spacer_entry["entry"].label.grid()
                
                rows_entry["entry"].label.grid()
                rows_entry["entry"].entry.grid()
                
                cols_entry["entry"].label.grid()
                cols_entry["entry"].entry.grid()
    
    def run(self):
        # Start the Tkinter event loop
        self.window.mainloop()


class EntryWithLabel:
    def __init__(self, window, label_text, has_textbox=False, has_dropdown=False, dropdown_label=None, dropdown_options=None, default_dropdown_option=None, button_text=None, button_command=None, tooltip_text=""):
        self.label = tk.Label(window, text=label_text)
        self.label.grid(sticky="n")
        
        if has_textbox:
            self.entry = tk.Entry(window)
            self.entry.grid(sticky="n")
        
        if has_dropdown and dropdown_label and dropdown_options:
            self.dropdown_var = tk.StringVar()
            self.dropdown_var.set(dropdown_label)
            self.dropdown = tk.OptionMenu(window, self.dropdown_var, *dropdown_options)
            if default_dropdown_option:
                self.dropdown_var.set(default_dropdown_option)
            else:
                self.dropdown_var.set(dropdown_options[0])
            self.dropdown.grid(sticky="n")
            self.tooltip = Tooltip(self.dropdown, tooltip_text)  # Add tooltip to the dropdown button
        elif has_dropdown and not dropdown_options:
            self.dropdown_var = tk.StringVar()
            self.dropdown_var.set("Dropdown Undefined!")
            self.dropdown = tk.OptionMenu(window, self.dropdown_var, "Dropdown Options Undefined!")
            self.dropdown.grid(sticky="n")
        
        if button_text and button_command:
            self.button = tk.Button(window, text=button_text, command=lambda: button_command(self.entry))
            self.button.grid(sticky="n")
            self.tooltip = Tooltip(self.button, tooltip_text)  # Add tooltip to the button


class ImagePreviewer:
    def __init__(self, window):
        self.window = window
        self.image_path = None  # Initialize the image path as None
        
        # Image Preview
        self.image_label = tk.Label(self.window)
        self.image_label.grid(sticky="n")
        # Set the maximum size of the image preview
        self.image_label.configure(
            width=300, height=300, padx=10, pady=10,
        )

    def update_image(self, image_path=None):
        self.image_path = image_path  # Update the image path

        if self.image_path:
            # Load the image
            image = tk.PhotoImage(file=self.image_path)
            self.image_label.configure(image=image)
            self.image_label.image = image  # Keep a reference to avoid garbage collection
        else:
            self.image_label.configure(image="")
            self.image_label.image = sys._MEIPASS + "./Preview.png"


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        
    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y += self.widget.winfo_rooty()
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1
        )
        label.grid(sticky="n")
        
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


### GUI Functions ###


def browse_image(entry):
    # Open a file dialog for selecting an image file
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, file_path)
        gui.image_previewer.update_image(image_path=file_path)  # Pass the image path

    return file_path


def browse_output(entry):
    # Open a file dialog for selecting an image file
    output_path = filedialog.askdirectory()
    if output_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, output_path)
    return output_path


#Retrives the input parameters from the GUI Windows Entries, and passes it along to the split image function
def process_image(entries):
    # Get the parameter values from the GUI inputs
    image_path_entry = next((entry for entry in entries if entry["label"] == "Image:"), None)
    output_directory_entry = next((entry for entry in entries if entry["label"] == "Output Directory:"), None)
    
    if image_path_entry and output_directory_entry:
        image_path = image_path_entry["entry"].entry.get()
        output_dir = output_directory_entry["entry"].entry.get()
    
    # Get the selected option from the dropdown menu
    gap_options_entry = next((entry for entry in entries if entry["label"] == "Image Options:"), None)
    horizontal_gap_entry = next((entry for entry in entries if entry["label"] == "Horizontal Gap:"), None)
    vertical_gap_entry = next((entry for entry in entries if entry["label"] == "Vertical Gap:"), None)
    rows_entry = next((entry for entry in entries if entry["label"] == "Rows:"), None)
    cols_entry = next((entry for entry in entries if entry["label"] == "Columns:"), None)
    
    if gap_options_entry and horizontal_gap_entry and vertical_gap_entry and rows_entry and cols_entry:
        selected_option = gap_options_entry["entry"].dropdown_var.get()
        # Calculate the gap values based on the selected option
        if selected_option == "Defaults":
            rows = 2
            cols = 6
            gap_horizontal = 40
            gap_vertical = 40
        elif selected_option == "User Defined":
            rows = int(rows_entry["entry"].entry.get())
            cols = int(cols_entry["entry"].entry.get())
            gap_horizontal = int(horizontal_gap_entry["entry"].entry.get())
            gap_vertical = int(vertical_gap_entry["entry"].entry.get())
        else:
            gap_horizontal = 0
            gap_vertical = 0
   
    # Call the image splitting function
    determine_split_type(image_path, output_dir, rows, cols, gap_horizontal, gap_vertical)
    
    print("Process Image Exit")


####################################################################################################################
#                                                    Create GUI
####################################################################################################################


# Define the parameters for each entry
entries = [
    {
        "label": "Made by Neuffexx",
    },
    {
        "label": "-------------------------------------",
    },
    {
        "label": "Image:",
        "has_textbox": True,
        "button_text": "Browse",
        "button_command": browse_image,  # Replace with your function for browsing the image,
        "tooltip": "Select the Image to Split.",
    },
    {
        "label": "Output Directory:",
        "has_textbox": True,
        "button_text": "Browse",
        "button_command": browse_output,  # Replace with your function for browsing the output directory,
        "tooltip": "Select the folder to save split images to.",
    },
    {
        "label": "-------------------------------------",
    },
    {
        "label": "Image Options:",
        "has_dropdown": True,
        "dropdown_label": "Settings Values",
        "dropdown_options": ["Defaults", "User Defined"],
        "default_dropdown_option": "Defaults",
        "tooltip": "Default values are \n Rows: 2 \n Columns; 6 \n Horizontal/Vertical Gap: 40",
    },
    {
        "label": "Rows:",
        "has_textbox": True,
        "tooltip": "The number of Rows the Image will be split into Cells by (aka. Top to Bottom / Vertically).",
    },
    {
        "label": "Columns:",
        "has_textbox": True,
        "tooltip": "The number of Columns the Image will be split into Cells by (aka. Left to Right / Horizontally)",
    },
    {
        "label": "--------------------",
    },
    {
        "label": "Horizontal Gap:",
        "has_textbox": True,
        "tooltip": "Enter the horizontal gap between cells",
    },
    {
        "label": "Vertical Gap:",
        "has_textbox": True,
        "tooltip": "Enter the vertical gap between cells",
    },
    {
        "label": "-------------------------------------",
    },
]


# Create an instance of the ImageSplitterGUI class with the entries
gui = ImageSplitterGUI(entries)
gui.run()
