import sys

from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
                             QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Variables
        self.input_path = None
        self.output_path = None
        self.f = None
        self.d = None

        # Window parameters
        self.setWindowTitle("MCS - DCT")
        self.setMinimumWidth(500)

        # Outer layout
        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.form_layout = QFormLayout()
        self.horizontal_layout = QHBoxLayout()

        # Widgets
        self.input_browse_button = QPushButton("Browse")
        self.output_browse_button = QPushButton("Browse")
        self.input_line_edit = QLineEdit()
        self.output_line_edit = QLineEdit()

        self.f_parameter_line_edit = QLineEdit()
        self.d_parameter_line_edit = QLineEdit()

        self.reset_button = QPushButton("Reset")
        self.compute_button = QPushButton("Compute")

        # Build layouts
        self.build_path_grid()
        self.build_parameters_form()
        self.build_buttons_box()

        self.layout.addLayout(self.grid_layout)
        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.horizontal_layout)
        self.setLayout(self.layout)

    def build_path_grid(self):
        # Path
        self.input_browse_button.clicked.connect(self.get_image_file)
        self.output_browse_button.clicked.connect(self.get_output_folder)
        self.grid_layout.addWidget(QLabel("Image File: "), 0, 0, 1, 1)
        self.grid_layout.addWidget(self.input_line_edit, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.input_browse_button, 0, 2, 1, 1)
        self.grid_layout.addWidget(QLabel("Output Folder: "), 1, 0, 1, 1)
        self.grid_layout.addWidget(self.output_line_edit, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.output_browse_button, 1, 2, 1, 1)

    def build_parameters_form(self):
        self.form_layout.addRow("F Parameter:", self.f_parameter_line_edit)
        self.form_layout.addRow("d Parameter:", self.d_parameter_line_edit)

    def build_buttons_box(self):
        self.reset_button.clicked.connect(self.reset_fields)
        self.horizontal_layout.addWidget(self.reset_button)
        self.compute_button.clicked.connect(self.compute)
        self.horizontal_layout.addWidget(self.compute_button)

    def get_image_file(self):
        filter_file = 'Image Files (*.bmp)\nAll Files (*.*)'
        path, _ = QFileDialog().getOpenFileName(self, 'Image', filter=filter_file)
        print(f"Input Path: {path}")
        self.input_path = path
        self.input_line_edit.setText(path)

    def get_output_folder(self):
        path = QFileDialog().getExistingDirectory(self, 'Output folder')
        print(f"Output Path: {path}")
        self.output_path = path
        self.output_line_edit.setText(path)

    def reset_fields(self):
        self.input_line_edit.setText("")
        self.output_line_edit.setText("")
        self.f_parameter_line_edit.setText("")
        self.d_parameter_line_edit.setText("")
        self.input_path = None
        self.output_path = None
        self.d = None
        self.f = None

    def compute(self):
        self.update_variables()
        print(f"Input file: {self.input_path}")
        print(f"Output folder: {self.output_path}")
        print(f"F parameter: {self.f}")
        print(f"d parameter: {self.d}")

    def update_variables(self):
        self.input_path = self.input_line_edit.text()
        self.output_path = self.output_line_edit.text()
        self.f = self.f_parameter_line_edit.text()
        self.d = self.d_parameter_line_edit.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
