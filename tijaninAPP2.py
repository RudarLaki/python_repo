import random
import string
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import json
import os

# ------------------ Similar Map ------------------
similar_map = {
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
    'A': ['4', 'a'], 'B': ['8', 'b'], 'C': ['c', 'G', 'g'], 'D': ['0', 'd'], 'E': ['3', 'e'],
    'F': ['P', 'f'], 'G': ['6', 'C', 'c', 'g'], 'H': ['M', 'h'], 'I': ['1', 'i', 'l', 'L', 'J', 'j'],
    'J': ['L', 'j'], 'K': ['X', 'k'], 'L': ['I', 'i', '1', 'l', 'J', 'j'], 'M': ['N', 'H', 'm'],
    'N': ['M', 'n'], 'O': ['0', 'Q', 'D', 'o'], 'P': ['F', 'R', 'p'], 'Q': ['O', '0', 'q'],
    'R': ['P', 'r'], 'S': ['5', 's', 'Z', 'z'], 'T': ['7', 't'], 'U': ['V', 'u'], 'V': ['U', 'v'],
    'W': ['VV', 'M', 'w'], 'X': ['K', 'x'], 'Y': ['T', 'V', 'y'], 'Z': ['2', 'S', 's', 'z'],
    'a': ['4', 'A'], 'b': ['8', 'B'], 'c': ['C', 'G', 'g'], 'd': ['D', '0'], 'e': ['3', 'E'],
    'f': ['F', 'p'], 'g': ['6', 'G', '9', 'q'], 'h': ['H', 'M'], 'i': ['1', 'I', 'l', 'L', 'j', 'J'],
    'j': ['J', 'I', 'i', 'L', 'l'], 'k': ['K', 'X'], 'l': ['1', 'I', 'i', 'L', 'j', 'J'], 'm': ['M', 'N'],
    'n': ['N', 'M'], 'o': ['0', 'O', 'Q', 'D'], 'p': ['P', 'F', 'R'], 'q': ['Q', '0', 'O', 'g'],
    'r': ['R', 'P'], 's': ['5', 'S', 'Z', 'z'], 't': ['T', '7'], 'u': ['U', 'V'], 'v': ['V', 'U'],
    'w': ['W', 'VV', 'M'], 'x': ['X', 'K'], 'y': ['Y', 'T', 'V'], 'z': ['Z', '2', 'S', 's']
}

# ------------------ Leaderboard Storage ------------------
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Load leaderboard from JSON file"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

def add_to_leaderboard(username, accuracy, avg_time):
    """Add a new score to the leaderboard"""
    leaderboard = load_leaderboard()
    leaderboard.append({
        'username': username,
        'accuracy': accuracy,
        'avg_time': avg_time
    })
    
    # Sort by accuracy (descending), then by username (ascending)
    leaderboard.sort(key=lambda x: (-x['accuracy'], x['username']))
    
    save_leaderboard(leaderboard)

# ------------------ Common Functions ------------------
def get_alphabet(charset):
    if charset == "Letters":
        return string.ascii_letters
    elif charset == "Numbers":
        return string.digits
    return string.ascii_letters + string.digits

def generate_sequence(length, alphabet):
    return [random.choice(alphabet) for _ in range(length)]

def maybe_mutate_sequence(sequence, probability, alphabet):
    if random.random() < probability:
        index = random.randrange(len(sequence))
        original = sequence[index].upper()
        if original in similar_map:
            new_value = random.choice(similar_map[original])
        else:
            new_value = random.choice(alphabet)
            while new_value == sequence[index]:
                new_value = random.choice(alphabet)
        mutated = sequence.copy()
        mutated[index] = new_value
        return mutated, index
    return sequence.copy(), None

