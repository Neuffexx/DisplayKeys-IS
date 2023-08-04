# Image Splitter made by Neuffexx
# This image splitter was made to allow people to take images they want displayed across their Mountain DisplayPad keys.
# Who asked for this? Me. I did. Because it's a workaround to a problem that shouldn't exist in the first place.
# And I was too lazy to do this to each image manually.
# Was this more effort? Yes. You are welcome.

from typing import Literal, Callable, Annotated
import os
import sys
from PIL import Image, ImageTk, ImageSequence, ImageDraw
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinterdnd2 as tkdnd
from tkinterdnd2 import *

####################################################################################################################
#                                                    GUI Window
####################################################################################################################


# The Main Application Window
class DisplayKeys_GUI:
    """
        The Main Class of the Application.
        It Creates the Window and all of its UI Elements within it when Initialized.
    """
    def __init__(self):
        print("---Creating Window---")
        self.window = tkdnd.Tk()
        self.window.title("DisplayKeys-IS")
        icon_path = "./DisplayKeys-IS.ico" #Sys._MEIPASS + "./DisplayKeys-IS.ico"
        self.window.iconbitmap(icon_path)
        self.window.geometry("600x600")
        self.window.resizable(False, False)

        #########################

        print("---Creating Left Column---")
        # Create the Properties Frame
        self.properties_frame = tk.Frame(self.window, width=200, height=500, background="#343A40")
        self.properties_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.properties_frame.grid_columnconfigure(0, weight=1)
        # Populate the properties frame with widgets
        self.properties = []
        self.properties = self.populate_column(self.properties_frame, self.get_properties_widgets())
        #(next(widget for widget in self.properties if widget.id == "GetOutput").textbox, 'image').enable_dnd()

        print("---Creating Right Column---")
        # Create the Preview Frame
        self.preview_frame = tk.Frame(self.window, height=500, background="#212529")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        # Create the Preview Widget and place it in the right column
        self.preview = DisplayKeys_Previewer(self.preview_frame, width=350, height=350)
        self.preview_reset = tk.Button(self.preview_frame, text="Reset", background="#E9ECEF", command=lambda: DisplayKeys_Previewer.reset_drag(self.preview), width=10)
        self.preview_reset.grid(sticky="n", row=1)
        self.previewer_reset_tooltip = DisplayKeys_Tooltip(self.preview_reset, "Reset the Preview Image to its original position.")
        # Create the Preview Statistics and place them in the right column
        self.previewer_help = DisplayKeys_Help(parent=self.preview_frame, row=1, alignment="nes", percentage_size=40,
                                               help_tooltip="Previewer is not 100% Accurate!\n\nPreviewer Legend:\n  - Red Lines: Image Split\n  - Red Line Thickness: Gap\n  - Black Stipped: Cell Cropping",
                                               tooltip_justification="left", tooltip_anchor="center")
        # TODO: Add Results Widget's and populate content (ie. cell resolution, % of lost pixels?, etc.)
        #       Also check if there is any actual meaningful information that can be added.
        #self.preview_info = self.populate_column(self.preview_frame, self.get_preview_widgets())
        #self.previewer_info_help = DisplayKeys_Help(parent=self.preview_frame, row=10, alignment="se", percentage_size=40,
        #                                       help_tooltip="Further Information on the Results!")

        #########################

        # Initially Hide Options Based on Dropdown Selection
        ButtonFunctions.property_options_visibility(self.properties)

        # Set focus to Application Window, to stop it being hidden behind others on launch
        self.window.focus_force()

    # Used to populate a column(Frame) with DisplayKeys_Composite_Widget's
    @staticmethod
    def populate_column(parent, widgets):
        created_widgets = []
        for widget in widgets:
            created_widgets.append(DisplayKeys_Composite_Widget(parent, **widget))

        return created_widgets

    @staticmethod
    def get_properties_widgets():
        ToolProperties = [
            {
                "widget_id": "Credits",
                "label_text": "Image Splitter made by Neuffexx",
                "label_colour": "#E9ECEF",
            },
            {
                "widget_id": "GetImage",
                "label_text": "Choose Image:",
                "label_colour": "#E9ECEF",
                "has_textbox": True,
                "textbox_state": "readonly",
                "textbox_colour": "#ADB5BD",
                "has_textbox_dnd": True,
                "dnd_type": 'image',
                "button_label": "Browse Image",
                "button_command": ButtonFunctions.browse_image,
                "button_tooltip": "Select the Image you want to be split.",
                "updates_previewer": True,
            },
            {
                "widget_id": "GetOutput",
                "label_text": "Choose Output Location:",
                "label_colour": "#E9ECEF",
                "has_textbox": True,
                "textbox_state": "readonly",
                "textbox_colour": "#ADB5BD",
                "has_textbox_dnd": True,
                "dnd_type": 'folder',
                "button_label": "Browse Folder",
                "button_command": ButtonFunctions.browse_directory,
                "button_tooltip": "Select the Folder to save the split Image to.",
            },
            {
                "widget_id": "TopDivider",
                "label_text": "-------------------------------------",
                "label_colour": "#343A40",
            },
            {
                "widget_id": "GetParamsType",
                "label_text": "Set Splitting Parameters:",
                "label_colour": "#E9ECEF",
                "dropdown_options": ["Defaults", "User Defined"],  # "Profile"], for future implementation
                "dropdown_command": ButtonFunctions.property_options_visibility,
                "dropdown_tooltip": "Default Values are: \n Rows         | 2 \nColumns   | 6 \n Gap            | 40",
                "has_textbox": False,
            },
            {
                "widget_id": "GetRows",
                "label_text": "Rows:",
                "label_colour": "#E9ECEF",
                "has_spinbox": True,
                "spinbox_colour": "#CED4DA",
                "spinbox_default_value": "2",
                "has_spinbox_dnd": True,
                "dnd_type": "text",
                "updates_previewer": True,
            },
            {
                "widget_id": "GetColumns",
                "label_text": "Columns:",
                "label_colour": "#E9ECEF",
                "has_spinbox": True,
                "spinbox_colour": "#CED4DA",
                "spinbox_default_value": "6",
                "has_spinbox_dnd": True,
                "dnd_type": "text",
                "updates_previewer": True,
            },
            {
                "widget_id": "GetGap",
                "label_text": "Gap (in Pixels):",
                "label_colour": "#E9ECEF",
                "has_spinbox": True,
                "spinbox_colour": "#CED4DA",
                "spinbox_default_value": "40",
                "has_spinbox_dnd": True,
                "dnd_type": "text",
                "updates_previewer": True,
            },
            {
                "widget_id": "BottomDivider",
                "label_text": "-------------------------------------",
                "label_colour": "#343A40",
            },
            {
                "widget_id": "SplitImage",
                "button_label": "Split Image",
                "label_colour": "#E9ECEF",
                "button_command": ButtonFunctions.process_image,
            },
        ]

        return ToolProperties

    @staticmethod
    def get_preview_widgets():
        PreviewWidgets = [
            {
                "widget_id": "PreviewDivider",
                "label_text": "",
                "label_colour": "#E9ECEF",
             },
            {
                "widget_id": "OutputDetails",
                "label_text": "Results :",
                "label_colour": "#E9ECEF",
            },
            {
                "widget_id": "",
                "label_text": "",
                "label_colour": "#E9ECEF",
            },
            {
                "widget_id": "",
                "label_text": "",
                "label_colour": "#E9ECEF",
            },
        ]

        return PreviewWidgets

    # Starts the Window loop
    def run(self):
        self.window.mainloop()


