import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
                             QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QProgressBar, QSpacerItem)

from src.dct import Worker


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
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

        # Label
        self.progress_bar = QProgressBar()

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
        self.layout.addItem(QSpacerItem(20, 20))
        self.layout.addWidget(self.progress_bar)
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
        self.input_line_edit.setText(path)

    def get_output_folder(self):
        path = QFileDialog().getExistingDirectory(self, 'Output folder')
        self.output_line_edit.setText(path)

    def reset_fields(self):
        self.input_line_edit.setText("")
        self.output_line_edit.setText("")
        self.f_parameter_line_edit.setText("")
        self.d_parameter_line_edit.setText("")
        self.progress_bar.setValue(0)
        self.thread.quit()

    def compute(self):
        self.progress_bar.setValue(0)

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self.progress_bar, self.input_line_edit.text(),
                             self.f_parameter_line_edit.text(), self.d_parameter_line_edit.text())
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_progress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.compute_button.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.compute_button.setEnabled(True)
        )

    def report_progress(self, i):
        self.progress_bar.setValue(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