# ------------------ Main Menu ------------------
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        
    def setup_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Sequence Challenge Game")
        self.root.geometry("700x550")
        
        main = ttk.Frame(self.root, padding=40)
        main.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(main, text="🎯 Sequence Challenge Game", 
                 font=("Arial", 24, "bold")).pack(pady=(0, 20))
        
        # Mode selection buttons
        button_frame = ttk.Frame(main)
        button_frame.pack(pady=30)
        
        # Challenge Mode button
        challenge_btn = ttk.Button(button_frame, text="🏆 Challenge Mode", 
                                  command=self.start_challenge_mode,
                                  width=25)
        challenge_btn.pack(pady=15)
        
        # Practice Mode button
        practice_btn = ttk.Button(button_frame, text="🎮 Practice Mode", 
                                 command=lambda: PracticeMode(self.root),
                                 width=25)
        practice_btn.pack(pady=15)
        
        # Leaderboard button
        leaderboard_btn = ttk.Button(button_frame, text="🏅 Leaderboard", 
                                     command=lambda: Leaderboard(self.root),
                                     width=25)
        leaderboard_btn.pack(pady=15)
        
        # Instructions
        inst_frame = ttk.LabelFrame(main, text="📝 How to Play", padding=20)
        inst_frame.pack(pady=30, fill="x")
        
        instructions = [
            "• Two sequences will be displayed side by side",
            "• Determine if they are IDENTICAL or DIFFERENT",
            "• Click 'YES (Same)' if they are exactly the SAME",
            "• Click 'NO (Different)' if they have ANY difference",
            "• Try to be both FAST and ACCURATE!",
            "",
            "🏆 Challenge Mode: Timed challenge with increasing difficulty",
            "🎮 Practice Mode: Customize settings and practice freely",
            "🏅 Leaderboard: View top performers"
        ]
        
        for i, inst in enumerate(instructions):
            ttk.Label(inst_frame, text=inst, font=("Arial", 10)).pack(anchor="w", pady=2)
            
        # Footer
        ttk.Label(main, text="Test your visual perception skills! 👁️", 
                 font=("Arial", 11, "italic")).pack(pady=(20, 0))
    
    def start_challenge_mode(self):
        """Prompt for username and start challenge mode"""
        username = simpledialog.askstring(
            "Enter Username", 
            "Enter your username for the leaderboard:",
            parent=self.root
        )
        
        if username and username.strip():
            ChallengeMode(self.root, username.strip())

