from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QStandardItemModel, QPainter, QPixmap, QPen, QColor
from PyQt6.uic import loadUi
import sys, os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence


# Preview section constructor
class ImageSplitterPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None
        self.rows = 0
        self.columns = 0
        self.gap = 0

    def paintEvent(self, event):
        if self.image_path is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Load the image
        pixmap = QPixmap(self.image_path)

        # Rescale image to fit within preview boundaries
        if pixmap.height() == 0:
            return
        else:
            aspect_ratio = pixmap.width() / pixmap.height()
        preview_width = self.width()
        preview_height = self.height()
        if preview_width / preview_height >= aspect_ratio:
            # Constrained by height
            new_height = preview_height
            new_width = int(preview_height * aspect_ratio)
        else:
            # Constrained by width
            new_width = preview_width
            new_height = int(preview_width / aspect_ratio)
        scaled_pixmap = pixmap.scaled(
            new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio
        )

        # Calculate offsets to center the image
        x_offset = (preview_width - new_width) // 2
        y_offset = (preview_height - new_height) // 2

        # Draw the scaled image
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)

        # Draw red lines to indicate splitting
        pen = QPen(QColor("red"))
        pen.setWidth(self.gap)
        painter.setPen(pen)

        if self.columns == 0 or self.rows == 0:
            cell_width = 0
            cell_height = 0
        else:
            cell_width = new_width // self.columns
            cell_height = new_height // self.rows

        # Vertical lines
        for i in range(1, self.columns):
            x = x_offset + i * cell_width
            painter.drawLine(x, y_offset, x, y_offset + new_height)

        # Horizontal lines
        for i in range(1, self.rows):
            y = y_offset + i * cell_height
            painter.drawLine(x_offset, y, x_offset + new_width, y)

    def updatePreview(self, image_path, rows, columns, gap):
        self.image_path = image_path
        self.rows = rows
        self.columns = columns
        self.gap = gap
        self.update()


