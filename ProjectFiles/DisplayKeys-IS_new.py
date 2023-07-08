from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QPainter, QColor, QPen)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)
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
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)

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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1109, 830)
        font = QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u"ProjectFiles/assets/DisplayKeys-IS.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
# Main stylsheet file
        MainWindow.setStyleSheet(
u"#left_menu_wrapper {\n"
"	background-color: #22282c;\n"
"}\n"
"\n"
"#preview_wrapper {\n"
"	background-color: #292f33;\n"
"}\n"
"\n"
"* {\n"
"	font: \"Poppins\";\n"
"}\n"
"\n"
"QLabel {\n"
"color: white;\n"
"}\n"
"QPushButton{\n"
"	border-radius: 10px;\n"
"	background-color: rgb(65, 75, 81);\n"
"	color: white;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(82, 95, 102);\n"
"    border: 2px solid #AAAAAA;\n"
"}\n"
"QComboBox {\n"
"	border-radius: 10px;\n"
"	background-color: rgb(65, 75, 81);\n"
"	color: white;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_wrapper = QWidget(self.centralwidget)
        self.left_menu_wrapper.setObjectName(u"left_menu_wrapper")
        self.left_menu_wrapper.setStyleSheet(u"")
        self.verticalLayout_4 = QVBoxLayout(self.left_menu_wrapper)
        self.verticalLayout_4.setSpacing(30)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

# _____________________________________
# Main Title
# _____________________________________

        self.title_label = QLabel(self.left_menu_wrapper)
        self.title_label.setObjectName(u"title_label")
        font1 = QFont()
        font1.setFamilies([u"Poppins"])
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setItalic(False)
        self.title_label.setFont(font1)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.title_label)

# _________________________________________
# Import image section
# _________________________________________

        self.import_image_wrapper = QWidget(self.left_menu_wrapper)
        self.import_image_wrapper.setObjectName(u"import_image_wrapper")
        self.import_image_wrapper.setStyleSheet(
u".QWidget {\n"
"border-bottom: 2px solid grey\n"
"}")
        self.verticalLayout = QVBoxLayout(self.import_image_wrapper)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.browse_label = QLabel(self.import_image_wrapper)
        self.browse_label.setObjectName(u"browse_label")
        self.browse_label.setFont(font1)
        self.browse_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.browse_label)

        self.input_image_path = QLabel(self.import_image_wrapper)
        self.input_image_path.setObjectName(u"input_image_path")
        self.input_image_path.setWordWrap(True)
        font2 = QFont()
        font2.setPointSize(15)
        font2.setBold(False)
        font2.setItalic(False)
        self.input_image_path.setFont(font2)
        self.input_image_path.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.input_image_path)



        self.browse_button = QPushButton(self.import_image_wrapper)
        self.browse_button.setObjectName(u"browse_button")
        self.browse_button.setMinimumSize(QSize(0, 40))
        self.browse_button.setFont(font2)
        self.browse_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.browse_button.clicked.connect(self.browse_image)

        self.verticalLayout.addWidget(self.browse_button)


        self.verticalLayout_4.addWidget(self.import_image_wrapper)

# _________________________________________
# Output directory section
# _________________________________________

        self.output_wrapper = QWidget(self.left_menu_wrapper)
        self.output_wrapper.setObjectName(u"output_wrapper")
        self.output_wrapper.setStyleSheet(
u".QWidget {\n"
"border-bottom: 2px solid grey\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.output_wrapper)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.browse_label_2 = QLabel(self.output_wrapper)
        self.browse_label_2.setObjectName(u"browse_label_2")
        self.browse_label_2.setFont(font1)
        self.browse_label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.browse_label_2)

        self.input_image_path_2 = QLabel(self.output_wrapper)
        self.input_image_path_2.setObjectName(u"input_image_path_2")
        self.input_image_path_2.setFont(font2)
        self.input_image_path_2.setAlignment(Qt.AlignCenter)
        self.input_image_path.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.input_image_path_2)

        self.browse_button_2 = QPushButton(self.output_wrapper)
        self.browse_button_2.setObjectName(u"browse_button_2")
        self.browse_button_2.setMinimumSize(QSize(0, 40))
        self.browse_button_2.setFont(font2)
        self.browse_button_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.browse_button_2.clicked.connect(self.browse_directory)

        self.verticalLayout_2.addWidget(self.browse_button_2)


        self.verticalLayout_4.addWidget(self.output_wrapper)

        self.splitting_wrapper = QWidget(self.left_menu_wrapper)
        self.splitting_wrapper.setObjectName(u"splitting_wrapper")
        self.splitting_wrapper.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.splitting_wrapper)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitting_title = QLabel(self.splitting_wrapper)
        self.splitting_title.setObjectName(u"splitting_title")
        self.splitting_title.setFont(font1)
        self.splitting_title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.splitting_title)