# ------------------ Practice Mode ------------------
class PracticeMode:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.reset_state()
        
    def reset_state(self):
        self.second_sequence = []
        self.correct_answer = False
        self.changed_index = None
        self.timer_running = False
        self.start_time = 0
        
    def setup_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Practice Mode - Sequence Challenge")
        self.root.geometry("700x600")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_to_menu).pack(side="left")
        
        ttk.Label(header_frame, text="🎮 Practice Mode", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Controls Frame
        controls_frame = ttk.LabelFrame(main, text="Settings", padding=15)
        controls_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        # Row 1 — Length
        ttk.Label(controls_frame, text="Length:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.length_var = tk.StringVar(value="10")
        ttk.Combobox(
            controls_frame,
            textvariable=self.length_var,
            values=["5", "10", "15", "20"],
            state="readonly",
            width=10
        ).grid(row=0, column=1, sticky="w", padx=5)
        
        # Row 2 — Charset
        ttk.Label(controls_frame, text="Charset:").grid(row=0, column=2, sticky="w", pady=5, padx=(20,5))
        self.charset_var = tk.StringVar(value="Alphanumeric")
        ttk.Combobox(
            controls_frame,
            textvariable=self.charset_var,
            values=["Letters", "Numbers", "Alphanumeric"],
            state="readonly",
            width=15
        ).grid(row=0, column=3, sticky="w", padx=5)
        
        # Row 3 — Mutation probability
        ttk.Label(controls_frame, text="Mutation %:").grid(row=1, column=0, sticky="w", pady=15, padx=5)
        self.prob_var = tk.IntVar(value=50)
        prob_scale = ttk.Scale(
            controls_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.prob_var,
            length=200
        )
        prob_scale.grid(row=1, column=1, sticky="w", padx=5)
        
        self.prob_label = ttk.Label(controls_frame, text="50%")
        self.prob_label.grid(row=1, column=2, sticky="w", padx=5)
        self.prob_var.trace("w", lambda *_: self.prob_label.config(text=f"{self.prob_var.get()}%"))
        
        # Generate button
        ttk.Button(controls_frame, text="🔄 Generate New", 
                  command=self.generate, width=15).grid(row=1, column=3, padx=20)
        
        # Timer
        self.timer_label = ttk.Label(controls_frame, text="Time: 0 ms", font=("Arial", 12, "bold"))
        self.timer_label.grid(row=0, column=4, rowspan=2, padx=20)
        
        # Display sequences
        seq_frame = ttk.Frame(main)
        seq_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Label(seq_frame, text="Original Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.original_label = ttk.Label(seq_frame, font=("Courier", 18), relief="solid", 
                                       padding=10, background="white")
        self.original_label.pack(fill="x", pady=(5, 20))
        
        ttk.Label(seq_frame, text="Second Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.seq_text = tk.Text(seq_frame, height=1, font=("Courier", 18), borderwidth=2,
                               relief="solid", bg="white")
        self.seq_text.pack(fill="x", pady=(5, 0))
        self.seq_text.tag_config("changed", background="yellow", foreground="red")
        
        # Guess Buttons
        guess_frame = ttk.Frame(main)
        guess_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        self.yes_btn = ttk.Button(guess_frame, text="✅ YES (Same)",
                                 command=lambda: self.guess(False), 
                                 width=20, style="Accent.TButton")
        self.yes_btn.grid(row=0, column=0, padx=10)
        
        self.no_btn = ttk.Button(guess_frame, text="❌ NO (Different)",
                                command=lambda: self.guess(True), 
                                width=20, style="Accent.TButton")
        self.no_btn.grid(row=0, column=1, padx=10)
        
        # Result
        self.result_label = ttk.Label(main, text="Click 'Generate New' to start", 
                                     font=("Arial", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=4, pady=10)
        
        # Utilities
        util_frame = ttk.Frame(main)
        util_frame.grid(row=5, column=0, columnspan=4, pady=10)
        
        ttk.Button(util_frame, text="📋 Copy Sequence",
                  command=self.copy_to_clipboard, width=15).grid(row=0, column=0, padx=5)
        
        # Generate initial sequence
        self.root.after(100, self.generate)
        
    def start_timer(self):
        self.start_time = time.perf_counter()
        self.timer_running = True
        self.update_timer()
        
    def stop_timer(self):
        self.timer_running = False
        
    def update_timer(self):
        if self.timer_running:
            elapsed = time.perf_counter() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed*1000:.0f} ms")
            self.root.after(50, self.update_timer)
            
    def generate(self):
        self.reset_state()
        length = int(self.length_var.get())
        probability = self.prob_var.get() / 100
        alphabet = get_alphabet(self.charset_var.get())
        
        seq1 = generate_sequence(length, alphabet)
        seq2, self.changed_index = maybe_mutate_sequence(seq1, probability, alphabet)
        self.second_sequence = seq2
        self.correct_answer = self.changed_index is not None
        
        self.original_label.config(text="".join(seq1))
        self.draw_second_sequence(seq2, None)
        self.result_label.config(text="Make your guess", foreground="black")
        self.start_timer()
        
        # Enable buttons
        self.yes_btn.config(state="normal")
        self.no_btn.config(state="normal")
        
    def draw_second_sequence(self, sequence, highlight_index):
        self.seq_text.config(state="normal")
        self.seq_text.delete("1.0", tk.END)
        
        for i, char in enumerate(sequence):
            if i == highlight_index:
                self.seq_text.insert(tk.END, char, "changed")
            else:
                self.seq_text.insert(tk.END, char)
                
        self.seq_text.config(state="disabled")
        
    def guess(self, user_guess):
        if not self.timer_running:
            return
            
        self.stop_timer()
        elapsed = time.perf_counter() - self.start_time
        
        if user_guess == self.correct_answer:
            self.result_label.config(
                text=f"✅ CORRECT — {elapsed*1000:.0f} ms",
                foreground="green"
            )
        else:
            self.result_label.config(
                text=f"❌ WRONG — {'DIFFERENT' if self.correct_answer else 'SAME'} — {elapsed*1000:.0f} ms",
                foreground="red"
            )
            
        # Reveal difference AFTER guess
        if self.changed_index is not None:
            self.draw_second_sequence(self.second_sequence, self.changed_index)
            
        # Disable buttons until next generate
        self.yes_btn.config(state="disabled")
        self.no_btn.config(state="disabled")
            
    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.seq_text.get("1.0", tk.END).strip())
        
    def back_to_menu(self):
        MainMenu(self.root)

# ------------------ Challenge Mode ------------------
class ChallengeMode:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.setup_gui()
        self.reset_game()
        
    def reset_game(self):
        self.levels = [10, 15, 20]
        self.level_index = 0
        self.questions_per_level = 5
        self.current_question = 0
        self.sequence_a = []
        self.sequence_b = []
        self.changed_index = None
        self.correct_answer = False
        self.results = []
        self.probability = 0.5
        self.start_time = 0
        self.total_correct = 0
        self.total_time = 0
        
    def setup_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Challenge Mode - Sequence Challenge")
        self.root.geometry("700x650")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_to_menu).pack(side="left")
        
        ttk.Label(header_frame, text="🏆 Challenge Mode", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(main, text="Progress", padding=15)
        progress_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        self.username_label = ttk.Label(progress_frame,
                                       text=f"Player: {self.username}",
                                       font=("Arial", 11, "bold"))
        self.username_label.pack(pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, 
                                       text="Level 1/3 (Length: 10) - Question 1/5",
                                       font=("Arial", 12, "bold"))
        self.progress_label.pack()
        
        self.stats_label = ttk.Label(progress_frame, 
                                    text="Correct: 0/0 | Avg Time: 0 ms",
                                    font=("Arial", 10))
        self.stats_label.pack(pady=(5, 0))
        
        # Display sequences
        seq_frame = ttk.Frame(main)
        seq_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 20))
        
        ttk.Label(seq_frame, text="Original Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.original_label = ttk.Label(seq_frame, font=("Courier", 18), relief="solid", 
                                       padding=10, background="white")
        self.original_label.pack(fill="x", pady=(5, 20))
        
        ttk.Label(seq_frame, text="Second Sequence:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.seq_text = tk.Text(seq_frame, height=1, font=("Courier", 18), borderwidth=2,
                               relief="solid", bg="white")
        self.seq_text.pack(fill="x", pady=(5, 0))
        self.seq_text.tag_config("changed", background="yellow", foreground="red")
        
        # Guess Buttons
        guess_frame = ttk.Frame(main)
        guess_frame.grid(row=3, column=0, columnspan=4, pady=20)
        
        self.yes_btn = ttk.Button(guess_frame, text="✅ YES (Same)",
                                 command=lambda: self.make_guess(False), 
                                 width=20, style="Accent.TButton")
        self.yes_btn.grid(row=0, column=0, padx=10)
        
        self.no_btn = ttk.Button(guess_frame, text="❌ NO (Different)",
                                command=lambda: self.make_guess(True), 
                                width=20, style="Accent.TButton")
        self.no_btn.grid(row=0, column=1, padx=10)
        
        # Timer and Result
        self.timer_label = ttk.Label(main, text="Time: 0 ms", 
                                    font=("Arial", 14, "bold"))
        self.timer_label.grid(row=4, column=0, columnspan=4, pady=5)
        
        self.result_label = ttk.Label(main, text="Are the sequences the same?", 
                                     font=("Arial", 14))
        self.result_label.grid(row=5, column=0, columnspan=4, pady=10)
        
        # Start the challenge
        self.root.after(100, self.start_next_question)
        
    def start_timer(self):
        self.start_time = time.perf_counter()
        self.update_challenge_timer()
        
    def update_challenge_timer(self):
        if self.start_time > 0:
            elapsed = time.perf_counter() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed*1000:.0f} ms")
            self.root.after(50, self.update_challenge_timer)
        
    def draw_second_sequence(self, sequence, highlight_index):
        self.seq_text.config(state="normal")
        self.seq_text.delete("1.0", tk.END)
        
        for i, char in enumerate(sequence):
            if i == highlight_index:
                self.seq_text.insert(tk.END, char, "changed")
            else:
                self.seq_text.insert(tk.END, char)
                
        self.seq_text.config(state="disabled")
        
    def start_next_question(self):
        if self.current_question >= self.questions_per_level:
            self.level_index += 1
            if self.level_index >= len(self.levels):
                self.show_summary()
                return
            else:
                self.current_question = 0
                
        length = self.levels[self.level_index]
        alphabet = get_alphabet("Alphanumeric")
        seq1 = generate_sequence(length, alphabet)
        seq2, self.changed_index = maybe_mutate_sequence(seq1, self.probability, alphabet)
        
        self.sequence_a = seq1
        self.sequence_b = seq2
        self.correct_answer = self.changed_index is not None
        
        self.original_label.config(text="".join(seq1))
        self.draw_second_sequence(seq2, None)
        
        self.progress_label.config(
            text=f"Level {self.level_index + 1}/3 (Length: {length}) - Question {self.current_question + 1}/{self.questions_per_level}")
        
        # Calculate stats
        total_questions = len(self.results)
        if total_questions > 0:
            avg_time = sum(r[4] for r in self.results) / total_questions
            self.stats_label.config(
                text=f"Correct: {self.total_correct}/{total_questions} | Avg Time: {avg_time*1000:.0f} ms")
        
        self.result_label.config(text="Are the sequences the same?", foreground="black")
        
        # Enable buttons
        self.yes_btn.config(state="normal")
        self.no_btn.config(state="normal")
        
        self.start_timer()
        
    def make_guess(self, user_guess):
        elapsed = time.perf_counter() - self.start_time
        self.start_time = 0  # Stop timer updates
        
        self.results.append((
            "".join(self.sequence_a),
            "".join(self.sequence_b),
            self.correct_answer,
            user_guess,
            elapsed
        ))
        
        if user_guess == self.correct_answer:
            self.result_label.config(
                text=f"✅ Correct — {elapsed*1000:.0f} ms",
                foreground="green"
            )
            self.total_correct += 1
        else:
            self.result_label.config(
                text=f"❌ Wrong — {'Different' if self.correct_answer else 'Same'}",
                foreground="red"
            )
            if self.changed_index is not None:
                self.draw_second_sequence(self.sequence_b, self.changed_index)
        
        self.total_time += elapsed
        
        # Disable buttons
        self.yes_btn.config(state="disabled")
        self.no_btn.config(state="disabled")
        
        # Update stats immediately
        total_questions = len(self.results)
        avg_time = self.total_time / total_questions if total_questions > 0 else 0
        self.stats_label.config(
            text=f"Correct: {self.total_correct}/{total_questions} | Avg Time: {avg_time*1000:.0f} ms")
        
        self.current_question += 1
        self.root.after(1500, self.start_next_question)
        
    def show_summary(self):
        total_questions = len(self.results)
        accuracy = (self.total_correct / total_questions * 100) if total_questions > 0 else 0
        avg_time = (self.total_time / total_questions * 1000) if total_questions > 0 else 0
        
        # Save to leaderboard
        add_to_leaderboard(self.username, round(accuracy, 1), round(avg_time))
        
        summary = (
            f"🏆 Challenge Complete! 🏆\n\n"
            f"Player: {self.username}\n"
            f"Total Questions: {total_questions}\n"
            f"Correct Answers: {self.total_correct}\n"
            f"Accuracy: {accuracy:.1f}%\n"
            f"Average Time: {avg_time:.0f} ms\n\n"
            f"Your score has been saved to the leaderboard!\n\n"
            f"Congratulations! 🎉"
        )
        
        messagebox.showinfo("Challenge Summary", summary)
        self.back_to_menu()
        
    def back_to_menu(self):
        MainMenu(self.root)

