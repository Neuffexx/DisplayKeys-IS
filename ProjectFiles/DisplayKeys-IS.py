import os, sys
from PIL import Image, ImageTk, ImageSequence, ImageDraw
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


####################################################################################################################
#                                                    GUI Window
####################################################################################################################


# The Main Application Window
class DisplayKeys_GUI:
    def __init__(self, widgets):
        print("---Creating Window---")
        self.window = tk.Tk()
        self.window.title("DisplayKeys-IS")
        icon_path = sys._MEIPASS + "./DisplayKeys-IS.ico"
        self.window.iconbitmap(icon_path)
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        #########################

        print("---Creating Left Column---")
        # Create the Properties Frame
        self.properties_frame = tk.Frame(self.window, width=200, height=500)
        self.properties_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.properties_frame.grid_columnconfigure(0, weight=1)
        # Populate the properties frame with widgets
        self.properties = []
        self.properties = self.populate_column(self.properties_frame, widgets)

        print("---Creating Right Column---")
        # Create the Preview Frame
        self.preview_frame = tk.Frame(self.window, height=500)
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        # Create the Preview widget and place it in the right column
        # preview = PreviewPlaceholder(self.preview_frame)
        self.preview = DisplayKeys_Previewer(self.preview_frame, width=350, height=350)
        self.update_preview_button = DisplayKeys_Widget(self.preview_frame, 'UpdatePreview', button_label="Update Preview", button_command=ButtonFunctions.process_preview, button_tooltip="Update the Preview")
        self.update_preview_button.grid(sticky="n")

        #########################

        # Initially Hide Options Based on Dropdown Selection
        ButtonFunctions.property_options_visibility(self.properties)

    # Used to populate a column(frame) with widgets
    def populate_column(self, parent, widgets):
        created_widgets = []
        for widget in widgets:
            created_widgets.append(DisplayKeys_Widget(parent, **widget))

        return created_widgets

    # Starts the Window loop
    def run(self):
        self.window.mainloop()


# The Widget that show's all changes done to the Image within the Application
class DisplayKeys_Previewer:
    def __init__(self, parent, width, height):
        self.width = width
        self.height = height
        self.image_path = sys._MEIPASS + "./Preview.png"

        # Initialize canvas
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height)
        self.canvas.grid()

        # Load and show the initial placeholder image
        self.display_preview_image(self.image_path)

    def display_preview_image(self, image_path):
        image = Image.open(image_path)

        # Rescaling image to fit within preview boundaries
        aspect_ratio = image.width / image.height
        if self.width / self.height >= aspect_ratio:
            # Constrained by height
            new_height = self.height
            new_width = int(self.height * aspect_ratio)
        else:
            # Constrained by width
            new_width = self.width
            new_height = int(self.width / aspect_ratio)
        self.scale_factor = new_width / image.width
        resized_image = image.resize((new_width, new_height))

        # Convert to PhotoImage to be used in TkInter Canvas
        self.tk_image = ImageTk.PhotoImage(resized_image)
        x_offset = (self.width - new_width) / 2
        y_offset = (self.height - new_height) / 2
        self.canvas.create_image(x_offset, y_offset, image=self.tk_image, anchor=tk.NW)

        self.resized_image = resized_image
        self.x_offset = x_offset
        self.y_offset = y_offset

    def update(self, image_path, rows, columns, gap):
        # Clear the canvas of anything drawn on it from before
        self.canvas.delete("all")

        # Load new image
        self.display_preview_image(image_path)

        # Calculate dimensions of each image-cell
        image_width, image_height = self.resized_image.size
        cell_width = image_width / columns
        cell_height = image_height / rows
        scaled_gap = gap * self.scale_factor

        # Calculate and Draw Cropping Overlay
        square_size = min(cell_width, cell_height) - scaled_gap
        for i in range(columns):
            for j in range(rows):
                # Calculating cropping area
                x1 = i * cell_width + (cell_width - square_size) / 2 + self.x_offset
                y1 = j * cell_height + (cell_height - square_size) / 2 + self.y_offset
                x2 = x1 + square_size
                y2 = y1 + square_size

                # Drawing the cropping overlay
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")

                # Drawing cropping overlays for inner cells
                if cell_width > square_size:
                    self.canvas.create_rectangle(x1, y1, i * cell_width + self.x_offset, y2, fill="gray",
                                                 stipple="gray25")
                    self.canvas.create_rectangle(x2, y1, (i + 1) * cell_width + self.x_offset, y2, fill="gray",
                                                 stipple="gray25")
                if cell_height > square_size:
                    self.canvas.create_rectangle(x1, y1, x2, j * cell_height + self.y_offset, fill="gray",
                                                 stipple="gray25")
                    self.canvas.create_rectangle(x1, y2, x2, (j + 1) * cell_height + self.y_offset, fill="gray",
                                                 stipple="gray25")

        # Draw Grid Lines with adjusted width to factor in Gap.
        # Grid is drawn after Cropping Overlay so that its more clear
        # what is removed by either cropping or the gap.
        for i in range(1, columns):
            x = i * cell_width + self.x_offset
            self.canvas.create_line(x, self.y_offset, x, image_height + self.y_offset, fill="red",
                                    width=scaled_gap)
        for i in range(1, rows):
            y = i * cell_height + self.y_offset
            self.canvas.create_line(self.x_offset, y, image_width + self.x_offset, y, fill="red",
                                    width=scaled_gap)