# The Widget that show's all changes done to the Image within the Application
class DisplayKeys_Previewer:
    """
        The Widget that show's all changes done to the Image within the Application.
        :param parent: The Widget Container holding this Previewer.
        :param width: The Width of the Previewer Canvas.
        :param height: The Height of the Previewer Canvas.
    """
    def __init__(self, parent, width, height):
        # Initialize Image
        self.width = width
        self.height = height
        self.placeholder_path = "./Preview.png" #Sys._MEIPASS + "./Preview.png"
        self.image_path = None

        # Initialize canvas
        self.canvas = tk.Canvas(parent, width=self.width, height=self.height, background="#151515", highlightthickness=3, highlightbackground="#343A40")
        self.canvas.grid()
        self.canvas.tag_bind("preview_image", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("preview_image", "<ButtonRelease-1>", self.end_drag)
        self.canvas.tag_bind("preview_image", "<B1-Motion>", self.do_drag)

        # Initialize Click-Drag / Offset Functionality
        self.drag_data = {"item": None, "x": 0.0, "y": 0.0}
        self.image_reset_position = {"x": 0.0, "y": 0.0}
        self.image_current_position = {"x": 0.0, "y": 0.0}
        self.allowed_drag_distance_cell = 0
        self.allowed_drag_distance_cropping = {"x": 0.0, "y": 0.0}
        self.drag_limit_type = False
        self.scale_factor = 1
        self.final_offset = {"x": 0.0, "y": 0.0}

        # Load and show the initial placeholder image
        self.display_preview_image(self.placeholder_path)

    def display_preview_image(self, image_path):
        """
        Simply gets the image, rescales it and renders it onto the canvas.
        :param image_path: The on Disk path to the Image to be Previewed
        """
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
        self.preview_image = self.canvas.create_image(x_offset if self.image_path != image_path else self.image_current_position["x"], y_offset if self.image_path != image_path else self.image_current_position["y"], image=self.tk_image, anchor=tk.NW, tags="preview_image")

        # Store initial position of Image for reset
        # (only if it's a new image)
        if self.image_path != image_path:
            self.image_reset_position["x"], self.image_reset_position["y"] = self.canvas.coords(self.preview_image)
            self.image_path = image_path
        # And make it the current position
        self.image_current_position["x"], self.image_current_position["y"] = self.canvas.coords(self.preview_image)

        # For Grid/Cropping Preview
        self.resized_image = resized_image
        self.x_offset = x_offset
        self.y_offset = y_offset

        # For click-drag offset input
        self.drag_data["x"] = x_offset
        self.drag_data["y"] = y_offset

    # This calculates an approximate version of the split_image function,
    # to preview the Splitting and Cropping of an image provided.
    # Also calls the 'display_preview_image' to refresh the image.
    # TODO:
    #     - Update function to use newly added 'Offset' inputs
    def update_preview(self, image_path, num_rows, num_columns, gap):
        # Clear the canvas to prepare for new content
        self.canvas.delete("all")

        # Display the image after rescaling
        self.display_preview_image(image_path)

        # Calculate the dimensions of each image cell
        image_width, image_height = self.resized_image.size
        cell_width = image_width / num_columns
        cell_height = image_height / num_rows
        scaled_gap = gap * self.scale_factor

        # Define the size of the square to be cropped from each cell
        square_size = min(cell_width, cell_height) - scaled_gap
        # For Cell Clamping
        self.allowed_drag_distance_cell = square_size
        # For Cropping Clamping
        self.allowed_drag_distance_cropping["x"] = abs((cell_width - square_size)) / (self.scale_factor)
        self.allowed_drag_distance_cropping["y"] = abs((cell_height - square_size)) / (self.scale_factor)

        # Draw Cropping Stipple's
        for column_index in range(num_columns):
            for row_index in range(num_rows):

                # Initial position for cropping rectangle (centered in cell)
                crop_left = column_index * cell_width + (cell_width - square_size) / 2 + self.x_offset
                crop_top = row_index * cell_height + (cell_height - square_size) / 2 + self.y_offset
                crop_right = crop_left + square_size
                crop_bottom = crop_top + square_size

                # Position adjustments for Outlier Image-Cells
                if row_index == 0:  # First Row
                    crop_bottom = (row_index + 1) * cell_height - scaled_gap / 2 + self.y_offset
                    crop_top = crop_bottom - square_size
                elif row_index == num_rows - 1:  # Last Row
                    crop_top = row_index * cell_height + scaled_gap / 2 + self.y_offset
                    crop_bottom = crop_top + square_size

                if column_index == 0:  # First Column
                    crop_right = (column_index + 1) * cell_width - scaled_gap / 2 + self.x_offset
                    crop_left = crop_right - square_size
                elif column_index == num_columns - 1:  # Last Column
                    crop_left = column_index * cell_width + scaled_gap / 2 + self.x_offset
                    crop_right = crop_left + square_size

                # Draw the adjusted Cropping Overlay
                self.canvas.create_rectangle(crop_left, crop_top, crop_right, crop_bottom, outline="blue")

                # Draw Cropping Overlays with stipple effect, adjusted for Outlier Image-Cells
                stipple_pattern = "gray25"
                overlay_left = self.x_offset if column_index == 0 else column_index * cell_width + self.x_offset
                overlay_right = self.x_offset + image_width if column_index == num_columns - 1 else (
                                                                                                            column_index + 1) * cell_width + self.x_offset
                overlay_top = self.y_offset if row_index == 0 else row_index * cell_height + self.y_offset
                overlay_bottom = self.y_offset + image_height if row_index == num_rows - 1 else (
                                                                                                            row_index + 1) * cell_height + self.y_offset

                self.canvas.create_rectangle(overlay_left, crop_top, crop_right, overlay_top, fill="gray",
                                             stipple=stipple_pattern)
                self.canvas.create_rectangle(overlay_left, crop_bottom, crop_right, overlay_bottom, fill="gray",
                                             stipple=stipple_pattern)
                self.canvas.create_rectangle(crop_left, overlay_top, overlay_left, overlay_bottom, fill="gray",
                                             stipple=stipple_pattern)
                self.canvas.create_rectangle(crop_right, overlay_top, overlay_right, overlay_bottom, fill="gray",
                                             stipple=stipple_pattern)

        # Draw the Grid Lines
        for column_index in range(1, num_columns):
            grid_x = column_index * cell_width + self.x_offset
            self.canvas.create_line(grid_x, self.y_offset, grid_x, image_height + self.y_offset, fill="#CC0000",
                                    width=scaled_gap)

        for row_index in range(1, num_rows):
            grid_y = row_index * cell_height + self.y_offset
            self.canvas.create_line(self.x_offset, grid_y, image_width + self.x_offset, grid_y, fill="#CC0000",
                                    width=scaled_gap)

        # Draw Blackout Lines
        blackout_rectangles = [
            self.canvas.create_rectangle(0, 0, self.width + 15, self.y_offset, fill='black'), # Top
            self.canvas.create_rectangle(0, self.y_offset + self.resized_image.height, self.width + 15, self.height + 15,
                                         fill='black'), # Bottom
            self.canvas.create_rectangle(0, self.y_offset, self.x_offset, self.y_offset + self.resized_image.height,
                                         fill='black'), # Left
            self.canvas.create_rectangle(self.x_offset + self.resized_image.width, self.y_offset, self.width + 15,
                                         self.y_offset + self.resized_image.height, fill='black'), # Right
        ]

    # noinspection PyTypedDict
    def start_drag(self, event):
        # record the item and its location
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        #print("Start Drag Position:", event.x, event.y)

    def end_drag(self, event):
        # Save the end position of the drag
        self.image_current_position["x"], self.image_current_position["y"] = self.canvas.coords(self.preview_image)

        # Calculate the distance moved on Canvas
        canvas_delta_x = self.image_current_position["x"] - self.image_reset_position["x"]
        canvas_delta_y = self.image_current_position["y"] - self.image_reset_position["y"]
        # Convert to In-Canvas Image Space
        delta_x = canvas_delta_x / self.scale_factor
        delta_y = canvas_delta_y / self.scale_factor

        # Clamp the distance moved in Canvas Space
        if self.drag_limit_type:
            # Clamp the distance moved based on Cell Size
            if delta_x > 0:
                delta_x = min(delta_x, self.allowed_drag_distance_cell)
            else:
                delta_x = max(delta_x, -self.allowed_drag_distance_cell)

            if delta_y > 0:
                delta_y = min(delta_y, self.allowed_drag_distance_cell)
            else:
                delta_y = max(delta_y, -self.allowed_drag_distance_cell)
        else:
            # Clamp the distance moved based on Cropping Size
            if delta_x > 0:
                delta_x = min(delta_x, self.allowed_drag_distance_cropping["x"])
            else:
                delta_x = max(delta_x, -self.allowed_drag_distance_cropping["x"])

            if delta_y > 0:
                delta_y = min(delta_y, self.allowed_drag_distance_cropping["y"])
            else:
                delta_y = max(delta_y, -self.allowed_drag_distance_cropping["y"])


        # Update the position in Canvas Space, given the new delta_x and delta_y
        self.image_current_position["x"] = self.image_reset_position["x"] + delta_x * self.scale_factor
        self.image_current_position["y"] = self.image_reset_position["y"] + delta_y * self.scale_factor

        # move the image back to the new clamped position
        self.canvas.coords(self.preview_image, self.image_current_position["x"], self.image_current_position["y"])

        # Get / Store Offset in Original-Image Space
        delta_x = (self.image_current_position["x"] - self.image_reset_position["x"]) / self.scale_factor
        delta_y = (self.image_current_position["y"] - self.image_reset_position["y"]) / self.scale_factor
        self.final_offset = {"x": delta_x, "y": delta_y}
        print("Final Offset:", delta_x, delta_y)

        # reset the drag information
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

        # Update the Previewer - In the future it will show what cells will be discarded
        ButtonFunctions.process_image("DragPreviewImage")

    def do_drag(self, event):
        # compute how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        #print("New Drag Position:", delta_x, delta_y)

    # Move the preview image back to its original position
    def reset_drag(self):
        # Reset Position / Save
        self.canvas.coords(self.preview_image, self.image_reset_position["x"], self.image_reset_position["y"])
        self.image_current_position["x"], self.image_current_position["y"] = self.canvas.coords(self.preview_image)
        delta_x = self.image_current_position["x"] - self.image_reset_position["x"]
        delta_y = self.image_current_position["y"] - self.image_reset_position["y"]
        self.final_offset = {"x": delta_x, "y": delta_y}
        print("Reset Offset:", delta_x, delta_y)

        # Update the Previewer - In the future it will show what cells will be discarded
        ButtonFunctions.process_image("ResetPreviewer")


# Generic Widgets used throughout the Applications UI (ie. Labels, Textboxes, Buttons, etc.)
class DisplayKeys_Composite_Widget(tk.Frame):
    """
        Generic Widgets used throughout the Applications UI (ie. Labels, Textboxes, Buttons, etc.)

        Optional Named Widget Params: All parameters not listed here are Optional and too many to list.
        :param parent: The Widget container
        :param widget_id: A Unique ID to Identify/Distinguish it from other Composite Widgets.
    """
    def __init__(self, parent: tk.Frame, widget_id: str, label_text: str = None, label_tooltip: str = None,
                 dropdown_options: list[str] = None, dropdown_tooltip: str = None,
                 dropdown_command: Callable[[list['DisplayKeys_Composite_Widget']], None] = None,
                 has_textbox: bool = False, textbox_state: Literal["normal", "disabled", "readonly"] = "normal",
                 textbox_default_value: str = None, has_spinbox: bool = False, spinbox_default_value: int | str = 0,
                 button_label: str = None, button_command: Callable[[str], None] = None, button_tooltip: str = None,
                 updates_previewer: bool = False, label_colour: str = "white",
                 textbox_colour: str = "white", spinbox_colour: str = "white",
                 has_textbox_dnd: bool = False, has_spinbox_dnd: bool = False,
                 dnd_type: Literal['image', 'folder'] = 'image'):
        super().__init__(parent, bg="#343A40")
        self.grid(sticky="nsew", padx=5, pady=5)
        self.columnconfigure(0, weight=1)

        # The reference name by which button functions will find this widget
        self.id = widget_id

        # Text Label - Text that is non-interactive (ie. A Tittle)
        # Takes: Label Text, Label Tooltip
        if label_text:
            self.label = tk.Label(self, text=label_text, background=label_colour)
            self.label.grid(sticky="nsew", column=0)

            if label_tooltip:
                self.l_tooltip = DisplayKeys_Tooltip(self.label, label_tooltip)

        # Dropdown Button - This is set up to be used with anything
        # All it needs is options and what command that will use the widgets to perform operations on.
        # Takes: Options Text Array, Command, Tooltip Text
        if dropdown_options and dropdown_command:
            self.dropdown_var = tk.StringVar()
            self.dropdown_var.set(dropdown_options[0])  # Set default value
            self.dropdown = ttk.Combobox(self, textvariable=self.dropdown_var, values=dropdown_options,
                                         state="readonly", justify="left")
            self.dropdown.grid(sticky="nsew", column=0)
            # Bind the selection change event to the dropdown command
            self.dropdown.bind("<<ComboboxSelected>>", lambda event: dropdown_command(app.properties))

            if dropdown_tooltip:
                self.d_tooltip = DisplayKeys_Tooltip(self.dropdown, dropdown_tooltip)

            # TODO: Make dropdown update previewer when changing selections.
            #       Simply make dropdown selections change the values in the textboxes that will be taken anyways.
            #       Instead of manually checking for the dropdown selection in the Process_Image Function.
            #       You just take whatever is in the textboxes at all times, and have all dropdown selections only,
            #       update the textboxes based on 'saved' values from them (this will tie in nicely with presets)!

        # Textbox - Mainly used for getting user input, but can also be used as a good place to dynamically show text
        # Takes: Default Text Value, Tooltip Text, State
        if has_textbox:
            self.textbox_var = tk.StringVar()
            self.textbox = tk.Entry(self, textvariable=self.textbox_var, state=textbox_state, background=textbox_colour,readonlybackground=textbox_colour, disabledbackground=textbox_colour, insertbackground=textbox_colour, selectbackground=textbox_colour)
            if textbox_default_value:
                self.textbox_var.set(textbox_default_value)
                self.textbox.insert(tk.END, textbox_default_value)
            # Binds the Textbox to Call the DisplayKeys_Previewer Update function when any of the Image Splitting Properties are changed
            if updates_previewer:
                self.textbox_trace = self.textbox_var.trace('w', lambda *args: ButtonFunctions.process_image(self.id))
            if (has_textbox_dnd and not has_spinbox_dnd) and dnd_type:
                self.dnd = DisplayKeys_DragDrop(self.textbox, drop_type=dnd_type, parent_widget=self, traced_callback=lambda *args: ButtonFunctions.process_image(self.id) if updates_previewer else None)

            self.textbox.grid(sticky="nsew", column=0)

        # Spinbox - Only added for the functionality of incremental user input buttons
        # spinbox_default_value + 1, to avoid 'from=0, to=0' cases
        # Takes: Default Spinbox Value, Tooltip Text
        if has_spinbox:
            self.spinbox_var = tk.IntVar()
            self.spinbox = tk.Spinbox(self, from_=0, to=(int(spinbox_default_value) + 1) * 100, textvariable=self.spinbox_var, background=spinbox_colour, readonlybackground=spinbox_colour, disabledbackground=spinbox_colour, insertbackground=spinbox_colour, selectbackground=spinbox_colour)
            self.spinbox_default = spinbox_default_value
            if spinbox_default_value:
                self.spinbox_var.set(spinbox_default_value)
                self.spinbox.delete(0, tk.END)
                self.spinbox.insert(tk.END, spinbox_default_value)
            # Binds the Spinbox to Call the DisplayKeys_Previewer Update function when any of the Image Splitting Properties are changed
            if updates_previewer:
                self.spinbox_trace = self.spinbox_var.trace('w', lambda *args: ButtonFunctions.process_image(self.id))
            if (has_spinbox_dnd and not has_textbox_dnd) and dnd_type:
                self.dnd = DisplayKeys_DragDrop(self.spinbox, drop_type=dnd_type, parent_widget=self,
                                                traced_callback=lambda *args: ButtonFunctions.process_image(
                                                    self.id) if updates_previewer else None)
                self.dnd.enable_dnd()

            self.spinbox.grid(sticky="nsew", column=0)

        # Button - Used specifically to call any function in the Application
        # Provides the function with its own ID in case the function needs to access its parents.
        # Takes: Label Text, Command, Tooltip Text
        if button_label and button_command:
            self.button = tk.Button(self, text=button_label, background=label_colour, command=lambda: button_command(self.id))
            self.button.grid(sticky="nsew", column=0, pady=3)

            if button_tooltip:
                self.b_tooltip = DisplayKeys_Tooltip(self.button, button_tooltip)


# A Tooltip that can be assigned to any of the DisplayKeys_Composite_Widget sub widgets
class DisplayKeys_Tooltip:
    """
        A Tooltip that can be assigned to any of the DisplayKeys_Composite_Widget sub widgets
        :param parent: Widget that the Tooltip is Bound to.
        :param text: The Tooltip text to show.
        :param justify: The Relative Alignment of Text to itself when broken into a new line.
        :param anchor: The Alignment of Text in general Relative to the Tooltips Widget Space
    """
    def __init__(self, parent: tk.Label | tk.Entry | tk.Spinbox | tk.Button | ttk.Combobox, text: str,
                 justify: Literal["left", "center", "right"] = "center",
                 anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "center"):
        self.parent = parent
        self.text = text
        self.tooltip = None
        self.text_justification = justify
        self.text_anchor = anchor
        self.parent.bind("<Enter>", self.show_tooltip)
        self.parent.bind("<Leave>", self.hide_tooltip)
        self.parent.bind("<Motion>", self.move_tooltip)

    # Creates the Tooltip whenever the Cursor hovers over its Parent Widget
    def show_tooltip(self, event):
        self.tooltip = tk.Toplevel(self.parent)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip_position(event)
        label = tk.Label(
            self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
            justify=self.text_justification, anchor=self.text_anchor
        )
        label.grid(sticky="n")

    # Updates the Tooltips position based on mouse movement
    def move_tooltip(self, event):
        if self.tooltip:
            self.tooltip_position(event)

    # Positions the Tooltip to the Bottom Right of the Cursor
    def tooltip_position(self, event):
        x = self.parent.winfo_pointerx()
        y = self.parent.winfo_pointery()
        self.tooltip.wm_geometry(f"+{x+20}+{y+20}")

    # Destroys the Tooltip whenever the Cursor leaves the region of the Parent Widget
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


#
# noinspection PyUnresolvedReferences
class DisplayKeys_DragDrop:
    """
    Class that adds drag-and-drop functionality to a Tkinter widget.
    Any Data received will be passed along to the Widget to handle the input.
    This simply ensures that you get the expected data.
    :param widget: The Widget to which to attach the Drag n Drop functionality.
    :param drop_type: Specifies the type of Data that is expected to be received and handled by this widget.
    """
    def __init__(self, widget: tk.Entry | tk.Spinbox, parent_widget, drop_type: Literal["image", "folder", "text", "any"], traced_callback=None):
        self.widget = widget
        self.parent_widget = parent_widget
        self.trace_callback = traced_callback
        self.type_legend = {"image": DND_FILES, "folder": DND_FILES, "text": DND_TEXT, "any": DND_ALL}
        self.type = drop_type
        self.accept_type = self.type_legend[drop_type] if drop_type in self.type_legend else print("Incorrect drag type for:", widget)
        self.enable_dnd()

    def enable_dnd(self):
        # Register widget with drag and drop functionality.
        self.widget.drop_target_register(self.accept_type)
        self.widget.dnd_bind('<<Drop>>', self.drop)
        self.widget.dnd_bind('<<DragEnter>>', self.drag_enter)  # Doesnt trigger
        self.widget.dnd_bind('<<DragLeave>>', self.drag_leave)  # Doesnt trigger
        self.widget.dnd_bind('<<Drag>>', self.drag)  # Doesnt trigger

    def disable_dnd(self):
        self.widget.dnd_bind('<<Drop>>', None)
        self.widget.dnd_bind('<<DragEnter>>', None)
        self.widget.dnd_bind('<<DragLeave>>', None)
        self.widget.dnd_bind('<<Drag>>', None)

    @staticmethod
    def drag(event):
        # For testing
        print('Dragging over widget: %s' % event.widget)
        return event.action

    def drag_enter(self, event):
        self.original_bg = self.widget.cget("background")
        self.widget.configure(background="green")
        print('Entering widget: %s' % event.widget)
        return event.action

    def drag_leave(self, event):
        self.widget.configure(background=self.original_bg)
        print('Leaving widget: %s' % event.widget)
        return event.action

    def drop(self, event):
        print("---Dropping File---")
        if event.data:
            # Check if a variable is attached to the widget
            widget_var = None
            trace_id = None
            if isinstance(self.widget, tk.Entry) and hasattr(self.parent_widget, 'textbox_var'):
                widget_var = self.parent_widget.textbox_var
                if hasattr(self.parent_widget, 'textbox_trace'):
                    trace_id = self.parent_widget.textbox_trace
            elif isinstance(self.widget, tk.Spinbox) and hasattr(self.parent_widget, 'spinbox_var'):
                widget_var = self.parent_widget.spinbox_var
                if hasattr(self.parent_widget, 'spinbox_trace'):
                    trace_id = self.parent_widget.spinbox_trace

            if widget_var is not None and trace_id is not None:
                # Disable trace if one exists
                ButtonFunctions.disable_trace(widget_var, trace_id)

            # Store original widget state
            widget_original_state = self.widget.__getitem__('state')
            print("Original widget State: " + widget_original_state)

            # Set widget to editable
            self.widget.configure(state='normal')
            self.widget.delete(0, tk.END)

            # Re-Enable Trace if one existed
            if widget_var is not None and trace_id is not None:
                # Enable trace back again
                ButtonFunctions.enable_trace(widget_var, self.parent_widget, self.trace_callback)

            if self.accept_type == (self.type_legend["image"] or self.type_legend["folder"]):
                # Remove brackets
                data_path = event.data[1:-1]
                print("The data path:", data_path)

                if self.type == "image":
                    # Attempt to open image file, to ensure it is an image
                    try:
                        Image.open(data_path)
                        # Save path to widget
                        self.widget.insert(tk.END, data_path)
                    except IOError:
                        print("Not an Image DnD!")

                elif self.type == "folder":
                    # Ensure that dropped item is a folder
                    if os.path.isdir(data_path):
                        self.widget.insert(tk.END, data_path)
                    else:
                        print("Not a Folder DnD!")

            elif self.accept_type == self.type_legend["text"]:
                # Ensure that dropped item is text
                try:
                    event.data.encode('utf-8')
                    self.widget.insert(tk.END, event.data)
                except UnicodeDecodeError:
                    print("Not a Text DnD!")

            elif self.accept_type == self.type_legend["any"]:
                self.widget.insert(tk.END, event.data)

            # Set widget back to its original state
            self.widget.configure(state=widget_original_state)

        else:
            print("COULDN'T GET DROP DATA!")
        return event.action


# A Label holding an Image with a Tooltip attached to it, used to simply provide helpful information
class DisplayKeys_Help:
    """
        A Label with a Question Mark Image and a Tooltip used for General Hints/Support
        :param parent: The Widget that it will be contained in (usually a frame).
        :param row: Used to determine its Horizontal Position inside its parent Frame.
        :param col: Used to determine its Vertical Position inside its parent Frame.
        :param alignment: Determines the Positional Alignment in its row | col.
        :param percentage_size: Scales the size of the Image.
        :param help_tooltip: The tooltip text to display.
        :param tooltip_justification: See DisplayKeys_Tooltip for clarification.
        :param tooltip_anchor: See DisplayKeys_Tooltip for clarification.
    """
    def __init__(self, parent: tk.Frame, row: int = 0, col: int = 0, alignment: str = "nsew",
                 percentage_size: int = 100, help_tooltip: str = "Placeholder Help",
                 tooltip_justification: Literal["left", "center", "right"] = "center",
                 tooltip_anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "center"):
        self.image = Image.open("./Help.png")#Sys._MEIPASS + "./Help.png")
        new_size = int( self.image.height * (percentage_size / 100) )
        self.resized_image = ImageTk.PhotoImage( self.image.resize((new_size, new_size)) )

        self.label = tk.Label(master=parent, image=self.resized_image, background=parent.cget("bg"))
        self.label.grid(sticky=alignment, column=col, row=row)

        self.h_tooltip = DisplayKeys_Tooltip(self.label, help_tooltip, justify=tooltip_justification, anchor=tooltip_anchor)


# A collection of button functions to be used throughout the UI
class ButtonFunctions:
    # --- Debug: ---
    # For testing new UI without wanting any actual actions taken.
    @staticmethod
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

    # --- Workarounds: ---
    # For temporary in code workaround solutions
    @staticmethod
    def disable_binding(widget, event_name, function_name):
        widget.unbind(event_name, function_name)

    @staticmethod
    def enable_binding(widget, event_name, function_name):
        widget.bind(event_name, function_name)

    @staticmethod
    def disable_trace(traced_variable: vars, trace_id: vars, event: str = "w"):
        """

            :param traced_variable: The Widget's Variable which holds the Trace to be destroyed.
            :param trace_id: The variable holding the stored Trace.
            :param event: The Type of Event to trigger the Trace.
        """
        # Ensure widget has a trace
        if ButtonFunctions.has_trace(traced_variable):
            traced_variable.trace_vdelete(event, trace_id)
            print("Deleted Trace:", trace_id)

    # Trace_variable_name (string) should be provided based on type of widget
    # (i.e. if textbox: textbox_trace, if spinbox: spinbox_trace, etc.)
    @staticmethod
    def enable_trace(variable_to_trace: vars, widget: DisplayKeys_Composite_Widget, function, event: str = "w"):
        """
        Will create a new Trace on a widget, that will fire a callback function whenever it is triggered.
        :param variable_to_trace: The Widget's Variable to enable the trace on.
        :param widget: The Parent widget to store the newly created Trace.
        :param function: The Function to Call when the Trace is triggered.
        :param event: The Event that will trigger this Trace.
        """
        # Create trace
        trace = variable_to_trace.trace(event, lambda *args: function(widget.id))
        widget.textbox_trace = trace
        print("Re-attached Trace:", type(widget.textbox_trace), widget.textbox_trace)
        return trace

    @staticmethod
    def has_trace(item: vars) -> bool:
        if item.trace_info():
            return True

        return False

    # --- Main Window Functions: ---
    # Buttons

    # Grabs the Path to an Image, and if possible adds this into a widgets textbox
    @staticmethod
    def browse_image(widget_id: str) -> str:
        """
            Grabs the Path to an Image, and if possible adds this into a widgets textbox
            :param widget_id: The Unique ID of the Widget that Called this function
            :return: The Path on Disk to the Image
        """
        print("---Browsing for Image---")
        print("Widget ID: " + widget_id)
        widget: DisplayKeys_Composite_Widget = next((widget for widget in app.properties if widget.id == widget_id), None)

        if widget:
            # Ask the user to select an Image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
            )
            # Put File Path into textbox if widget has a textbox
            if file_path and widget.textbox:
                widget_original_state = widget.textbox.__getitem__('state')
                print("Original Textbox State: " + widget_original_state)

                # Temporarily disable the trace (avoid calling process image with 'None' path)
                ButtonFunctions.disable_trace(widget.textbox_var, widget.textbox_trace)

                widget.textbox.configure(state='normal')
                widget.textbox.delete(0, tk.END)

                # Re-Enable the trace
                ButtonFunctions.enable_trace(widget.textbox_var, widget, ButtonFunctions.process_image)

                widget.textbox.insert(tk.END, file_path)
                widget.textbox.configure(state=widget_original_state)

            # Just in case its ever needed
            return file_path

    # Grabs the Path to a Directory, and if possible adds this into a widgets textbox
    @staticmethod
    def browse_directory(widget_id: str) -> str:
        """
            Grabs the Path to a Directory, and if possible adds this into a widgets textbox
            :param widget_id: The Unique ID of the Widget that Called this function
            :return: The Path on Disk to the Output Folder
        """
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

    # Grabs all required parameters and passes it to either the DisplayKeys_Previewer update or
    # Determine_Split_Type function.
    # Currently, defaults are provided for any of the required inputs that are missing.
    @staticmethod
    def process_image(widget_id: str):
        """
            Grabs all required parameters and passes it to either the DisplayKeys_Previewer update or
            Determine_Split_Type function.

            Currently, no defaults are provided for any of the required inputs that are missing.
            :param widget_id: The Unique ID of the Widget that Called this function
        """
        print("---Processing Image---")
        print("Widget ID: " + widget_id)
        calling_widget = next((widget for widget in app.properties if widget.id == widget_id), None)
        widgets = app.properties
        previewer = app.preview


        # Get Image Properties Type
        get_params_type_widget = next((widget for widget in widgets if widget.id == "GetParamsType"), None)

        # Get Text boxes to process image
        get_image_widget = next((widget for widget in widgets if widget.id == "GetImage"), None)
        get_output_widget = next((widget for widget in widgets if widget.id == "GetOutput"), None)
        get_rows_widget = next((widget for widget in widgets if widget.id == "GetRows"), None)
        get_columns_widget = next((widget for widget in widgets if widget.id == "GetColumns"), None)
        get_gap_widget = next((widget for widget in widgets if widget.id == "GetGap"), None)

        # TODO: 1.) Change to directly getting values from the TextBoxes rather than deciding what it should be based on
        # TODO: the dropdown selection. Use a 'for loop' to iterate through the widgets just in case to make sure
        # TODO: they exist, and only if they dont exist will it return 'defaults'. (Once it is a profile?)
        # TODO: Otherwise will directly get value, and if value is 'NONE' then return, and show pop-up error message.

        if all(widget is not None for widget in
               [get_image_widget, get_output_widget, get_rows_widget, get_columns_widget, get_gap_widget,
                get_params_type_widget, previewer]):

            # Will always attempt to get the Image and Output Dir as it will ALWAYS be required
            image_path = get_image_widget.textbox.get() if get_image_widget.textbox.get() else None
            output_dir = get_output_widget.textbox.get() if get_output_widget.textbox.get() else None
            if not image_path:
                image_path = "./Preview.png"  # #Sys._MEIPASS + "./Preview.png"

                # Disable Trace temporarily to not call this function again mid-execution
                ButtonFunctions.disable_trace(get_image_widget.textbox_var, get_image_widget.textbox_trace)

                # Temporarily set the text entry widget to normal state to update its value
                get_image_widget.textbox.configure(state="normal")
                get_image_widget.textbox.delete(0, tk.END)

                get_image_widget.textbox.insert(tk.END, image_path)
                get_image_widget.textbox.configure(state="readonly")

                # Re-enable Trace
                ButtonFunctions.enable_trace(get_image_widget.textbox_var, get_image_widget,
                                             lambda *args: ButtonFunctions.process_image(get_image_widget.id))

            if not output_dir:
                output_dir = os.path.join(os.path.expanduser("~"), "Desktop")

                # Temporarily set the text entry widget to normal state to update its value
                get_output_widget.textbox.configure(state="normal")
                get_output_widget.textbox.delete(0, tk.END)
                get_output_widget.textbox.insert(tk.END, output_dir)
                get_output_widget.textbox.configure(state="readonly")

            # Determine if the default or user-defined values should be used
            # Can later be expanded to profiles (i.e. 'CurrentProfile')
            if get_params_type_widget.dropdown_var.get() == "Defaults":
                rows = int(get_rows_widget.spinbox_default)
                columns = int(get_columns_widget.spinbox_default)
                gap = int(get_gap_widget.spinbox_default)
                x_offset = 0
                y_offset = 0

            elif get_params_type_widget.dropdown_var.get() == "User Defined":
                rows = int(get_rows_widget.spinbox.get()) if get_rows_widget.spinbox.get().isnumeric() else None
                columns = int(
                    get_columns_widget.spinbox.get()) if get_columns_widget.spinbox.get().isnumeric() else None
                gap = int(get_gap_widget.spinbox.get()) if get_gap_widget.spinbox.get().isnumeric() else None
                x_offset = previewer.final_offset["x"] if previewer.final_offset else None
                y_offset = previewer.final_offset["y"] if previewer.final_offset else None
                if not all(param is not None for param in [rows, columns, gap, x_offset, y_offset]):
                    # TODO: Make into Error Pop-up in the future
                    return
            else:
                return

            if widget_id == "SplitImage":
                # Split Image
                # Determine_Split_Type function then passes it to the appropriate Splitting funcion
                determine_split_type(image_path, output_dir, rows, columns, gap, x_offset, y_offset)
            else:
                # Update the preview
                app.preview.update_preview(image_path, rows, columns, gap)

        else:
            print("One or more required widgets are missing.")

    # --- Dropdowns: ---
    # Hides / Un-hides specific Widgets
    # TODO: Make generic so that dropdown button provides the list of WidgetID's its responsible for.
    # TODO: Will make life easier for future dropdown functions as well (namely profiles etc.).
    @staticmethod
    def property_options_visibility(properties: list[DisplayKeys_Composite_Widget]):
        """
            Hides / Un-hides specific Widgets
            (Will change in the future be changed to provide the list of Widgets it wants the visibility toggled for)
            :param properties: The list of Properties Widgets.
        """
        widgets = properties

        properties_dropdown_widget = next((widget for widget in widgets if widget.id == "GetParamsType"), None)
        option = properties_dropdown_widget.dropdown_var.get()

        # Get the widgets to show/hide
        get_rows_widget = next((widget for widget in widgets if widget.id == "GetRows"), None)
        get_columns_widget = next((widget for widget in widgets if widget.id == "GetColumns"), None)
        get_gap_widget = next((widget for widget in widgets if widget.id == "GetGap"), None)

        # Show/hide the widgets based on the selected option
        if all(widget is not None for widget in [get_rows_widget, get_columns_widget, get_gap_widget]):
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
def determine_split_type(file_path: str, output_dir: str, rows: int, cols: int, gap: int, x_offset: float, y_offset: float):
    print("---Determining File Type---")

    # The supported file formats:
    image_formats = get_supported_types()[0]
    animated_formats = get_supported_types()[1]

    print("File Types are: ")
    print(get_supported_types()[0])
    print(get_supported_types()[1])

    try:
        # Check if Image Format is supported
        with Image.open(file_path) as image:
            print("Image can be opened: " + (
                "True" if image else "False") + "\n   Image format is: " + "." + image.format.lower())
            # Is Static
            if "." + image.format.lower() in image_formats:
                split_static(file_path, output_dir, rows, cols, gap, x_offset, y_offset)
                return True
            # Is Animated
            elif "." + image.format.lower() in animated_formats:
                split_animated(file_path, output_dir, rows, cols, gap, x_offset, y_offset)
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


