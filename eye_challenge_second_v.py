import random
import string
import tkinter as tk
from tkinter import ttk
import time


# ------------------ Logic ------------------


def get_alphabet():
    mode = charset_var.get()
    if mode == "Letters":
        return string.ascii_letters
    elif mode == "Numbers":
        return string.digits
    return string.ascii_letters + string.digits

def generate_sequence(length, alphabet):
    return [random.choice(alphabet) for _ in range(length)]

def maybe_mutate_sequence(sequence, probability, alphabet):
    if random.random() < probability:
        index = random.randrange(len(sequence))
        original = sequence[index].upper()  # map uses uppercase keys
        if original in similar_map:
            new_value = random.choice(similar_map[original])
        else:
            # fallback: pick a random character from alphabet
            if alphabet is None:
                alphabet = string.ascii_letters + string.digits
            new_value = random.choice(alphabet)
            while new_value == sequence[index]:
                new_value = random.choice(alphabet)

        mutated = sequence.copy()
        mutated[index] = new_value
        return mutated, index

    return sequence.copy(), None

# ------------------ Timer ------------------

def start_timer():
    global start_time, timer_running
    start_time = time.perf_counter()
    timer_running = True
    update_timer()

def stop_timer():
    global timer_running
    timer_running = False

def update_timer():
    if timer_running:
        elapsed = time.perf_counter() - start_time
        timer_label.config(text=f"Time: {elapsed*1000:.0f} ms")
        root.after(50, update_timer)

# ------------------ GUI Actions ------------------

def generate():
    global correct_answer, changed_index, second_sequence
    length = int(length_var.get())
    probability = prob_var.get() / 100
    alphabet = get_alphabet()

    seq1 = generate_sequence(length, alphabet)
    seq2, changed_index = maybe_mutate_sequence(seq1, probability, alphabet)
    second_sequence = seq2

    correct_answer = changed_index is not None

    original_label.config(text="".join(seq1))
    draw_second_sequence(seq2, None)

    result_label.config(text="Make your guess", foreground="black")

    start_timer()

def draw_second_sequence(sequence, highlight_index):
    seq_text.config(state="normal")
    seq_text.delete("1.0", tk.END)

    for i, char in enumerate(sequence):
        if i == highlight_index:
            seq_text.insert(tk.END, char, "changed")
        else:
            seq_text.insert(tk.END, char)

    seq_text.config(state="disabled")

    seq_text.tag_config("changed", background="yellow", foreground="red")

def guess(user_guess):
    stop_timer()
    elapsed = time.perf_counter() - start_time

    if user_guess == correct_answer:
        result_label.config(
            text=f"✔ CORRECT — {elapsed*1000:.0f} ms",
            foreground="green"
        )
    else:
        result_label.config(
            text=f"✖ WRONG — {'DIFFERENT' if correct_answer else 'SAME'} — {elapsed*1000:.0f} ms",
            foreground="red"
        )

    # 🔥 Reveal difference AFTER guess
    if changed_index is not None:
        draw_second_sequence(second_sequence, changed_index)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(seq_text.get("1.0", tk.END).strip())

# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title("Sequence Guessing Game")
root.geometry("680x460")
root.resizable(False, False)

main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

# Controls
ttk.Label(main, text="Length:").grid(row=0, column=0, sticky="w")
length_var = tk.StringVar(value="10")
# Row 0 — Length
ttk.Label(main, text="Length:").grid(row=0, column=0, sticky="w", pady=5)
length_var = tk.StringVar(value="10")
ttk.Combobox(
    main,
    textvariable=length_var,
    values=["5", "10", "15", "20"],
    state="readonly",
    width=10
).grid(row=0, column=1, sticky="w")

# Row 1 — Charset
ttk.Label(main, text="Charset:").grid(row=1, column=0, sticky="w", pady=5)
charset_var = tk.StringVar(value="Alphanumeric")
ttk.Combobox(
    main,
    textvariable=charset_var,
    values=["Letters", "Numbers", "Alphanumeric"],
    state="readonly",
    width=15
).grid(row=1, column=1, sticky="w")

# Row 2 — Mutation probability
ttk.Label(main, text="Mutation probability:").grid(row=2, column=0, sticky="w", pady=5)
prob_var = tk.IntVar(value=50)
ttk.Scale(
    main,
    from_=0,
    to=100,
    orient="horizontal",
    variable=prob_var
).grid(row=2, column=1, sticky="we")


ttk.Button(main, text="Generate", command=generate).grid(row=3, column=0, pady=10)


