import os
from PIL import Image, ImageSequence
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox


####################################################################################################################
#                                                    GUI Window
####################################################################################################################


class ImageSplitterGUI:
    def __init__(self, widgets):
        print("---Creating Window---")
        self.window = tk.Tk()
        self.window.title("DisplayKeys-IS")
        self.window.geometry("550x500")
        self.window.resizable(False, False)

        #########################

        print("---Creating Left Column---")
        # Create the Properties(left) column
        self.properties_frame = tk.Frame(self.window, width=200, height=500)
        self.properties_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.properties_frame.grid_columnconfigure(0, weight=1)
        # Populate the left column with widgets
        self.properties = []
        self.properties = self.populate_column(self.properties_frame, widgets)

        print("---Creating Right Column---")
        # Create the Preview(right) column
        self.preview_frame = tk.Frame(self.window, height=500)
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        # Create the Preview widget and place it in the right column
        preview = Preview(self.preview_frame)

        #########################

        # Initially Hide Options Based on Dropdown Selection
        ButtonFunctions.property_options_visibility(self.properties)

    # Used to populate a column(frame) with widgets
    def populate_column(self, parent, widgets):
        created_widgets = []
        for widget in widgets:
            created_widgets.append(ImageSetup(parent, **widget))

        return created_widgets

    # Starts the Window loop
    def run(self):
        # Start the Tkinter event loop
        self.window.mainloop()


class Preview:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=300, height=300, bg="black")
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.grid(sticky="n")

        self.update_button = ImageSetup(parent, widget_id="PreviewUpdate", button_label="Update", button_command=placeholder, button_tooltip="Update the preview.")
        self.update_button.place()
        self.update_button.grid(sticky="n")


class ImageSetup(tk.Frame):
    def __init__(self, parent, widget_id, text_label=None, dropdown_options=None, dropdown_tooltip=None, dropdown_command=None,
                 has_textbox=False, textbox_state="normal", default_value=None, button_label=None, button_command=None,
                 button_tooltip=None):
        super().__init__(parent)
        self.grid(sticky="n")

        # The reference name by which button functions will find this widget
        self.id = widget_id

        # Create the label widget
        if text_label:
            self.label = tk.Label(self, text=text_label)
            self.label.grid(sticky="n")

        # Create the dropdown selection button
        if dropdown_options and dropdown_command:
            self.dropdown_var = tk.StringVar()
            self.dropdown_var.set(dropdown_options[0])  # Set default value
            self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var, values=dropdown_options, state="readonly")
            self.dropdown.grid(sticky="n")
            # Bind the selection change event to the dropdown command
            self.dropdown.bind("<<ComboboxSelected>>", lambda event: dropdown_command(app.properties))

            if dropdown_tooltip:
                self.d_tooltip = Tooltip(self.dropdown, dropdown_tooltip)

        # Create the textbox
        if has_textbox:
            self.textbox = tk.Entry(self, state=textbox_state)
            if default_value:
                self.textbox_default = default_value

            self.textbox.grid(sticky="n")

        # Create a function button
        if button_label and button_command:
            self.button = tk.Button(self, text=button_label, command= lambda: button_command(self.id))
            self.button.grid(sticky="n")

            if button_tooltip:
                self.b_tooltip = Tooltip(self.button, button_tooltip)


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