# TODO:
#  1.) Combine image splitting logic into one function, update split_image/split_gif to call that logic as needed
#      ---------- DONE ----------
#  2.) Update split_.../calculate_... functions to use newly added 'Offset' inputs.
#      ---------- DONE ----------
#  3.) Add offset input, limit(clamp) max offset amount to 1cell in both width / height
#      ---------- DONE ----------           ( temporarily(?) in Previewer )
#  3.) Replace the Previewer Drawing Functionality inside of the Previewer Update Function
#      to use the calculate_image_split function returned 'preview_coordinates'
#       ( This may be too complicated now with the way the Offset input interacts with the Preview rendering )
#       ( Will check when I am not sleep deprived to make sure it works when adapting to use external function )
#  4.) Wrap all splitting related functions into class, no reason other than that I prefer it this way...


# Calls 'calculate_image_split' and saves its output 'image_cells'
def split_static(image_path: str, output_dir: str, rows: int, cols: int, gap: int, x_offset: float, y_offset: float):
    # Open the image using PIL
    static_image = Image.open(image_path)

    # Split the Image
    split_image = calculate_image_split(static_image, rows, cols, gap, x_offset, y_offset)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output file path
    filename_without_extension = os.path.splitext(os.path.basename(static_image.filename))[0]

    # Save the image-cells
    cell: ImageTk.PhotoImage
    for cell in split_image["image_cells"]:
        output_path = os.path.join(output_dir, f"{filename_without_extension}_{cell.filename}.png")
        cell.save(output_path)

        print(f"Saved {output_path}")


