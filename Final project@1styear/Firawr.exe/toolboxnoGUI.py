"""
╔══════════════════════════════════════════════════════════════╗
║                  🧰 PYTHON TOOLBOX v1.0                      ║
║         A unified hub for all your utility scripts           ║
╚══════════════════════════════════════════════════════════════╝

HOW TO ADD MORE TOOLS:
  1. Define a function:  def run_my_tool(): ...
  2. Add an entry to TOOLS dict at the bottom:
        "My Tool": {"desc": "Short description", "fn": run_my_tool, "icon": "🔧"}

Built-in tools (5):
  1. 🎙  Speech Recorder     – record mic audio to RAW/WAV/AIFF/FLAC
  2. 🎵  Audio Converter     – convert audio files between formats (via pydub)
  3. 💰  Budget Tracker      – Tkinter GUI for personal finance (SQLite)
  4. 🔢  Calculator          – arithmetic, factorial, complex math, binomial
  5. 📁  File Organizer      – sort a directory's files into category folders
"""

import os
import sys
import time
import shutil
import logging
import argparse
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ─────────────────────────────────────────────────────────────────────────────
#  TOOL 1 – Speech Recorder
# ─────────────────────────────────────────────────────────────────────────────

def run_speech_recorder():
    """Record audio from the microphone and save in multiple formats."""
    try:
        import speech_recognition as sr
    except ImportError:
        print("  ✗  Missing dependency: pip install SpeechRecognition pyaudio")
        return

    r = sr.Recognizer()
    print("\n  🎙  Speak now – recording from microphone…")
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
    except Exception as e:
        print(f"  ✗  Microphone error: {e}")
        return

    saved = []
    formats = {
        "microphone-results.raw":  audio.get_raw_data,
        "microphone-results.wav":  audio.get_wav_data,
        "microphone-results.aiff": audio.get_aiff_data,
        "microphone-results.flac": audio.get_flac_data,
    }
    for fname, getter in formats.items():
        with open(fname, "wb") as f:
            f.write(getter())
        saved.append(fname)

    print("\n  ✓  Audio saved to:")
    for s in saved:
        print(f"     • {s}")


# ─────────────────────────────────────────────────────────────────────────────
#  TOOL 2 – Audio Converter
# ─────────────────────────────────────────────────────────────────────────────

def run_audio_converter():
    """Convert an audio file from one format to another using pydub."""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("  ✗  Missing dependency: pip install pydub")
        return

    filename = input("\n  Enter path to audio file: ").strip()
    if not os.path.isfile(filename):
        print(f"  ✗  File not found: {filename}")
        return

    frm = input("  Target format (e.g. mp3, wav, flac, ogg): ").strip().lower()
    fileext = filename.rsplit(".", 1)[-1].lower()

    if filename.endswith(f".{frm}"):
        print("  ⚠  File is already in that format.")
        return

    filepath = os.path.abspath(filename)
    filebase = os.path.basename(filename)
    newbase  = filebase[:-(len(fileext))] + frm
    newpath  = os.path.join(os.path.dirname(filepath), newbase)

    print(f"\n  Converting {fileext} → {frm} …")
    try:
        track = AudioSegment.from_file(filename, fileext)
        track.export(newpath, format=frm)
        print(f"  ✓  Saved to: {newpath}")
    except Exception as e:
        print(f"  ✗  Conversion failed: {e}")


# ─────────────────────────────────────────────────────────────────────────────
#  TOOL 3 – Budget Tracker
# ─────────────────────────────────────────────────────────────────────────────

