import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from converter import FileConverter
import threading

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal File Converter")
        self.geometry("700x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.converter = FileConverter()
        self.selected_files = []
        self.output_folder = ""

        # Main Layout
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Header
        self.header_label = ctk.CTkLabel(self.main_frame, text="File Converter Tool", font=("Roboto Medium", 24))
        self.header_label.grid(row=0, column=0, pady=(20, 10), padx=20)

        # Tabs for different conversions
        self.tab_view = ctk.CTkTabview(self.main_frame, width=600, height=350)
        self.tab_view.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tab_pdf_to_word = self.tab_view.add("PDF to Word")
        self.tab_img_to_pdf = self.tab_view.add("Images to PDF")
        self.tab_word_to_pdf = self.tab_view.add("Word to PDF")

        self.setup_pdf_to_word_tab()
        self.setup_img_to_pdf_tab()
        self.setup_word_to_pdf_tab()

        # Status Footer
        self.status_label = ctk.CTkLabel(self.main_frame, text="Ready", text_color="gray")
        self.status_label.grid(row=3, column=0, pady=10)

    def select_file(self, file_types, label_widget):
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.selected_files = [filename]
            label_widget.configure(text=f"Selected: {os.path.basename(filename)}")
            return filename
        return None

    def select_files(self, file_types, label_widget):
        filenames = filedialog.askopenfilenames(filetypes=file_types)
        if filenames:
            self.selected_files = list(filenames)
            count = len(filenames)
            label_widget.configure(text=f"Selected: {count} file(s)")
            return filenames
        return None

    def save_file(self, file_types, default_ext):
        filename = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=file_types)
        return filename

    def update_status(self, success, message):
        color = "green" if success else "red"
        self.status_label.configure(text=message, text_color=color)
        self.set_loading(False)

    def set_loading(self, loading):
        if loading:
            self.status_label.configure(text="Converting... Please wait.", text_color="orange")
            self.configure(cursor="watch")
        else:
            self.configure(cursor="arrow")

    # --- PDF to Word ---
    def setup_pdf_to_word_tab(self):
        frame = self.tab_pdf_to_word
        frame.grid_columnconfigure(0, weight=1)

        self.pdf_label = ctk.CTkLabel(frame, text="Select a PDF file to convert to Word")
        self.pdf_label.grid(row=0, column=0, pady=20)

        self.btn_select_pdf = ctk.CTkButton(frame, text="Browse PDF", command=self.browse_pdf_ptw)
        self.btn_select_pdf.grid(row=1, column=0, pady=10)

        self.lbl_selected_pdf = ctk.CTkLabel(frame, text="No file selected", text_color="gray")
        self.lbl_selected_pdf.grid(row=2, column=0, pady=5)

        self.btn_convert_ptw = ctk.CTkButton(frame, text="Convert to Word", command=self.convert_pdf_to_word, state="disabled")
        self.btn_convert_ptw.grid(row=3, column=0, pady=20)

    def browse_pdf_ptw(self):
        file = self.select_file([("PDF Files", "*.pdf")], self.lbl_selected_pdf)
        if file:
            self.btn_convert_ptw.configure(state="normal")

    def convert_pdf_to_word(self):
        if not self.selected_files:
            return
        
        output_path = self.save_file([("Word Files", "*.docx")], ".docx")
        if output_path:
            self.set_loading(True)
            threading.Thread(target=self.converter.pdf_to_word, args=(self.selected_files[0], output_path, self.update_status)).start()


    # --- Images to PDF ---
    def setup_img_to_pdf_tab(self):
        frame = self.tab_img_to_pdf
        frame.grid_columnconfigure(0, weight=1)

        self.img_label = ctk.CTkLabel(frame, text="Select Images to convert to a single PDF")
        self.img_label.grid(row=0, column=0, pady=20)

        self.btn_select_img = ctk.CTkButton(frame, text="Browse Images", command=self.browse_img_itp)
        self.btn_select_img.grid(row=1, column=0, pady=10)

        self.lbl_selected_img = ctk.CTkLabel(frame, text="No files selected", text_color="gray")
        self.lbl_selected_img.grid(row=2, column=0, pady=5)

        self.btn_convert_itp = ctk.CTkButton(frame, text="Convert to PDF", command=self.convert_img_to_pdf, state="disabled")
        self.btn_convert_itp.grid(row=3, column=0, pady=20)

    def browse_img_itp(self):
        files = self.select_files([("Images", "*.png;*.jpg;*.jpeg;*.bmp")], self.lbl_selected_img)
        if files:
            self.btn_convert_itp.configure(state="normal")

    def convert_img_to_pdf(self):
        if not self.selected_files:
            return
        
        output_path = self.save_file([("PDF Files", "*.pdf")], ".pdf")
        if output_path:
            self.set_loading(True)
            threading.Thread(target=self.converter.images_to_pdf, args=(self.selected_files, output_path, self.update_status)).start()

    # --- Word to PDF ---
    def setup_word_to_pdf_tab(self):
        frame = self.tab_word_to_pdf
        frame.grid_columnconfigure(0, weight=1)

        self.word_label = ctk.CTkLabel(frame, text="Select a Word file to convert to PDF")
        self.word_label.grid(row=0, column=0, pady=20)

        self.btn_select_word = ctk.CTkButton(frame, text="Browse Word File", command=self.browse_word_wtp)
        self.btn_select_word.grid(row=1, column=0, pady=10)

        self.lbl_selected_word = ctk.CTkLabel(frame, text="No file selected", text_color="gray")
        self.lbl_selected_word.grid(row=2, column=0, pady=5)

        self.btn_convert_wtp = ctk.CTkButton(frame, text="Convert to PDF", command=self.convert_word_to_pdf, state="disabled")
        self.btn_convert_wtp.grid(row=3, column=0, pady=20)

    def browse_word_wtp(self):
        file = self.select_file([("Word Files", "*.docx;*.doc")], self.lbl_selected_word)
        if file:
            self.btn_convert_wtp.configure(state="normal")
            
    def convert_word_to_pdf(self):
        if not self.selected_files:
            return
        
        output_path = self.save_file([("PDF Files", "*.pdf")], ".pdf")
        if output_path:
            self.set_loading(True)
            threading.Thread(target=self.converter.word_to_pdf, args=(self.selected_files[0], output_path, self.update_status)).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