# _________________________________________

        self.comboBox = QComboBox(self.splitting_wrapper)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(162, 30))
        self.comboBox.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Poppins"])
        font3.setPointSize(15)
        font3.setBold(False)
        font3.setItalic(False)
        self.comboBox.setFont(font3)
        self.comboBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.comboBox.setStyleSheet(
u"QComboBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #CCCCCC;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    min-width: 150px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: right;\n"
"    width: 20px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #CCCCCC;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #EEEEEE, stop:1 #FFFFFF);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(assets/chevron-down.svg)\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #F2F2F2;\n"
"    border: 1px solid #AAAAAA;\n"
"}\n"
"\n"
"QComboBox::drop-down:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #DDDDDD, stop:1 #FFFFFF);\n"
"}")
        self.comboBox.setFrame(True)
        self.comboBox.currentIndexChanged.connect(self.settings_visibilty)

        self.verticalLayout_5.addWidget(self.comboBox)

# _________________________________________
# User defined settings box
# _________________________________________

        self.settings_wrapper = QWidget(self.splitting_wrapper)
        self.settings_wrapper.setObjectName(u"settings_wrapper")
        self.settings_wrapper.setFont(font2)
        self.settings_wrapper.setStyleSheet(
u"QSpinBox {\n"
"    border: 1px solid #d1d1d1;\n"
"    border-radius: 10px;\n"
"    padding: 5px;\n"
"    background-color: #f5f5f5;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QSpinBox:hover {\n"
"    background-color: #e8e8e8;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 16px;\n"
"    border-top-right-radius: 10px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 16px;\n"
"    border-bottom-right-radius: 10px;\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    image: url(assets/chevron-up.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(assets/chevron-down.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.settings_wrapper)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.rows_label = QLabel(self.settings_wrapper)
        self.rows_label.setObjectName(u"rows_label")
        self.rows_label.setFont(font2)
        self.rows_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.rows_label)

        self.rows_box = QSpinBox(self.settings_wrapper)
        self.rows_box.setObjectName(u"rows_box")
        self.rows_box.setMaximumSize(QSize(100, 16777215))
        self.rows_box.setFont(font2)
        self.rows_box.setAlignment(Qt.AlignCenter)
        self.rows_box.setMaximum(100)
        self.rows_box.setMinimum(2)
        self.rows_box.valueChanged.connect(self.process_preview)

        self.verticalLayout_3.addWidget(self.rows_box)

        self.columns_label = QLabel(self.settings_wrapper)
        self.columns_label.setObjectName(u"columns_label")
        self.columns_label.setFont(font2)
        self.columns_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.columns_label)

        self.columns_box = QSpinBox(self.settings_wrapper)
        self.columns_box.setObjectName(u"columns_box")
        self.columns_box.setMaximumSize(QSize(100, 16777215))
        self.columns_box.setFont(font2)
        self.columns_box.setAlignment(Qt.AlignCenter)
        self.columns_box.setMaximum(100)
        self.columns_box.setMinimum(2)
        self.columns_box.valueChanged.connect(self.process_preview)

        self.verticalLayout_3.addWidget(self.columns_box)

        self.gap_label = QLabel(self.settings_wrapper)
        self.gap_label.setObjectName(u"gap_label")
        self.gap_label.setFont(font2)
        self.gap_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.gap_label)

        self.gap_box = QSpinBox(self.settings_wrapper)
        self.gap_box.setObjectName(u"gap_box")
        self.gap_box.setMaximumSize(QSize(100, 16777215))
        self.gap_box.setFont(font2)
        self.gap_box.setAlignment(Qt.AlignCenter)
        self.gap_box.setMaximum(10000)
        self.gap_box.setMinimum(1)
        self.gap_box.valueChanged.connect(self.process_preview)

        self.verticalLayout_3.addWidget(self.gap_box)


        self.verticalLayout_5.addWidget(self.settings_wrapper)


        self.verticalLayout_4.addWidget(self.splitting_wrapper)

        self.settings_wrapper.hide()