# Calls 'calculate_image_split' for each frame of an image
# Recombines each image cell for each frame, before saving the combined Image-Cell
# Preserves or adds Frame Timings in case Frame's are missing this information.
# Discards 0ms Frame Times. Default Frame Timing is 100ms. If only some Frame's have timing, average will be used.
# noinspection PyUnresolvedReferences
def split_animated(gif_path: str, output_dir: str, rows: int, cols: int, gap: int, x_offset: float, y_offset: float):
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

    # Takes the extracted frames from the gif and splits them individually
    modified_frame_cells = []
    for frame in frames:
        split_frame = calculate_image_split(frame, rows, cols, gap, x_offset, y_offset)
        modified_frame_cells.append(split_frame["image_cells"])

    combined_cells = []
    # Combine Image cell's into gif cell's (ie. [frame 0 cell 0] + [frame 1 cell 0] + [frame 2 cell 0] + etc.)
    num_cells = len(modified_frame_cells[0])
    for cell_index in range(num_cells):
        for frame_cells in modified_frame_cells:
            combined_cells.append(frame_cells[cell_index])

        # Generate the output file path
        filename_without_extension = os.path.splitext(os.path.basename(gif.filename))[0]

        # Use the filename of the cell image for creating the output_path

        cell_name = combined_cells[0].filename
        output_path = os.path.join(output_dir, f"{filename_without_extension}_{cell_name}.gif")

        # Save the combined cells as a .gif file
        combined_cells[0].save(output_path, save_all=True, append_images=combined_cells[1:],
                               duration=frame_durations, loop=0)

        print(f"Saved {output_path}")
        combined_cells = []


