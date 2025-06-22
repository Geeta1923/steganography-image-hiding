import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# -------- Core LSB Logic --------

def encode_lsb(img_path, message, output_path='encoded_image.png'):
    image = Image.open(img_path)
    binary_msg = ''.join([format(ord(char), '08b') for char in message]) + '11111110'  # EOF
    pixels = list(image.getdata())
    data_index = 0
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_msg):
            r = r & ~1 | int(binary_msg[data_index])
            data_index += 1
        if data_index < len(binary_msg):
            g = g & ~1 | int(binary_msg[data_index])
            data_index += 1
        if data_index < len(binary_msg):
            b = b & ~1 | int(binary_msg[data_index])
            data_index += 1
        new_pixels.append((r, g, b))

    image.putdata(new_pixels)
    image.save(output_path)
    return output_path

def decode_lsb(img_path):
    image = Image.open(img_path)
    pixels = list(image.getdata())
    binary_data = ''

    for pixel in pixels:
        for channel in pixel[:3]:
            binary_data += str(channel & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_msg = ''
    for byte in all_bytes:
        if byte == '11111110':  # EOF
            break
        decoded_msg += chr(int(byte, 2))
    return decoded_msg

# -------- GUI Code --------

class StegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("600x400")
        self.root.config(bg="#e6f2ff")

        self.image_path = ""

        # Title
        tk.Label(root, text="Steganography - Hide Text in Image", font=("Helvetica", 16, "bold"), bg="#e6f2ff").pack(pady=10)

        # Upload button
        tk.Button(root, text="📂 Upload Image", command=self.upload_image, bg="#b3d9ff", font=("Helvetica", 12)).pack()

        # Message input
        tk.Label(root, text="Secret Message:", bg="#e6f2ff").pack(pady=(20, 5))
        self.msg_entry = tk.Text(root, height=4, width=50)
        self.msg_entry.pack()

        # Encode / Decode buttons
        tk.Button(root, text="🔐 Encode", command=self.encode_message, bg="#99ccff", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(root, text="🔍 Decode", command=self.decode_message, bg="#80bfff", font=("Helvetica", 12)).pack()

        # Output
        self.output_label = tk.Label(root, text="", bg="#e6f2ff", fg="green", wraplength=500)
        self.output_label.pack(pady=10)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if self.image_path:
            messagebox.showinfo("Image Selected", f"Image path:\n{self.image_path}")

    def encode_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        msg = self.msg_entry.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Empty Message", "Please type a message to encode.")
            return
        try:
            output_path = encode_lsb(self.image_path, msg)
            messagebox.showinfo("Success", f"Message encoded and saved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_message(self):
        if not self.image_path:
            messagebox.showwarning("No Image", "Please upload an image first.")
            return
        try:
            message = decode_lsb(self.image_path)
            self.output_label.config(text="🔓 Hidden Message: " + message)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# -------- Main --------

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoGUI(root)
    root.mainloop()