class ButtonFunctions:
    # Buttons
    def browse_image(widget_id):
        print("---Browsing for Image---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)

        if widget:
            # Open a file dialog for selecting an image file
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
            )
            if file_path:
                widget_original_state = widget.textbox.__getitem__('state')
                print("Original Textbox State: " + widget_original_state)

                widget.textbox.configure(state='normal')
                widget.textbox.delete(0, tk.END)
                widget.textbox.insert(tk.END, file_path)
                widget.textbox.configure(state=widget_original_state)
                # Previewer Code Here...  # Pass the image path

            return file_path

    def browse_output(widget_id):
        print("---Browsing for Output Dir---")
        print("Widget ID: " + widget_id)
        widget = next((widget for widget in app.properties if widget.id == widget_id), None)

        if widget:
            # Open a file dialog for selecting an image file
            output_path = filedialog.askdirectory()
            if output_path:
                widget_original_state = widget.textbox.__getitem__('state')
                print("Original Textbox State: " + widget_original_state)

                widget.textbox.configure(state='normal')
                widget.textbox.delete(0, tk.END)
                widget.textbox.insert(tk.END, output_path)
                widget.textbox.configure(state=widget_original_state)

            return output_path

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
                output_dir = get_output_widget.textbox.get()
                rows = int(get_rows_widget.textbox_default)
                columns = int(get_columns_widget.textbox_default)
                gap = int(get_gap_widget.textbox_default)
            # Get the text from the required textboxes
            elif get_params_type_widget.dropdown_var.get() == "User Defined":
                image_path = get_image_widget.textbox.get()
                output_dir = get_output_widget.textbox.get()
                rows = int(get_rows_widget.textbox.get())
                columns = int(get_columns_widget.textbox.get())
                gap = int(get_gap_widget.textbox.get())
            else:
                return

            # Pass onto Determine_Split_Type function, that then passes it onto the appropriate Splitting funcion
            determine_split_type(image_path, output_dir, rows, columns, gap)
            # For testing purposes, prints the received textbox values and prints them.
            #placeholder_process(image_path, output_dir, rows, columns, gap)

        else:
            print("One or more required widgets are missing.")

    # Dropdowns

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


####################################################################################################################
#                                                   Split Image
####################################################################################################################


# Image Splitter functionality...
def get_supported_types():
    # The supported file formats:
    sup_image_formats = [".png", ".jpg", ".jpeg", ".bmp"]
    sup_animated_formats = [".gif"]
    return sup_image_formats, sup_animated_formats


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
            filename_without_extension = os.path.splitext(os.path.basename(image.filename))[0]
            output_path = os.path.join(output_dir, f"{filename_without_extension}_{row}_{col}.png")

            # Save the image-cell
            image_cell.save(output_path)

            print(f"Saved {output_path}")


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


def placeholder():
    return

def placeholder_process(image_path, output_dir, rows, columns, gap):
    print("ImagePath: " + image_path)
    print("OutputPath: " + output_dir)
    print("Rows: " + rows)
    print("Columns: " + columns)
    print("Gap: " + gap)
    return


if __name__ == "__main__":
    print("---Code Start---")
    # Create Widgets
    ToolProperties = [
        {
            "widget_id": "Credits",
            "text_label": "Image Splitter made by Neuffexx",
        },
        {
            "widget_id": "GetImage",
            "text_label": "Choose Image:",
            "has_textbox": True,
            "textbox_state": "readonly",
            "button_label": "Browse Image",
            "button_command": ButtonFunctions.browse_image,
            "button_tooltip": "Select the Image you want to be split.",
        },
        {
            "widget_id": "GetOutput",
            "text_label": "Choose Output Location:",
            "has_textbox": True,
            "textbox_state": "readonly",
            "button_label": "Browse Folder",
            "button_command": ButtonFunctions.browse_output,
            "button_tooltip": "Select the Folder to save the split Image to.",
        },
        {
            "widget_id": "TopDivider",
            "text_label": "-------------------------------------",
        },
        {
            "widget_id": "GetParamsType",
            "text_label": "Set Splitting Parameters:",
            "dropdown_options": ["Defaults", "User Defined"],  # "Profile"], for future implementation
            "dropdown_command": ButtonFunctions.property_options_visibility,
            "has_textbox": False,
        },
        {
            "widget_id": "GetRows",
            "text_label": "Rows:",
            "has_textbox": True,
            "default_value": "2",
        },
        {
            "widget_id": "GetColumns",
            "text_label": "Columns:",
            "has_textbox": True,
            "default_value": "6",
        },
        {
            "widget_id": "GetGap",
            "text_label": "Gap (in Pixels):",
            "has_textbox": True,
            "default_value": "40",
        },
        {
            "widget_id": "BottomDivider",
            "text_label": "-------------------------------------",
        },
        {
            "widget_id": "SplitImage",
            "button_label": "Split Image",
            "button_command": ButtonFunctions.process_image,
        },
    ]


    # Create Application
    app = ImageSplitterGUI(ToolProperties)
    app.run()