# Splits the provided Image into Image-Cell's based on provided parameters.
# Will also crop the Image-Cells into a Square Format
# Returns {preview_coordinates, image_cells}
def calculate_image_split(image: ImageTk, rows: int, cols: int, gap: int, x_offset: float, y_offset: float) -> dict[str, list[dict] | str, list[ImageTk.PhotoImage]]:
    preview_grid = []
    cropped_cells = []

    # Calculate the width and height of each image-cell
    width, height = image.size
    print("Image Dimensions:", width, height)
    cell_width = (width - (cols - 1) * gap) // cols
    cell_height = (height - (rows - 1) * gap) // rows
    print("Cell Dimensions:", cell_width, cell_height)

    # Determine the maximum cell size (to maintain square shape)
    max_cell_size = min(cell_width, cell_height)
    print("Max Cell Size:", max_cell_size)

    # Calculate the horizontal and vertical gap offsets for cropping
    gap_horizontal_offset = (cell_width - max_cell_size) // 2
    gap_vertical_offset = (cell_height - max_cell_size) // 2

    print("Gap Offsets:", gap_horizontal_offset, gap_vertical_offset)

    # Determine the longest dimension (width or height)
    longest_dimension = "width" if cell_width > cell_height else "height"

    # Split the image and save each image-cell
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates for cropping
            left = (col * (cell_width + gap) + gap_horizontal_offset) - x_offset
            upper = (row * (cell_height + gap) + gap_vertical_offset) - y_offset

            # Remove rows/columns only if they are part of the Outlier image-cells
            if row == 0:
                upper += gap_vertical_offset
            elif row == rows - 1:
                upper -= gap_vertical_offset
            if col == 0:
                left += gap_horizontal_offset
            elif col == cols - 1:
                left -= gap_horizontal_offset
            if longest_dimension == "width":
                right = left + max_cell_size
                lower = upper + cell_height
            else:
                right = left + cell_width
                lower = upper + max_cell_size

            # Crop all image-cells
            image_cell = image.crop((left, upper, right, lower))

            ########## Outputs ##########

            # Generate new Image-Cell Name
            image_cell.filename = f"{row}_{col}"
            # Save Image Cell
            cropped_cells.append(image_cell)

            # Store Coordinates of split image cells, for Previewer
            grid_cell = [{
                "cell": f"{row}_{col}",
                "Left_Coord": left,
                "Right_Coord": right,
                "Upper_Coord": upper,
                "Lower_Coord": lower,
            }]
            preview_grid.append(grid_cell)

    return {"preview_coordinates": preview_grid, "image_cells": cropped_cells}


####################################################################################################################
#                                                    Create GUI
####################################################################################################################


if __name__ == "__main__":
    # For flow debugging
    print("---Code Start---")

    # Create/Start Application Window
    app = DisplayKeys_GUI()
    app.run()