# Generic Widgets used throughout the Applications UI (ie. Textboxes, Buttons, etc.)
class DisplayKeys_Widget(tk.Frame):
    def __init__(self, parent, widget_id, label_text=None, label_tooltip=None, dropdown_options=None, dropdown_tooltip=None, dropdown_command=None,
                 has_textbox=False, textbox_state="normal", default_value=None, button_label=None, button_command=None,
                 button_tooltip=None):
        super().__init__(parent)
        self.grid(sticky="n")

        # The reference name by which button functions will find this widget
        self.id = widget_id

        # Text Label - Text that is non-interactive (ie. A Tittle)
        # Takes: Label Text, Label Tooltip
        if label_text:
            self.label = tk.Label(self, text=label_text)
            self.label.grid(sticky="n")

            if label_tooltip:
                self.l_tooltip = DisplayKeys_Tooltip(self.label, label_tooltip)

        # Dropdown Button - This is set up to be used with anything
        # All it needs is options and what command that will use the widgets to perform operations on.
        # Takes: Options Text Array, Command, Tooltip Text
        if dropdown_options and dropdown_command:
            self.dropdown_var = tk.StringVar()
            self.dropdown_var.set(dropdown_options[0])  # Set default value
            self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var, values=dropdown_options, state="readonly", justify="left")
            self.dropdown.grid(sticky="n")
            # Bind the selection change event to the dropdown command
            self.dropdown.bind("<<ComboboxSelected>>", lambda event: dropdown_command(app.properties))

            if dropdown_tooltip:
                self.d_tooltip = DisplayKeys_Tooltip(self.dropdown, dropdown_tooltip)

        # Textbox - Mainly used for getting user input, but can also be used as a good place to dynamically show text
        # Takes: Default Text Value, Tooltip Text, State 
        if has_textbox:
            self.textbox = tk.Entry(self, state=textbox_state)
            if default_value:
                self.textbox_default = default_value

            self.textbox.grid(sticky="n")

        # Button - Used specifically to call any function in the Application
        # Provides the function with its own ID in case the function needs to access its parents.
        # Takes: Label Text, Command, Tooltip Text
        if button_label and button_command:
            self.button = tk.Button(self, text=button_label, command= lambda: button_command(self.id))
            self.button.grid(sticky="n")

            if button_tooltip:
                self.b_tooltip = DisplayKeys_Tooltip(self.button, button_tooltip)