class UI_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi("gui_source.ui", self)

        # Initializing the custom preview widget
        self.preview_frame = ImageSplitterPreview(self.preview_wrapper)
        self.preview_frame.setMaximumSize(QSize(16777215, 16777215))
        self.preview_frame.setObjectName("preview_frame")
        self.verticalLayout_6.addWidget(self.preview_frame)

        # Different widgets signal handling
        self.comboBox.currentIndexChanged.connect(self.settings_visibilty)
        self.browse_button.clicked.connect(self.browse_image)
        self.browse_button_2.clicked.connect(self.browse_directory)
        self.comboBox.currentIndexChanged.connect(self.settings_visibilty)
        self.rows_box.valueChanged.connect(self.process_preview)
        self.columns_box.valueChanged.connect(self.process_preview)
        self.gap_box.valueChanged.connect(self.process_preview)
        self.split_image_button.clicked.connect(self.process_image)

        self.settings_wrapper.hide()

    def button_clicked(self):
        print("Button clicked!")

    def get_supported_types(self):
        # The supported file formats:
        sup_image_formats = [".png", ".jpg", ".jpeg", ".bmp"]
        sup_animated_formats = [".gif"]
        return sup_image_formats, sup_animated_formats

    # Grabs all required parameters and passes it to the DisplayKeys_Previewer widget.
    # Currently, defaults are provided for any of the required inputs that are missing.
    def process_preview(self):
        print("---Processing Preview---")

        # Get Image Properties Type
        get_params_type = self.comboBox.currentText()

        # Get Text boxes to process image
        image_path = self.input_image_path.text()
        output_dir = self.input_image_path_2.text()
        rows = int(self.rows_box.value())
        columns = int(self.columns_box.value())
        gap = int(self.gap_box.value())

        # Determine if the default or user-defined values should be used
        if get_params_type == "Defaults":
            image_path = image_path
            if not image_path:
                image_path = "assets/Preview.png"
            rows = 2
            columns = 6
            gap = 40

        elif get_params_type == "User Defined":
            if not image_path:
                image_path = "assets/Preview.png"
        else:
            return

        # Update the preview
        self.preview_frame.updatePreview(image_path, rows, columns, gap)

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
                duration = int(gif.info["duration"])
                if duration > 0:
                    frame_durations.append(duration)
                else:
                    frame_durations.append(0)
            except (KeyError, TypeError):
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
                filename_without_extension = os.path.splitext(
                    os.path.basename(gif.filename)
                )[0]
                output_path = os.path.join(
                    output_dir, f"{filename_without_extension}_{row}_{col}.gif"
                )
                print("Num of Modified Frames: " + str(modified_frames.__sizeof__()))

                # Save all frames of the image-cell into a single .gif file
                modified_frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=modified_frames[1:],
                    duration=frame_durations,  # Might make this a user definable variable in the future
                    loop=0,
                )
                modified_frames = []
                print(
                    f"gif_cell_{row}_{col} has this many frames: "
                    + str(Image.open(output_path).n_frames)
                )
                print(f"Saved {output_path}")

    # Split the image
    def split_image(self, image_path, output_dir, rows, cols, gap):
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

        #  maximum cell size (to maintain square shape)
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
                filename_without_extension = os.path.splitext(
                    os.path.basename(image.filename)
                )[0]
                output_path = os.path.join(
                    output_dir, f"{filename_without_extension}_{row}_{col}.png"
                )

                # Save the image-cells
                image_cell.save(output_path)

                print(f"Saved {output_path}")

    # Checks the provided image and determines whether it's a static or dynamic image format.
    # Also passes along rest of variables provided by ButtonFunctions.ProcessImage
    def determine_split_type(self, file_path, output_dir, rows, cols, gap):
        print("---Determening File Type---")

        # The supported file formats:
        image_formats = self.get_supported_types()[0]
        animated_formats = self.get_supported_types()[1]

        print("File Types are: ")
        print(self.get_supported_types()[0])
        print(self.get_supported_types()[1])

        try:
            # Check if image format is supported
            with Image.open(file_path) as image:
                print(
                    "Image can be opened: "
                    + ("True" if image else "False")
                    + "\n   Image format is: "
                    + "."
                    + image.format.lower()
                )
                # Is Image
                if "." + image.format.lower() in image_formats:
                    self.split_image(file_path, output_dir, rows, cols, gap)
                    return True
                # Is Animated
                elif "." + image.format.lower() in animated_formats:
                    self.split_gif(file_path, output_dir, rows, cols, gap)
                    return True
                else:
                    print("No formats matched")

        # Is not of a supported image format
        except TypeError as error_message:
            messagebox.showerror(
                "Error"
                f"File Format not supported\nCurrently supported formats are: \n- Image | {self.get_supported_types()[0]} \n- Animated | {self.get_supported_types()[1]}"
            )
            print("Wrong File Type: ", type(error_message).__name__, str(error_message))
            return None

    def process_image(self):
        print("---Processing Images---")
        # Get Image Properties Type
        get_params_type = self.comboBox.currentText()

        # Get Text boxes to process image
        image_path = self.input_image_path.text()
        output_dir = self.input_image_path_2.text()
        rows = int(self.rows_box.value())
        columns = int(self.columns_box.value())
        gap = int(self.gap_box.value())

        # Determine if the default or user defined values should be used
        if get_params_type == "Defaults":
            if not image_path:
                image_path = "assets/Preview.png"
            if not output_dir:
                output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            rows = 2
            columns = 6
            gap = 40
        # Get the text from the required textboxes
        elif get_params_type == "User Defined":
            if not image_path:
                image_path = "assets/Preview.png"
            if not output_dir:
                output_dir = os.path.join(os.path.expanduser("~"), "Desktop")

        # Pass onto Determine_Split_Type function, that then passes it onto the appropriate Splitting funcion
        self.determine_split_type(image_path, output_dir, rows, columns, gap)

    # Buttons
    # Grabs the Path to an Image, and if possible adds this into a widgets textbox
    def browse_image(self):
        print("---Browsing for Image---")

        # Ask the user to select an Image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")]
        )
        # Put File Path into textbox if widget has a textbox
        if file_path:
            self.input_image_path.setText(file_path)
            self.process_preview()
            # Just in case its ever needed
            return file_path

    # Grabs the Path to a Directory, and if possible adds this into a widgets textbox
    def browse_directory(self):
        print("---Browsing for Output Dir---")
        output_path = filedialog.askdirectory()
        # Put Directory Path into textbox if widget has a textbox
        if output_path:
            self.input_image_path_2.setText(output_path)
            # Just in case its ever needed
            return output_path

    # Function that shows or hides the settings box according to the value of the ComboBox
    def settings_visibilty(self, index):
        if index == 0:
            self.settings_wrapper.hide()
        else:
            self.settings_wrapper.show()


if __name__ == "__main__":
    app = QApplication([])
    window = UI_MainWindow()
    window.show()
    app.exec()
