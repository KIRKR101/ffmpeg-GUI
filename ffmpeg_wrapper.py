import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class FFmpegWrapper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # File format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel('Output Format:'))
        self.format_combo = QComboBox()
        self.format_combo.addItems(['mp4', 'avi', 'mkv', 'webm'])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # Codec selection
        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel('Codec:'))
        self.codec_combo = QComboBox()
        self.codec_combo.addItems(['libx264', 'libx265', 'vp9', 'aom-av1'])
        codec_layout.addWidget(self.codec_combo)
        layout.addLayout(codec_layout)

        # Compression level
        compress_layout = QHBoxLayout()
        compress_layout.addWidget(QLabel('Compression Level:'))
        self.compress_slider = QSlider(Qt.Horizontal)
        self.compress_slider.setMinimum(1)
        self.compress_slider.setMaximum(100)
        self.compress_slider.setValue(50)
        self.compress_label = QLabel('50')
        self.compress_slider.valueChanged.connect(self.update_compress_label)
        compress_layout.addWidget(self.compress_slider)
        compress_layout.addWidget(self.compress_label)
        layout.addLayout(compress_layout)

        # File selection
        self.file_button = QPushButton('Select Input File')
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        # Convert button
        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.convert_file)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)
        self.setWindowTitle('FFmpeg Wrapper')
        self.show()

    def update_compress_label(self, value):
        self.compress_label.setText(str(value))

    def select_file(self):
        self.input_file, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if self.input_file:
            self.file_button.setText(f"Selected: {self.input_file}")

    def convert_file(self):
        if not hasattr(self, 'input_file'):
            print("Please select an input file first.")
            return

        output_format = self.format_combo.currentText()
        codec = self.codec_combo.currentText()
        crf = 51 - int(self.compress_slider.value() / 2)  # Convert 1-100 scale to 0-51 CRF scale
        output_file = f"output.{output_format}"

        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', codec,
            '-crf', str(crf),
            '-preset', 'medium',
            output_file
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Conversion complete. Output file: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during conversion: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FFmpegWrapper()
    sys.exit(app.exec_())