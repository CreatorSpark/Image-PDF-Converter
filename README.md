# Image-PDF Converter

A powerful and user-friendly desktop application for seamlessly converting between images and PDFs, featuring A4 standardization and advanced image management.

## 🌟 Features

- **Image to PDF Conversion**
  - Convert multiple JPG images to a single PDF
  - Automatic A4 size standardization
  - Maintains aspect ratio with white margins
  - Professional-grade output quality

- **PDF to Image Conversion**
  - Extract images from PDF files
  - Adjustable quality settings
  - Batch processing support

- **Advanced Image Management**
  - Drag-and-drop file reordering
  - Real-time image preview
  - Image rotation (90° clockwise/counter-clockwise)
  - Natural file sorting (1, 2, 10 instead of 1, 10, 2)
  - Bulk file operations

- **Professional UI**
  - Modern themed interface
  - Intuitive controls
  - Progress indicators
  - Status updates

## 📋 Requirements

- Python 3.7 or higher
- Poppler (for PDF to Image conversion)

### Installing Poppler:

- **Windows:**
  - Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases)
  - Add to system PATH

- **Linux:**  ```bash
  sudo apt-get install poppler-utils  ```

- **macOS:**  ```bash
  brew install poppler  ```

## 🚀 Installation

1. Clone the repository:   ```bash
   git clone https://github.com/CreatorSpark/image-pdf-converter.git
   cd image-pdf-converter   ```

2. Create and activate virtual environment:   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python -m venv venv
   source venv/bin/activate   ```

3. Install dependencies:   ```bash
   pip install -r requirements.txt   ```

## 💻 Usage

Run the application: python src/image_pdf_converter.py


### Converting Images to PDF:
1. Select "JPG to PDF" mode
2. Click "Add Files" or drag and drop JPG images
3. Arrange images in desired order
4. Click "Convert Files" and choose output location

### Converting PDF to Images:
1. Select "PDF to JPG" mode
2. Add PDF file(s)
3. Adjust quality slider if needed
4. Click "Convert Files" and select output folder

## 🛠️ Technical Details

- Built with Python and Tkinter
- Uses PIL for image processing
- Implements pdf2image for PDF conversion
- A4 size standardization (8.27" × 11.69" at 300 DPI)
- Optimized image compression

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by CreatorSpark

- GitHub: [@CreatorSpark](https://github.com/CreatorSpark)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/CreatorSpark/image-pdf-converter/issues).

## ⭐ Show your support

Give a ⭐️ if this project helped you!

## 📞 Contact

For support or queries, please open an issue in the GitHub repository.