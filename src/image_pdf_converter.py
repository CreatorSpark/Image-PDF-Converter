import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os
from pdf2image import convert_from_path

class ImagePDFConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Image-PDF Converter By CreatorSpark")
        self.master.geometry("900x600")     
        
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_rowconfigure(2, weight=1)
        
        self.file_paths = []
        self.conversion_type = tk.StringVar(value="jpg_to_pdf")
        self.quality = tk.IntVar(value=85)
        self.dragging_index = None
        
        # Set theme colors
        self.colors = {
            'bg': '#f0f0f0',
            'header_bg': '#2c3e50',
            'header_fg': 'black',
            'listbox_bg': '#ffffff',
            'listbox_fg': '#333333',
            'button_bg': '#3498db',
            'button_fg': 'white',
            'preview_bg': '#ecf0f1'
        }
        
        self.create_widgets()
        self.enable_drag_and_drop()
        
    def create_widgets(self):
        """Create UI components with enhanced styling."""
        # Configure styles first
        style = ttk.Style()
        style.configure('Header.TFrame', background=self.colors['header_bg'])
        style.configure('Convert.TButton', padding=10)
        style.configure('Custom.TButton', padding=5)  # New style for regular buttons
        
        # Header with better styling
        header_frame = ttk.Frame(self.master)
        header_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")
        header_frame.configure(style='Header.TFrame')
        
        ttk.Label(header_frame, 
                 text="Image-PDF Converter By CreatorSpark",
                 font=("Helvetica", 24, "bold"),
                 foreground=self.colors['header_fg']).pack(pady=(10,5))
        ttk.Label(header_frame,
                 text="Dobhan Photo Studio",
                 font=("Helvetica", 12, "italic"),
                 foreground=self.colors['header_fg']).pack(pady=(0,10))

        # Conversion Type Frame with better styling
        conversion_frame = ttk.LabelFrame(self.master, text="Conversion Type", padding=10)
        conversion_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="ew")

        ttk.Style().configure('Conversion.TRadiobutton', font=("Helvetica", 12))
        ttk.Radiobutton(conversion_frame, 
                       text="JPG to PDF", 
                       variable=self.conversion_type,
                       value="jpg_to_pdf", 
                       command=self.update_ui,
                       style='Conversion.TRadiobutton').grid(row=0, column=0, padx=20)
        ttk.Radiobutton(conversion_frame, 
                       text="PDF to JPG", 
                       variable=self.conversion_type,
                       value="pdf_to_jpg", 
                       command=self.update_ui,
                       style='Conversion.TRadiobutton').grid(row=0, column=1, padx=20)

        # File List Frame with enhanced styling
        file_frame = ttk.LabelFrame(self.master, text="Selected Files", padding=10)
        file_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        self.file_listbox = tk.Listbox(file_frame, 
                                     selectmode="single",
                                     font=("Helvetica", 12),
                                     bg=self.colors['listbox_bg'],
                                     fg=self.colors['listbox_fg'],
                                     selectbackground=self.colors['button_bg'],
                                     selectforeground='white',
                                     activestyle='none')
        self.file_listbox.pack(side="left", fill="both", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", lambda e: self.preview_selected_file())

        scrollbar = ttk.Scrollbar(file_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Button Frame with enhanced styling
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")
        
        buttons = [
            ("➕ Add Files", self.add_files, "Add new files to the list"),
            ("➖ Remove", self.remove_selected_files, "Remove selected files"),
            ("🔄 Sort", self.sort_files, "Sort files naturally (e.g., 1, 2, 10 instead of 1, 10, 2)"),
            ("↪️ Rotate Right", lambda: self.rotate_image(90), "Rotate selected image 90° clockwise"),
            ("↩️ Rotate Left", lambda: self.rotate_image(-90), "Rotate selected image 90° counter-clockwise"),
            ("🗑️ Clear All", self.clear_files, "Clear all files")
        ]

        # Updated button creation without font parameter
        for text, command, tooltip in buttons:
            btn = ttk.Button(button_frame, 
                           text=text, 
                           command=command,
                           style='Custom.TButton',
                           width=15)
            btn.pack(pady=5, padx=10, fill='x')
            self.create_tooltip(btn, tooltip)

        # Preview Frame with enhanced styling
        preview_frame = ttk.LabelFrame(self.master, text="Preview", padding=10)
        preview_frame.grid(row=2, column=2, padx=20, pady=10, sticky="nsew")

        self.preview_canvas = tk.Canvas(preview_frame,
                                      bg=self.colors['preview_bg'],
                                      width=300,
                                      height=400)
        self.preview_canvas.pack(fill="both", expand=True)

        # Quality Control Frame
        self.quality_frame = ttk.LabelFrame(self.master, text="Quality Control", padding=10)
        self.quality_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

        ttk.Label(self.quality_frame, 
                 text="Output Quality:",
                 font=("Helvetica", 11)).grid(row=0, column=0, padx=5)
        
        self.quality_slider = ttk.Scale(self.quality_frame,
                                      from_=1,
                                      to=100,
                                      variable=self.quality,
                                      orient="horizontal")
        self.quality_slider.grid(row=0, column=1, padx=5, sticky="ew")
        
        ttk.Label(self.quality_frame,
                 textvariable=self.quality,
                 font=("Helvetica", 11)).grid(row=0, column=2, padx=5)

        # Convert Button with enhanced styling
        convert_btn = ttk.Button(self.master,
                               text="Convert Files",
                               command=self.convert,
                               style='Convert.TButton')
        convert_btn.grid(row=4, column=0, columnspan=3, pady=20)

        # Status Bar with enhanced styling
        self.status_bar = ttk.Label(self.master,
                                  text="Ready",
                                  font=("Helvetica", 10),
                                  relief=tk.SUNKEN,
                                  anchor="w")
        self.status_bar.grid(row=5, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # GitHub link with icon
        github_frame = ttk.Frame(self.master)
        github_frame.grid(row=5, column=2, sticky="e", padx=5, pady=5)
        
        github_icon = "🔗"  # Unicode icon as a simple solution
        github_link = ttk.Label(github_frame,
                              text=f"{github_icon} github.com/CreatorSpark",
                              font=("Helvetica", 10),
                              cursor="hand2")
        github_link.pack(side="right")
        github_link.bind("<Button-1>", lambda e: self.open_github())

        self.update_ui()

    def enable_drag_and_drop(self):
        """Enable drag-and-drop reordering for the file list."""
        self.file_listbox.bind("<ButtonPress-1>", self.on_drag_start)
        self.file_listbox.bind("<B1-Motion>", self.on_drag)
        self.file_listbox.bind("<ButtonRelease-1>", self.on_drop)

    def on_drag_start(self, event):
        """Handle the start of dragging an item."""
        widget = event.widget
        self.dragging_index = widget.nearest(event.y)
        widget.selection_clear(0, tk.END)
        widget.selection_set(self.dragging_index)

    def on_drag(self, event):
        """Handle dragging of an item."""
        widget = event.widget
        index = widget.nearest(event.y)

        if index >= 0 and index < len(self.file_paths):
            widget.selection_clear(0, tk.END)
            widget.selection_set(index)

    def on_drop(self, event):
        """Handle dropping of an item."""
        if self.dragging_index is None:
            return

        widget = event.widget
        new_index = widget.nearest(event.y)

        if new_index != self.dragging_index and new_index >= 0 and new_index < len(self.file_paths):
            # Rearrange file paths and update Listbox
            item = self.file_paths.pop(self.dragging_index)
            self.file_paths.insert(new_index, item)

            self.update_file_listbox()

        self.dragging_index = None  # Reset dragging index after drop

    def update_file_listbox(self):
        """Refresh the Listbox with current file paths and show file count."""
        self.file_listbox.delete(0, tk.END)
        for file in self.file_paths:
            self.file_listbox.insert(tk.END, os.path.basename(file))
        
        # Update file count in frame title
        file_count = len(self.file_paths)
        self.file_listbox.master.configure(text=f"Selected Files ({file_count})")

    def create_tooltip(self, widget, text):
        """Create a tooltip for a given widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)

    def sort_files(self):
        """Sort files naturally, handling numbers correctly."""
        if not self.file_paths:
            return
        
        def natural_sort_key(path):
            import re
            # Split the filename into text and number parts
            filename = os.path.basename(path)
            parts = re.split('([0-9]+)', filename.lower())
            # Convert number strings to integers for proper numerical sorting
            parts = [int(part) if part.isdigit() else part for part in parts]
            return parts
        
        self.file_paths.sort(key=natural_sort_key)
        self.update_file_listbox()
        self.status_bar.config(text="Files sorted naturally")

    def clear_files(self):
        """Clear all files from the list."""
        if not self.file_paths:
            return
            
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all files?"):
            self.file_paths.clear()
            self.update_file_listbox()
            self.preview_canvas.delete("all")
            self.status_bar.config(text="All files cleared")

    def add_files(self):
        """Add files to the file list with improved filtering."""
        if self.conversion_type.get() == "jpg_to_pdf":
            filetypes = [("Image files", "*.jpg *.jpeg")]
        else:
            filetypes = [("PDF files", "*.pdf")]
            
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=filetypes + [("All files", "*.*")]
        )
        
        if files:
            # Filter out unsupported files
            valid_extensions = ('.jpg', '.jpeg') if self.conversion_type.get() == "jpg_to_pdf" else ('.pdf',)
            valid_files = [f for f in files if f.lower().endswith(valid_extensions)]
            
            if len(valid_files) != len(files):
                messagebox.showwarning(
                    "Invalid Files",
                    "Some files were skipped because they had unsupported formats."
                )
            
            self.file_paths.extend(valid_files)
            self.update_file_listbox()
            self.status_bar.config(text=f"Added {len(valid_files)} file(s)")

    def remove_selected_files(self):
        """Remove selected files from the file list."""
        selected_index = self.file_listbox.curselection()
        if selected_index:
            self.file_paths.pop(selected_index[0])
            self.update_file_listbox()

    def preview_selected_file(self):
        """Show a preview of the selected file."""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.preview_canvas.delete("all")
            return

        selected_index = selected_indices[0]
        selected_file = self.file_paths[selected_index]
        self.preview_canvas.delete("all")

        try:
            # Center coordinates for preview
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            center_x = canvas_width // 2
            center_y = canvas_height // 2

            if selected_file.lower().endswith(('.jpg', '.jpeg')):
                image = Image.open(selected_file)
                # Maintain aspect ratio
                image.thumbnail((canvas_width, canvas_height))
                self.preview_image = ImageTk.PhotoImage(image)
                self.preview_canvas.create_image(center_x, center_y, image=self.preview_image)
            elif selected_file.lower().endswith('.pdf'):
                pages = convert_from_path(selected_file, first_page=1, last_page=1)
                image = pages[0]
                # Maintain aspect ratio
                image.thumbnail((canvas_width, canvas_height))
                self.preview_image = ImageTk.PhotoImage(image)
                self.preview_canvas.create_image(center_x, center_y, image=self.preview_image)
        except Exception as e:
            self.status_bar.config(text=f"Error previewing file: {str(e)}")

    def update_ui(self):
        """Update the UI based on the conversion type."""
        if self.conversion_type.get() == "jpg_to_pdf":
            self.quality_frame.grid_forget()
        else:
            self.quality_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=20)

    def convert(self):
        """Start conversion based on selected files and type."""
        if not self.file_paths:
            messagebox.showerror("Error", "No files selected")
            return

        if self.conversion_type.get() == "jpg_to_pdf":
            self.jpg_to_pdf()
        else:
            self.pdf_to_jpg()

    def jpg_to_pdf(self):
        """Convert JPG files to a single PDF with compression and A4 size standardization."""
        if not any(file.lower().endswith(('.jpg', '.jpeg')) for file in self.file_paths):
            messagebox.showerror("Error", "No JPG files selected")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        try:
            from PIL import Image
            import io

            # A4 size in pixels at 300 DPI
            A4_WIDTH_PX = int(8.27 * 300)  # 8.27 inches * 300 DPI
            A4_HEIGHT_PX = int(11.69 * 300)  # 11.69 inches * 300 DPI

            # Create a list to store compressed images
            compressed_images = []
            
            # Process each image
            for image_path in self.file_paths:
                if not image_path.lower().endswith(('.jpg', '.jpeg')):
                    continue
                
                # Open image
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Calculate aspect ratios
                    img_aspect = img.width / img.height
                    a4_aspect = A4_WIDTH_PX / A4_HEIGHT_PX
                    
                    # Resize image to fit A4 while maintaining aspect ratio
                    if img_aspect > a4_aspect:  # Image is wider than A4
                        new_width = A4_WIDTH_PX
                        new_height = int(A4_WIDTH_PX / img_aspect)
                    else:  # Image is taller than A4
                        new_height = A4_HEIGHT_PX
                        new_width = int(A4_HEIGHT_PX * img_aspect)
                    
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Create new A4 canvas
                    a4_canvas = Image.new('RGB', (A4_WIDTH_PX, A4_HEIGHT_PX), 'white')
                    
                    # Paste resized image in center of A4
                    paste_x = (A4_WIDTH_PX - new_width) // 2
                    paste_y = (A4_HEIGHT_PX - new_height) // 2
                    a4_canvas.paste(resized_img, (paste_x, paste_y))
                    
                    # Create a bytes buffer
                    img_buffer = io.BytesIO()
                    
                    # Save with compression
                    a4_canvas.save(img_buffer, format='JPEG', quality=90, optimize=True)
                    img_buffer.seek(0)
                    compressed_images.append(img_buffer)

            # Convert compressed images to PDF
            from img2pdf import convert
            with open(output_path, "wb") as f:
                f.write(convert([img.getvalue() for img in compressed_images]))

            # Clean up
            for buffer in compressed_images:
                buffer.close()

            messagebox.showinfo("Success", "PDF created successfully!")
            self.status_bar.config(text="Conversion completed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_bar.config(text="Conversion failed")

    def pdf_to_jpg(self):
        """Convert PDF files to JPG images."""
        if not any(file.lower().endswith('.pdf') for file in self.file_paths):
            messagebox.showerror("Error", "No PDF files selected")
            return

        output_dir = filedialog.askdirectory()
        if not output_dir:
            return

        try:
            # Check if poppler is installed and accessible
            import platform
            if platform.system() == "Windows":
                from pdf2image.exceptions import PDFPageCountError, PDFInfoNotInstalledError
                try:
                    # First try with default poppler path
                    images = convert_from_path(self.file_paths[0], first_page=1, last_page=1)
                except (PDFInfoNotInstalledError, PDFPageCountError) as e:
                    messagebox.showerror("Error", 
                        "Poppler is not installed or not found. Please install poppler and add it to your system PATH.\n"
                        "You can download it from: https://github.com/oschwartz10612/poppler-windows/releases\n"
                        "After installing, restart the application.")
                    return

            for pdf_path in self.file_paths:
                if not pdf_path.lower().endswith('.pdf'):
                    continue
                    
                base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                images = convert_from_path(pdf_path)
                
                for i, image in enumerate(images):
                    output_path = os.path.join(output_dir, f"{base_name}_page_{i+1}.jpg")
                    image.save(output_path, "JPEG", quality=self.quality.get())
            
            messagebox.showinfo("Success", "JPG files created successfully!")
            self.status_bar.config(text="Conversion completed successfully")
        except Exception as e:
            messagebox.showerror("Error", 
                f"An error occurred: {str(e)}\n\n"
                "If you're seeing a poppler error, please install poppler and add it to your system PATH.")
            self.status_bar.config(text="Conversion failed")

    def open_github(self):
        """Open GitHub profile in default browser."""
        import webbrowser
        webbrowser.open("https://github.com/CreatorSpark")

    def rotate_image(self, degrees):
        """Rotate the selected image by specified degrees."""
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "Please select an image to rotate")
            return

        selected_index = selected_indices[0]
        selected_file = self.file_paths[selected_index]
        
        if not selected_file.lower().endswith(('.jpg', '.jpeg')):
            messagebox.showinfo("Info", "Only JPG images can be rotated")
            return
        
        try:
            # Open and rotate the image
            with Image.open(selected_file) as img:
                rotated_img = img.rotate(degrees, expand=True)
                # Save the rotated image, overwriting the original
                rotated_img.save(selected_file, quality=95, optimize=True)
            
            # Update the preview
            self.preview_selected_file()
            self.status_bar.config(text=f"Image rotated {abs(degrees)}° {'clockwise' if degrees > 0 else 'counter-clockwise'}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rotate image: {str(e)}")
            self.status_bar.config(text="Rotation failed")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Apply a sleek theme
    app = ImagePDFConverter(root)
    root.mainloop()
    