# Timer
timer_label = ttk.Label(main, text="Time: 0 ms", font=("Arial", 12, "bold"))
timer_label.grid(row=3, column=2, columnspan=2)

# Display
ttk.Label(main, text="Original Sequence:").grid(row=4, column=0, columnspan=4, sticky="w")
original_label = ttk.Label(main, font=("Courier", 16))
original_label.grid(row=5, column=0, columnspan=4, sticky="w")

ttk.Label(main, text="Second Sequence:").grid(row=6, column=0, columnspan=4, sticky="w", pady=(10, 0))
seq_text = tk.Text(main, height=1, font=("Courier", 16), borderwidth=0)
seq_text.grid(row=7, column=0, columnspan=4, sticky="w")
# seq_text.tag_config("changed", foreground="red")

# Guess Buttons
guess_frame = ttk.Frame(main)
guess_frame.grid(row=8, column=0, columnspan=4, pady=20)

ttk.Button(guess_frame, text="YES (Same)",
           command=lambda: guess(False), width=18).grid(row=0, column=0, padx=10)
ttk.Button(guess_frame, text="NO (Different)",
           command=lambda: guess(True), width=18).grid(row=0, column=1, padx=10)

# Result
result_label = ttk.Label(main, text="", font=("Arial", 14, "bold"))
result_label.grid(row=9, column=0, columnspan=4)

# Utilities
ttk.Button(main, text="Copy second sequence",
           command=copy_to_clipboard).grid(row=10, column=0, pady=10)

# State
similar_map = {
    # Numbers
    '0': ['O', 'o', 'D', 'Q'],
    '1': ['I', 'i', 'l', 'L', 'J', 'j'],
    '2': ['Z', 'z'],
    '3': ['E', 'e'],
    '4': ['A', 'a'],
    '5': ['S', 's'],
    '6': ['G', 'g'],
    '7': ['T', 't', 'Y', 'y'],
    '8': ['B', 'b'],
    '9': ['g', 'q', 'Q'],

    # Uppercase letters
    'A': ['4', 'a'],
    'B': ['8', 'b'],
    'C': ['c', 'G', 'g'],
    'D': ['0', 'd'],
    'E': ['3', 'e'],
    'F': ['P', 'f'],
    'G': ['6', 'C', 'c', 'g'],
    'H': ['M', 'h'],
    'I': ['1', 'i', 'l', 'L', 'J', 'j'],
    'J': ['L', 'j'],
    'K': ['X', 'k'],
    'L': ['I', 'i', '1', 'l', 'J', 'j'],
    'M': ['N', 'H', 'm'],
    'N': ['M', 'n'],
    'O': ['0', 'Q', 'D', 'o'],
    'P': ['F', 'R', 'p'],
    'Q': ['O', '0', 'q'],
    'R': ['P', 'r'],
    'S': ['5', 's', 'Z', 'z'],
    'T': ['7', 't'],
    'U': ['V', 'u'],
    'V': ['U', 'v'],
    'W': ['VV', 'M', 'w'],
    'X': ['K', 'x'],
    'Y': ['T', 'V', 'y'],
    'Z': ['2', 'S', 's', 'z'],

    # Lowercase letters
    'a': ['4', 'A'],
    'b': ['8', 'B'],
    'c': ['C', 'G', 'g'],
    'd': ['D', '0'],
    'e': ['3', 'E'],
    'f': ['F', 'p'],
    'g': ['6', 'G', '9', 'q'],
    'h': ['H', 'M'],
    'i': ['1', 'I', 'l', 'L', 'j', 'J'],
    'j': ['J', 'I', 'i', 'L', 'l'],
    'k': ['K', 'X'],
    'l': ['1', 'I', 'i', 'L', 'j', 'J'],
    'm': ['M', 'N'],
    'n': ['N', 'M'],
    'o': ['0', 'O', 'Q', 'D'],
    'p': ['P', 'F', 'R'],
    'q': ['Q', '0', 'O', 'g'],
    'r': ['R', 'P'],
    's': ['5', 'S', 'Z', 'z'],
    't': ['T', '7'],
    'u': ['U', 'V'],
    'v': ['V', 'U'],
    'w': ['W', 'VV', 'M'],
    'x': ['X', 'K'],
    'y': ['Y', 'T', 'V'],
    'z': ['Z', '2', 'S', 's']
}


second_sequence = []
correct_answer = False
changed_index = None
timer_running = False
start_time = 0


root.mainloop()