def run_budget_tracker():
    """Open a Tkinter GUI for tracking personal income and expenses."""
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL)""")
    conn.commit()

    root = tk.Tk()
    root.title("💰 Personal Budget Manager")
    root.resizable(False, False)

    # ── Input row ──────────────────────────────────────────────────────────
    frame_top = tk.LabelFrame(root, text=" Add Transaction ", padx=8, pady=8)
    frame_top.pack(padx=10, pady=(10, 4), fill="x")

    tk.Label(frame_top, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
    date_entry = tk.Entry(frame_top, width=14)
    date_entry.grid(row=0, column=1, padx=4, pady=4)

    tk.Label(frame_top, text="Description:").grid(row=0, column=2, sticky="e")
    desc_entry = tk.Entry(frame_top, width=22)
    desc_entry.grid(row=0, column=3, padx=4, pady=4)

    tk.Label(frame_top, text="Amount ($):").grid(row=0, column=4, sticky="e")
    amt_entry = tk.Entry(frame_top, width=10)
    amt_entry.grid(row=0, column=5, padx=4, pady=4)

    tk.Label(frame_top, text="Category:").grid(row=0, column=6, sticky="e")
    cat_cb = ttk.Combobox(frame_top, width=14,
                          values=["Income","Housing","Food","Transportation",
                                  "Utilities","Entertainment","Health","Other"],
                          state="readonly")
    cat_cb.grid(row=0, column=7, padx=4, pady=4)

    # ── List ───────────────────────────────────────────────────────────────
    frame_mid = tk.LabelFrame(root, text=" Transactions ", padx=8, pady=8)
    frame_mid.pack(padx=10, pady=4, fill="both", expand=True)

    cols = ("ID", "Date", "Description", "Amount", "Category")
    tree = ttk.Treeview(frame_mid, columns=cols, show="headings", height=14)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col not in ("ID",) else 40)
    scroll = ttk.Scrollbar(frame_mid, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # ── Balance ────────────────────────────────────────────────────────────
    frame_bot = tk.Frame(root)
    frame_bot.pack(padx=10, pady=(4, 10), fill="x")

    bal_label = tk.Label(frame_bot, text="Balance: $0.00",
                         font=("TkDefaultFont", 12, "bold"))
    bal_label.pack(side="left")

    def refresh():
        for row in tree.get_children():
            tree.delete(row)
        c.execute("SELECT * FROM transactions ORDER BY date DESC")
        for row in c.fetchall():
            tree.insert("", "end", values=row)
        c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions")
        total = c.fetchone()[0]
        c.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE amount<0")
        expense = abs(c.fetchone()[0])
        bal_label.config(text=f"Balance: ${total - expense:.2f}  |  "
                              f"Expenses: ${expense:.2f}")

    def add_tx():
        d, desc, amt, cat = (date_entry.get().strip(), desc_entry.get().strip(),
                              amt_entry.get().strip(), cat_cb.get())
        if not all([d, desc, amt, cat]):
            messagebox.showwarning("Missing fields", "Please fill in all fields.")
            return
        try:
            amt_f = float(amt)
        except ValueError:
            messagebox.showerror("Invalid amount", "Amount must be a number.")
            return
        c.execute("INSERT INTO transactions (date,description,amount,category) "
                  "VALUES (?,?,?,?)", (d, desc, amt_f, cat))
        conn.commit()
        for w in (date_entry, desc_entry, amt_entry): w.delete(0, tk.END)
        cat_cb.set("")
        refresh()

    def del_tx():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a transaction to delete.")
            return
        tx_id = tree.item(sel[0])["values"][0]
        c.execute("DELETE FROM transactions WHERE id=?", (tx_id,))
        conn.commit()
        refresh()

    tk.Button(frame_top, text="✚ Add", command=add_tx,
              bg="#2ecc71", fg="white").grid(row=0, column=8, padx=6)
    tk.Button(frame_bot, text="✖ Delete selected", command=del_tx,
              bg="#e74c3c", fg="white").pack(side="right")

    refresh()
    root.mainloop()


# ─────────────────────────────────────────────────────────────────────────────
#  TOOL 4 – Calculator
# ─────────────────────────────────────────────────────────────────────────────

def _factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def run_calculator():
    """Interactive CLI calculator with basic, statistical, and complex operations."""

    def addition():
        nums = list(map(float, input("  Numbers (space-separated): ").split()))
        return sum(nums)

    def subtraction():
        a = float(input("  First number:  "))
        b = float(input("  Second number: "))
        return a - b

    def multiplication():
        nums = list(map(float, input("  Numbers (space-separated): ").split()))
        r = 1
        for n in nums: r *= n
        return r

    def division():
        a = float(input("  First number:  "))
        b = float(input("  Second number: "))
        if b == 0:
            print("  ✗  Division by zero.")
            return None
        return a / b

    def average():
        nums = list(map(float, input("  Numbers (space-separated): ").split()))
        return sum(nums) / len(nums)

    def factorial():
        n = int(input("  Enter integer ≥ 0: "))
        if n < 0:
            print("  ✗  Must be non-negative.")
            return None
        return _factorial(n)

    def binomial():
        n = int(input("  n: "))
        k = int(input("  k: "))
        if n < k:
            print("  ✗  n must be ≥ k.")
            return None
        return _factorial(n) // (_factorial(k) * _factorial(n - k))

    def complex_arith():
        print("  [1] Add  [2] Subtract  [3] Multiply  [4] Divide")
        op = input("  Choice: ").strip()
        a_r = float(input("  First  – real part:      "))
        a_i = float(input("  First  – imaginary part: "))
        b_r = float(input("  Second – real part:      "))
        b_i = float(input("  Second – imaginary part: "))
        a, b = complex(a_r, a_i), complex(b_r, b_i)
        ops = {"1": a + b, "2": a - b, "3": a * b}
        if op == "4":
            if b == 0:
                print("  ✗  Division by zero.")
                return None
            return a / b
        return ops.get(op)

    menu = [
        ("Addition",          addition),
        ("Subtraction",       subtraction),
        ("Multiplication",    multiplication),
        ("Division",          division),
        ("Average",           average),
        ("Factorial",         factorial),
        ("Binomial C(n,k)",   binomial),
        ("Complex Arithmetic",complex_arith),
    ]

    while True:
        print("\n  ┌─ Calculator ─────────────────────────────")
        for i, (name, _) in enumerate(menu, 1):
            print(f"  │  [{i}] {name}")
        print("  │  [0] Back to main menu")
        print("  └──────────────────────────────────────────")
        c = input("  Choice: ").strip()
        if c == "0":
            break
        try:
            idx = int(c) - 1
            if 0 <= idx < len(menu):
                result = menu[idx][1]()
                if result is not None:
                    print(f"\n  ✓  Result: {result}")
            else:
                print("  ✗  Invalid option.")
        except (ValueError, ZeroDivisionError) as e:
            print(f"  ✗  Error: {e}")
        input("\n  [Enter to continue]")


# ─────────────────────────────────────────────────────────────────────────────
#  TOOL 5 – File Organizer
# ─────────────────────────────────────────────────────────────────────────────

CATEGORIES = {
    "Music":       (".mp3",".wav",".flac",".m4a",".aac",".ogg",".oga",".wma",".mid"),
    "Videos":      (".mp4",".avi",".mkv",".mpeg",".wmv",".vob",".flv",".mov",".3gp",".webm"),
    "Source Files":(".py",".c",".cpp",".java",".js",".cs",".html",".css",".php",".json",".xml",".sql",".db"),
    "Executables": (".exe",".msi",".sh",".bat",".apk",".jar",".deb",".run",".bin",".dmg",".iso"),
    "Pictures":    (".jpg",".jpeg",".png",".gif",".bmp",".svg",".webp",".psd",".ai",".ico"),
    "Documents":   (".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".txt",".md",".odt",".csv",".rtf"),
    "Compressed":  (".zip",".rar",".tar",".gz",".7z",".bz2",".xz",".z",".lz"),
    "Torrents":    (".torrent",),
}

def run_file_organizer():
    """Organize a directory by moving files into category sub-folders."""
    directory = input("\n  Enter directory path to organize: ").strip()

    if not os.path.isdir(directory):
        print(f"  ✗  Not a valid directory: {directory}")
        return
    if not os.listdir(directory):
        print("  ✗  Directory is empty.")
        return
    if not os.access(directory, os.W_OK):
        print("  ✗  Directory is not writable.")
        return

    verbose = input("  Enable verbose output? [y/N]: ").strip().lower() == "y"
    moved = 0

    for category, exts in CATEGORIES.items():
        matches = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
            and os.path.splitext(f)[1].lower() in exts
        ]
        if not matches:
            continue

        dest_folder = os.path.join(directory, category)
        os.makedirs(dest_folder, exist_ok=True)
        if verbose:
            print(f"  📂  {category}/")

        for fname in matches:
            src = os.path.join(directory, fname)
            dst = os.path.join(dest_folder, fname)
            shutil.move(src, dst)
            moved += 1
            if verbose:
                print(f"       ↳ {fname}")

    print(f"\n  ✓  Done! {moved} file(s) organized.")


# ─────────────────────────────────────────────────────────────────────────────
#  ★ TOOL REGISTRY – add your own tools here ★
# ─────────────────────────────────────────────────────────────────────────────
#
#  To add a new tool:
#    1. Define a function anywhere above:   def run_my_tool(): ...
#    2. Append an entry below:
#          "My Tool Name": {"desc": "One-line description", "fn": run_my_tool, "icon": "🔧"},
#
TOOLS = {
    "Speech Recorder":  {"desc": "Record mic audio → RAW / WAV / AIFF / FLAC",  "fn": run_speech_recorder,  "icon": "🎙 "},
    "Audio Converter":  {"desc": "Convert audio files between formats (pydub)",  "fn": run_audio_converter,  "icon": "🎵"},
    "Budget Tracker":   {"desc": "Tkinter GUI – track income & expenses (SQLite)","fn": run_budget_tracker,   "icon": "💰"},
    "Calculator":       {"desc": "Arithmetic, factorial, complex math, binomial", "fn": run_calculator,       "icon": "🔢"},
    "File Organizer":   {"desc": "Sort a directory's files into category folders", "fn": run_file_organizer,   "icon": "📁"},
    # ── Add more tools below this line ──────────────────────────────────────
    # "My Tool": {"desc": "What it does", "fn": run_my_tool, "icon": "🔧"},
}


# ─────────────────────────────────────────────────────────────────────────────
#  Main menu
# ─────────────────────────────────────────────────────────────────────────────

BANNER = r"""
  ╔══════════════════════════════════════════════════════╗
  ║           🧰  P Y T H O N   T O O L B O X           ║
  ╚══════════════════════════════════════════════════════╝"""

def main():
    tool_list = list(TOOLS.items())   # preserves insertion order (Python 3.7+)

    while True:
        os.system("cls||clear")
        print(BANNER)
        print(f"  {'#':<4} {'Tool':<22} Description")
        print("  " + "─" * 60)
        for i, (name, meta) in enumerate(tool_list, 1):
            print(f"  {i:<4} {meta['icon']} {name:<20} {meta['desc']}")
        print("  " + "─" * 60)
        print("  [0]  Exit\n")

        choice = input("  Select a tool: ").strip()

        if choice == "0":
            print("\n  Goodbye! 👋\n")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tool_list):
                name, meta = tool_list[idx]
                os.system("cls||clear")
                print(f"\n  {meta['icon']}  {name}\n  {'─' * 50}")
                meta["fn"]()
                input("\n  [Enter to return to menu]")
            else:
                print("  ✗  Invalid selection.")
                time.sleep(1)
        except ValueError:
            print("  ✗  Please enter a number.")
            time.sleep(1)


if __name__ == "__main__":
    main()