# ------------------ Leaderboard ------------------
class Leaderboard:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        
    def setup_gui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Leaderboard - Sequence Challenge")
        self.root.geometry("700x600")
        
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        
        # Title and Back button
        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Button(header_frame, text="← Back to Menu",
                  command=self.back_to_menu).pack(side="left")
        
        ttk.Label(header_frame, text="🏅 Leaderboard", 
                 font=("Arial", 18, "bold")).pack(side="right")
        
        # Load leaderboard data
        leaderboard = load_leaderboard()
        
        if not leaderboard:
            # Empty state
            empty_frame = ttk.Frame(main)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="🏆", font=("Arial", 48)).pack(pady=10)
            ttk.Label(empty_frame, text="No scores yet!", 
                     font=("Arial", 16)).pack(pady=10)
            ttk.Label(empty_frame, text="Complete a challenge to appear here!", 
                     font=("Arial", 12), foreground="gray").pack()
        else:
            # Create table frame with scrollbar
            table_frame = ttk.Frame(main)
            table_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Create scrollbar
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side="right", fill="y")
            
            # Create treeview
            columns = ("Rank", "Username", "Accuracy", "Avg Time")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                               yscrollcommand=scrollbar.set, height=15)
            
            # Configure scrollbar
            scrollbar.config(command=tree.yview)
            
            # Define headings
            tree.heading("Rank", text="Rank")
            tree.heading("Username", text="Username")
            tree.heading("Accuracy", text="Accuracy (%)")
            tree.heading("Avg Time", text="Avg Time (ms)")
            
            # Configure column widths
            tree.column("Rank", width=80, anchor="center")
            tree.column("Username", width=200, anchor="w")
            tree.column("Accuracy", width=150, anchor="center")
            tree.column("Avg Time", width=150, anchor="center")
            
            # Add data
            for i, entry in enumerate(leaderboard, 1):
                rank_text = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else str(i)
                tree.insert("", "end", values=(
                    rank_text,
                    entry['username'],
                    f"{entry['accuracy']:.1f}%",
                    f"{entry['avg_time']:.0f} ms"
                ))
            
            tree.pack(side="left", fill="both", expand=True)
            
            # Clear button
            button_frame = ttk.Frame(main)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="🗑️ Clear Leaderboard",
                      command=self.clear_leaderboard).pack()
    
    def clear_leaderboard(self):
        """Clear all leaderboard entries"""
        if messagebox.askyesno("Clear Leaderboard", 
                              "Are you sure you want to clear all leaderboard entries?"):
            save_leaderboard([])
            # Refresh the display
            self.setup_gui()
            
    def back_to_menu(self):
        MainMenu(self.root)

# ------------------ Main Application ------------------
def main():
    root = tk.Tk()
    root.title("Sequence Challenge Game")
    
    try:
        root.state('zoomed')  # Windows
    except:
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-50}")
    
    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()