# A Tooltip that can be assigned to any of the DisplayKeys_Widgets
class DisplayKeys_Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    # Tooltip Position is always to the right of the widget,
    # in case the widget has click functionality so that it get in the way.
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


class ButtonFunctions:
    # Debug:
    # For testing new UI without wanting any actual actions taken.
    def placeholder(widget_id):
        print("Placeholder Function")
        return

    @staticmethod
    # For Debugging the process_image function
    def placeholder_process(image_path, output_dir, rows, columns, gap):
        print("ImagePath: " + image_path)
        print("OutputPath: " + output_dir)
        print("Rows: " + rows)
        print("Columns: " + columns)
        print("Gap: " + gap)
        return
    
    # Main Window Functions:
    # Buttons
    # Grabs the Path to an Image, and if possible adds this into a widgets textbox
    def browse_image(widget_id):
        print("---Browsing for Image---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)

        if widget:
            # Ask the user to select an Image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
            )
            # Put File Path into textbox if widget has a textbox
            if file_path and widget.textbox:
                widget_original_state = widget.textbox.__getitem__('state')
                print("Original Textbox State: " + widget_original_state)

                widget.textbox.configure(state='normal')
                widget.textbox.delete(0, tk.END)
                widget.textbox.insert(tk.END, file_path)
                widget.textbox.configure(state=widget_original_state)

            # Just in case its ever needed
            return file_path

    # Grabs the Path to a Directory, and if possible adds this into a widgets textbox
    def browse_directory(widget_id):
        print("---Browsing for Output Dir---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)
        
        if widget:
            # Request the user to select a Directory
            output_path = filedialog.askdirectory()
            # Put Directory Path into textbox if widget has a textbox 
            if output_path and widget.textbox:
                widget_original_state = widget.textbox.__getitem__('state')
                print("Original Textbox State: " + widget_original_state)

                widget.textbox.configure(state='normal')
                widget.textbox.delete(0, tk.END)
                widget.textbox.insert(tk.END, output_path)
                widget.textbox.configure(state=widget_original_state)

            # Just in case its ever needed
            return output_path

    # Grabs all available parameters and passes it along, to split the provided image.
    # Currently, defaults are provided for any of the required inputs that are missing.
    def process_image(widget_id):
        print("---Processing Images---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)
        widgets = app.properties

        # Get Image Properties Type
        get_params_type_widget = next((widget for widget in widgets if widget.id == "GetParamsType"), None)

        # Get Text boxes to process image
        get_image_widget = next((widget for widget in widgets if widget.id == "GetImage"), None)
        get_output_widget = next((widget for widget in widgets if widget.id == "GetOutput"), None)
        get_rows_widget = next((widget for widget in widgets if widget.id == "GetRows"), None)
        get_columns_widget = next((widget for widget in widgets if widget.id == "GetColumns"), None)
        get_gap_widget = next((widget for widget in widgets if widget.id == "GetGap"), None)

        if all(widget is not None for widget in [
            get_image_widget, get_output_widget, get_rows_widget, get_columns_widget, get_gap_widget, get_params_type_widget
        ]):
            # Determine if the default or user defined values should be used
            if get_params_type_widget.dropdown_var.get() == "Defaults":
                image_path = get_image_widget.textbox.get()
                if not image_path:
                    image_path = sys._MEIPASS + "./Preview.png"
                output_dir = get_output_widget.textbox.get() if get_output_widget.textbox.get() else None
                if not output_dir:
                    output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                rows = int(get_rows_widget.textbox_default)
                columns = int(get_columns_widget.textbox_default)
                gap = int(get_gap_widget.textbox_default)
            # Get the text from the required textboxes
            elif get_params_type_widget.dropdown_var.get() == "User Defined":
                image_path = get_image_widget.textbox.get() if get_image_widget.textbox.get() else None
                output_dir = get_output_widget.textbox.get() if get_output_widget.textbox.get() else None
                rows = int(get_rows_widget.textbox.get()) if get_rows_widget.textbox.get().isnumeric() else None
                columns = int(get_columns_widget.textbox.get()) if get_columns_widget.textbox.get().isnumeric() else None
                gap = int(get_gap_widget.textbox.get()) if get_gap_widget.textbox.get().isnumeric() else None

                if not image_path:
                    image_path = sys._MEIPASS + "./Preview.png"
                if not output_dir:
                    output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                if not rows:
                    rows = int(get_rows_widget.textbox_default)
                if not columns:
                    columns = int(get_columns_widget.textbox_default)
                if not gap:
                    gap = int(get_gap_widget.textbox_default)
            else:
                return

            # Pass onto Determine_Split_Type function, that then passes it onto the appropriate Splitting funcion
            determine_split_type(image_path, output_dir, rows, columns, gap)
            # For testing purposes, prints the received textbox values and prints them.
            #placeholder_process(image_path, output_dir, rows, columns, gap)

        else:
            print("One or more required widgets are missing.")

    # Grabs all required parameters and passes it to the DisplayKeys_Previewer widget.
    # Currently, defaults are provided for any of the required inputs that are missing.
    def process_preview(widget_id):
        print("---Processing Preview---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)
        widgets = app.properties

        # Get Image Properties Type
        get_params_type_widget = next((widget for widget in widgets if widget.id == "GetParamsType"), None)

        # Get Text boxes to process image
        get_image_widget = next((widget for widget in widgets if widget.id == "GetImage"), None)
        get_rows_widget = next((widget for widget in widgets if widget.id == "GetRows"), None)
        get_columns_widget = next((widget for widget in widgets if widget.id == "GetColumns"), None)
        get_gap_widget = next((widget for widget in widgets if widget.id == "GetGap"), None)

        if all(widget is not None for widget in
               [get_image_widget, get_rows_widget, get_columns_widget, get_gap_widget, get_params_type_widget]):
            # Determine if the default or user-defined values should be used
            if get_params_type_widget.dropdown_var.get() == "Defaults":
                image_path = get_image_widget.textbox.get()
                if not image_path:
                    image_path = sys._MEIPASS + "./Preview.png"
                rows = int(get_rows_widget.textbox_default)
                columns = int(get_columns_widget.textbox_default)
                gap = int(get_gap_widget.textbox_default)

            elif get_params_type_widget.dropdown_var.get() == "User Defined":
                image_path = get_image_widget.textbox.get() if get_image_widget.textbox.get() else None
                rows = int(get_rows_widget.textbox.get()) if get_rows_widget.textbox.get().isnumeric() else None
                columns = int(get_columns_widget.textbox.get()) if get_columns_widget.textbox.get().isnumeric() else None
                gap = int(get_gap_widget.textbox.get()) if get_gap_widget.textbox.get().isnumeric() else None

                if not image_path:
                    image_path = sys._MEIPASS + "./Preview.png"
                if not rows:
                    rows = int(get_rows_widget.textbox_default)
                if not columns:
                    columns = int(get_columns_widget.textbox_default)
                if not gap:
                    gap = int(get_gap_widget.textbox_default)
            else:
                return

            # Temporarily set the text entry widget to normal state to update its value
            get_image_widget.textbox.configure(state="normal")
            get_image_widget.textbox.delete(0, tk.END)
            get_image_widget.textbox.insert(tk.END, image_path)
            get_image_widget.textbox.configure(state="readonly")

            # Update the preview
            app.preview.update(image_path, rows, columns, gap)

        else:
            print("One or more required widgets are missing.")

    # Dropdowns:
    # Hides / Unhides specific DisplayKeys_Widgets
    # TODO: Make generic so that dropdown button provides the list of WidgetID's its responsible for.
    # TODO: Will make life easier for future dropdown functions as well.
    def property_options_visibility(properties):
        widgets = properties

        properties_dropdown_widget = next((widget for widget in widgets if widget.id == "GetParamsType"), None)
        option = properties_dropdown_widget.dropdown_var.get()

        # Get the widgets to show/hide
        get_rows_widget = next((widget for widget in widgets if widget.id == "GetRows"), None)
        get_columns_widget = next((widget for widget in widgets if widget.id == "GetColumns"), None)
        get_gap_widget = next((widget for widget in widgets if widget.id == "GetGap"), None)

        # Show/hide the widgets based on the selected option
        if get_rows_widget and get_columns_widget and get_gap_widget:
            if option == "Defaults":
                for widget in (get_rows_widget, get_columns_widget, get_gap_widget):
                    if widget:
                        widget.grid_remove()
            elif option == "User Defined":
                for widget in (get_rows_widget, get_columns_widget, get_gap_widget):
                    if widget:
                        widget.grid(sticky="n")
                        
    # Popup Window Functions:
    # Placeholder for the future...


####################################################################################################################
#                                                   Split Image
####################################################################################################################


# Holds the list of currently supported Image Types,
# Might look into extending this in the future if necessary.
def get_supported_types():
    # The supported file formats:
    sup_image_formats = [".png", ".jpg", ".jpeg", ".bmp"]
    sup_animated_formats = [".gif"]
    return sup_image_formats, sup_animated_formats


# Checks the provided image and determines whether it's a static or dynamic image format.
# Also passes along rest of variables provided by ButtonFunctions.ProcessImage
def determine_split_type(file_path, output_dir, rows, cols, gap):
    print("---Determening File Type---")

    # The supported file formats:
    image_formats = get_supported_types()[0]
    animated_formats = get_supported_types()[1]

    print("File Types are: ")
    print(get_supported_types()[0])
    print(get_supported_types()[1])

    try:
        # Check if image format is supported
        with Image.open(file_path) as image:
            print("Image can be opened: " + (
                "True" if image else "False") + "\n   Image format is: " + "." + image.format.lower())
            # Is Image
            if "." + image.format.lower() in image_formats:
                split_image(file_path, output_dir, rows, cols, gap)
                return True
            # Is Animated
            elif "." + image.format.lower() in animated_formats:
                split_gif(file_path, output_dir, rows, cols, gap)
                return True
            else:
                print("No formats matched")

    # Is not of a supported image format
    except TypeError as error_message:
        # In the future simply open a Pop-Up Window with an error message:
        # |----------------------------------------|
        # | File Format not supported \n           |
        # | Currently supported formats are: \n    |
        # | - Image     | get_supported_types()[0] |
        # | - Animated  | get_supported_types()[1] |
        # |----------------------------------------|
        # Do nothing for now
        print(TypeError)
        print("Wrong File Type: ", type(error_message).__name__, str(error_message))
        return None


# Splits the provided Image into Image-Cell's based on provided parameters.
# This function crops the Image's to make them square.
def split_image(image_path, output_dir, rows, cols, gap):
    # Open the image using PIL
    image = Image.open(image_path)

    # Calculate the width and height of each image-cell
    width, height = image.size
    print("Width:", width)
    print("Height:", height)
    cell_width = (width - (cols - 1) * gap) // cols
    cell_height = (height - (rows - 1) * gap) // rows

    print("Cell Width:", cell_width)
    print("Cell Height:", cell_height)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine the maximum cell size (to maintain square shape)
    max_cell_size = min(cell_width, cell_height)
    print("Max Cell Size:", max_cell_size)

    # Calculate the horizontal and vertical offsets for cropping
    horizontal_offset = (cell_width - max_cell_size) // 2
    vertical_offset = (cell_height - max_cell_size) // 2

    print("Horizontal Offset:", horizontal_offset)
    print("Vertical Offset:", vertical_offset)

    # Determine the longest dimension (width or height)
    longest_dimension = "width" if cell_width > cell_height else "height"

    # Split the image and save each image-cell
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates for cropping
            left = col * (cell_width + gap) + horizontal_offset
            upper = row * (cell_height + gap) + vertical_offset

            # Remove rows/columns only if they are part of the Outlier image-cells
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

            # Crop all image-cells
            image_cell = image.crop((left, upper, right, lower))

            # Generate the output file path
            filename_without_extension = os.path.splitext(os.path.basename(image.filename))[0]
            output_path = os.path.join(output_dir, f"{filename_without_extension}_{row}_{col}.png")

            # Save the image-cells
            image_cell.save(output_path)

            print(f"Saved {output_path}")


# Splits the provided GIF into GIF-Cell's based on provided parameters.
# This function crops the GIF's to make them square.
# This function preserves or adds Frame Timings in case Frame's are missing this information.
# Discards 0ms Frame Times. Default Frame Timing is 100ms, if only some Frame's have timing, average will be used.
def split_gif(gif_path, output_dir, rows, cols, gap):
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
    cell_width = (width - (cols - 1) * gap) // cols
    cell_height = (height - (rows - 1) * gap) // rows

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
            left = col * (cell_width + gap) + horizontal_offset
            upper = row * (cell_height + gap) + vertical_offset

            # Remove rows/columns only if they are part of the Outlier image-cells
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
            filename_without_extension = os.path.splitext(os.path.basename(gif.filename))[0]
            output_path = os.path.join(output_dir, f"{filename_without_extension}_{row}_{col}.gif")
            print("Num of Modified Frames: " + str(modified_frames.__sizeof__()))

            # Save all frames of the image-cell into a single .gif file
            modified_frames[0].save(
                output_path,
                save_all=True,
                append_images=modified_frames[1:],
                duration=frame_durations,  # Might make this a user definable variable in the future
                loop=0
            )
            modified_frames = []
            print(f"gif_cell_{row}_{col} has this many frames: " + str(Image.open(output_path).n_frames))
            print(f"Saved {output_path}")


####################################################################################################################
#                                                    Create GUI
####################################################################################################################


if __name__ == "__main__":
    # For flow debugging
    print("---Code Start---")
    
    # Create DisplayKeys_Widget's
    ToolProperties = [
        {
            "widget_id": "Credits",
            "label_text": "Image Splitter made by Neuffexx",
        },
        {
            "widget_id": "GetImage",
            "label_text": "Choose Image:",
            "has_textbox": True,
            "textbox_state": "readonly",
            "button_label": "Browse Image",
            "button_command": ButtonFunctions.browse_image,
            "button_tooltip": "Select the Image you want to be split.",
        },
        {
            "widget_id": "GetOutput",
            "label_text": "Choose Output Location:",
            "has_textbox": True,
            "textbox_state": "readonly",
            "button_label": "Browse Folder",
            "button_command": ButtonFunctions.browse_directory,
            "button_tooltip": "Select the Folder to save the split Image to.",
        },
        {
            "widget_id": "TopDivider",
            "label_text": "-------------------------------------",
        },
        {
            "widget_id": "GetParamsType",
            "label_text": "Set Splitting Parameters:",
            "dropdown_options": ["Defaults", "User Defined"],  # "Profile"], for future implementation
            "dropdown_command": ButtonFunctions.property_options_visibility,
            "dropdown_tooltip": "Default Values are: \n Rows         | 2 \nColumns   | 6 \n Gap            | 40",
            "has_textbox": False,
        },
        {
            "widget_id": "GetRows",
            "label_text": "Rows:",
            "has_textbox": True,
            "default_value": "2",
        },
        {
            "widget_id": "GetColumns",
            "label_text": "Columns:",
            "has_textbox": True,
            "default_value": "6",
        },
        {
            "widget_id": "GetGap",
            "label_text": "Gap (in Pixels):",
            "has_textbox": True,
            "default_value": "40",
        },
        {
            "widget_id": "BottomDivider",
            "label_text": "-------------------------------------",
        },
        {
            "widget_id": "SplitImage",
            "button_label": "Split Image",
            "button_command": ButtonFunctions.process_image,
        },
    ]

    # Create/Start Application Window
    app = DisplayKeys_GUI(ToolProperties)
    app.run()
