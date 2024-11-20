import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Create database and table
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi FLOAT,
            fisika FLOAT,
            inggris FLOAT,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()
    conn.close()

def predict_faculty(biologi, fisika, inggris):
    nilai_tertinggi = max(biologi, fisika, inggris)
    if nilai_tertinggi == biologi:
        return "Kedokteran"
    elif nilai_tertinggi == fisika:
        return "Teknik"
    else:
        return "Bahasa"

def submit_nilai():
    try:
        nama = nama_entry.get()
        bio = float(biologi_entry.get())
        fis = float(fisika_entry.get())
        ing = float(inggris_entry.get())

        if bio <= 0 or fis <= 0 or ing <= 0:
            messagebox.showerror("Error", "Nilai tidak boleh negatif atau nol")
            return

        prediksi = predict_faculty(bio, fis, ing)
        
        # Save to database
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nama, bio, fis, ing, prediksi))
        conn.commit()
        conn.close()

        messagebox.showinfo("Hasil", f"Nama: {nama}\nPrediksi Fakultas: {prediksi}")
        
    except ValueError:
        messagebox.showerror("Error", "Input harus berupa angka")

# Create main window
root = tk.Tk()
root.title("Sistem Prediksi Fakultas")
root.geometry("400x300")

# Create database
create_database()

# Create entry fields
tk.Label(root, text="Nama Siswa:").pack(pady=5)
nama_entry = tk.Entry(root)
nama_entry.pack()

tk.Label(root, text="Nilai Biologi:").pack(pady=5)
biologi_entry = tk.Entry(root)
biologi_entry.pack()

tk.Label(root, text="Nilai Fisika:").pack(pady=5)
fisika_entry = tk.Entry(root)
fisika_entry.pack()

tk.Label(root, text="Nilai Inggris:").pack(pady=5)
inggris_entry = tk.Entry(root)
inggris_entry.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_nilai)
submit_button.pack(pady=20)

root.mainloop()