# _________________________________________
# Split image button
# _____________________________________

        self.split_image_button = QPushButton(self.left_menu_wrapper)
        self.split_image_button.setObjectName(u"split_image_button")
        self.split_image_button.setMinimumSize(QSize(0, 40))
        self.split_image_button.setFont(font2)
        self.split_image_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.split_image_button.clicked.connect(self.process_image)

        self.verticalLayout_4.addWidget(self.split_image_button)


        self.horizontalLayout.addWidget(self.left_menu_wrapper)

        self.preview_wrapper = QWidget(self.centralwidget)
        self.preview_wrapper.setObjectName(u"preview_wrapper")
        self.preview_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.verticalLayout_6 = QVBoxLayout(self.preview_wrapper)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 150, -1, 150)

# _____________________________________
# Create the preview widget
# _____________________________________

        self.preview_frame = ImageSplitterPreview(self.preview_wrapper)
        self.preview_frame.setMaximumSize(QSize(16777215, 16777215))
        self.preview_frame.setObjectName(u"preview_frame")
        self.verticalLayout_6.addWidget(self.preview_frame)

# _____________________________________


        self.horizontalLayout.addWidget(self.preview_wrapper)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

# _____________________________________
#  Main Window Functions:
# _____________________________________

# Function that contains supported formats
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
                filename_without_extension = os.path.splitext(os.path.basename(image.filename))[0]
                output_path = os.path.join(output_dir, f"{filename_without_extension}_{row}_{col}.png")

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
                print("Image can be opened: " + (
                    "True" if image else "False") + "\n   Image format is: " + "." + image.format.lower())
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
            messagebox.showerror('Error' f'File Format not supported\nCurrently supported formats are: \n- Image | {self.get_supported_types()[0]} \n- Animated | {self.get_supported_types()[1]}')
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


# Function that sets the text of every widgets
# This is useful for translating the UI in the future
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DisplayKeys-IS", None))
        self.title_label.setText(QCoreApplication.translate("MainWindow", u"Image Splitter made by Neuffexx", None))
        self.browse_label.setText(QCoreApplication.translate("MainWindow", u"Choose Image", None))
        self.input_image_path.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse image", None))
        self.browse_label_2.setText(QCoreApplication.translate("MainWindow", u"Choose Output Location", None))
        self.input_image_path_2.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.browse_button_2.setText(QCoreApplication.translate("MainWindow", u"Browse folder", None))
        self.splitting_title.setText(QCoreApplication.translate("MainWindow", u"Set Splitting Paramters", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Defaults", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"User Defined", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"Defaults", None))
        self.comboBox.setToolTip("Row: 2 \nColumn: 6 \nGap: 40")
        self.comboBox.currentTextChanged.connect(self.process_preview)
        self.rows_label.setText(QCoreApplication.translate("MainWindow", u"Rows", None))
        self.columns_label.setText(QCoreApplication.translate("MainWindow", u"Columns", None))
        self.gap_label.setText(QCoreApplication.translate("MainWindow", u"Gap ( in pixels )", None))
        self.split_image_button.setText(QCoreApplication.translate("MainWindow", u"Split Image", None))

# Creating the UI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())