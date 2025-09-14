import tkinter as tk
from tkinter import ttk, messagebox
import math

class TennisGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Classic Tennis Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E8B57")
        
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.player1_points = 0
        self.player2_points = 0
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.game_over = False
        
        self.setup_ui()
        
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#2E8B57")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="🎾 Classic Tennis Game 🎾",
                              font=("Arial", 24, "bold"), bg="#2E8B57", fg="white")
        title_label.pack(pady=10)
        
        self.create_tennis_court(main_frame)
        
        score_frame = tk.Frame(main_frame, bg="#2E8B57")
        score_frame.pack(pady=20)
        
        self.score_display = tk.Frame(score_frame, bg="#F0F8FF", relief=tk.RAISED, bd=3)
        self.score_display.pack(pady=10)
        
        header_frame = tk.Frame(self.score_display, bg="#1E3A8A")
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(header_frame, text="プレイヤー", font=("Arial", 12, "bold"), bg="#1E3A8A", fg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(header_frame, text="セット", font=("Arial", 12, "bold"), bg="#1E3A8A", fg="white").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(header_frame, text="ゲーム", font=("Arial", 12, "bold"), bg="#1E3A8A", fg="white").grid(row=0, column=2, padx=10, pady=5)
        tk.Label(header_frame, text="ポイント", font=("Arial", 12, "bold"), bg="#1E3A8A", fg="white").grid(row=0, column=3, padx=10, pady=5)
        
        self.player1_frame = tk.Frame(self.score_display, bg="#DBEAFE")
        self.player1_frame.pack(fill=tk.X, padx=10, pady=2)
        
        self.player1_name_label = tk.Label(self.player1_frame, text=self.player1_name, 
                                          font=("Arial", 14, "bold"), bg="#DBEAFE", fg="#1E40AF")
        self.player1_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.player1_sets_label = tk.Label(self.player1_frame, text="0", 
                                          font=("Arial", 16, "bold"), bg="#DBEAFE", fg="#1E40AF")
        self.player1_sets_label.grid(row=0, column=1, padx=10)
        
        self.player1_games_label = tk.Label(self.player1_frame, text="0", 
                                           font=("Arial", 16, "bold"), bg="#DBEAFE", fg="#1E40AF")
        self.player1_games_label.grid(row=0, column=2, padx=10)
        
        self.player1_points_label = tk.Label(self.player1_frame, text="0", 
                                            font=("Arial", 16, "bold"), bg="#DBEAFE", fg="#1E40AF")
        self.player1_points_label.grid(row=0, column=3, padx=10)
        
        self.player2_frame = tk.Frame(self.score_display, bg="#FEE2E2")
        self.player2_frame.pack(fill=tk.X, padx=10, pady=2)
        
        self.player2_name_label = tk.Label(self.player2_frame, text=self.player2_name, 
                                          font=("Arial", 14, "bold"), bg="#FEE2E2", fg="#DC2626")
        self.player2_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.player2_sets_label = tk.Label(self.player2_frame, text="0", 
                                          font=("Arial", 16, "bold"), bg="#FEE2E2", fg="#DC2626")
        self.player2_sets_label.grid(row=0, column=1, padx=10)
        
        self.player2_games_label = tk.Label(self.player2_frame, text="0", 
                                           font=("Arial", 16, "bold"), bg="#FEE2E2", fg="#DC2626")
        self.player2_games_label.grid(row=0, column=2, padx=10)
        
        self.player2_points_label = tk.Label(self.player2_frame, text="0", 
                                            font=("Arial", 16, "bold"), bg="#FEE2E2", fg="#DC2626")
        self.player2_points_label.grid(row=0, column=3, padx=10)
        
        button_frame = tk.Frame(main_frame, bg="#2E8B57")
        button_frame.pack(pady=20)
        
        self.player1_button = tk.Button(button_frame, text=f"{self.player1_name}がポイント獲得",
                                       command=lambda: self.point_won_by(1),
                                       bg="#059669", fg="white", font=("Arial", 14, "bold"),
                                       width=20, height=2, relief=tk.RAISED, bd=3,
                                       activebackground="#047857", activeforeground="white")
        self.player1_button.pack(side=tk.LEFT, padx=10)
        
        self.player2_button = tk.Button(button_frame, text=f"{self.player2_name}がポイント獲得",
                                       command=lambda: self.point_won_by(2),
                                       bg="#DC2626", fg="white", font=("Arial", 14, "bold"),
                                       width=20, height=2, relief=tk.RAISED, bd=3,
                                       activebackground="#B91C1C", activeforeground="white")
        self.player2_button.pack(side=tk.LEFT, padx=10)
        
        control_frame = tk.Frame(main_frame, bg="#2E8B57")
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="新しいゲーム", command=self.new_game,
                 bg="#F59E0B", fg="white", font=("Arial", 12, "bold"),
                 relief=tk.RAISED, bd=2, activebackground="#D97706", activeforeground="white").pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="終了", command=self.root.quit,
                 bg="#6B7280", fg="white", font=("Arial", 12, "bold"),
                 relief=tk.RAISED, bd=2, activebackground="#4B5563", activeforeground="white").pack(side=tk.LEFT, padx=5)
        
        self.create_instructions(main_frame)
        
    def create_tennis_court(self, parent):
        court_frame = tk.Frame(parent, bg="#2E8B57")
        court_frame.pack(pady=10)
        
        canvas = tk.Canvas(court_frame, width=400, height=200, bg="#228B22")
        canvas.pack()
        
        canvas.create_rectangle(20, 20, 380, 180, outline="white", width=3)
        canvas.create_line(200, 20, 200, 180, fill="white", width=2)
        canvas.create_line(20, 100, 380, 100, fill="white", width=1)
        canvas.create_rectangle(80, 50, 320, 150, outline="white", width=2)
        canvas.create_line(80, 100, 320, 100, fill="white", width=1)
        
        canvas.create_text(100, 35, text="🎾", font=("Arial", 16), fill="yellow")
        canvas.create_text(300, 165, text="🎾", font=("Arial", 16), fill="yellow")
    
    def create_instructions(self, parent):
        instructions_frame = tk.Frame(parent, bg="#2E8B57")
        instructions_frame.pack(pady=15)
        
        instructions_label = tk.Label(instructions_frame, 
                                    text="📖 ゲーム説明", 
                                    font=("Arial", 16, "bold"), 
                                    bg="#2E8B57", fg="white")
        instructions_label.pack(pady=(0, 10))
        
        instructions_bg = tk.Frame(instructions_frame, bg="#F8F9FA", relief=tk.RAISED, bd=2)
        instructions_bg.pack(padx=20, pady=5)
        
        instructions_text = tk.Text(instructions_bg, 
                                  height=6, width=70, 
                                  font=("Arial", 11),
                                  bg="#F8F9FA", fg="#333333",
                                  relief=tk.FLAT, bd=0,
                                  wrap=tk.WORD, state=tk.DISABLED)
        instructions_text.pack(padx=15, pady=10)
        
        instructions_content = """🎯 ゲームの始め方:
• 各プレイヤーのボタンをクリックしてポイントを獲得
• テニスのスコア: 0 → 15 → 30 → 40 → ゲーム獲得
• 40-40の場合は「Deuce」、そこから2ポイント差で勝利

🏆 勝利条件: 先に2セット獲得したプレイヤーの勝利
🔄 新しいゲーム: いつでも「新しいゲーム」ボタンでリセット可能"""
        
        instructions_text.config(state=tk.NORMAL)
        instructions_text.insert(tk.END, instructions_content)
        instructions_text.config(state=tk.DISABLED)
        
    def get_score_display(self):
        score_map = {0: "0", 1: "15", 2: "30", 3: "40"}
        
        if self.player1_points >= 3 and self.player2_points >= 3:
            if self.player1_points == self.player2_points:
                return "Deuce", "Deuce"
            elif self.player1_points > self.player2_points:
                return "Ad", "40"
            else:
                return "40", "Ad"
        
        p1_score = score_map.get(self.player1_points, "40")
        p2_score = score_map.get(self.player2_points, "40")
        
        return p1_score, p2_score
    
    def point_won_by(self, player):
        if self.game_over:
            return
            
        if player == 1:
            self.player1_points += 1
        else:
            self.player2_points += 1
            
        self.update_display()
        self.check_game_won()
    
    def check_game_won(self):
        if (self.player1_points >= 4 or self.player2_points >= 4):
            if abs(self.player1_points - self.player2_points) >= 2:
                if self.player1_points > self.player2_points:
                    self.player1_games += 1
                    winner_name = self.player1_name
                else:
                    self.player2_games += 1
                    winner_name = self.player2_name
                
                self.player1_points = 0
                self.player2_points = 0
                
                messagebox.showinfo("ゲーム終了", f"{winner_name}がゲームを獲得！")
                self.update_display()
                self.check_set_won()
    
    def check_set_won(self):
        if (self.player1_games >= 6 or self.player2_games >= 6):
            if abs(self.player1_games - self.player2_games) >= 2:
                if self.player1_games > self.player2_games:
                    self.player1_sets += 1
                    winner_name = self.player1_name
                else:
                    self.player2_sets += 1
                    winner_name = self.player2_name
                
                messagebox.showinfo("セット終了", f"{winner_name}がセットを獲得！")
                self.player1_games = 0
                self.player2_games = 0
                self.update_display()
                self.check_match_won()
    
    def check_match_won(self):
        if self.player1_sets >= 2 or self.player2_sets >= 2:
            winner = self.player1_name if self.player1_sets > self.player2_sets else self.player2_name
            messagebox.showinfo("マッチ終了", f"🏆 {winner}がマッチに勝利しました！ 🏆")
            self.game_over = True
            self.player1_button.config(state="disabled")
            self.player2_button.config(state="disabled")
    
    def update_display(self):
        self.player1_name_label.config(text=self.player1_name)
        self.player2_name_label.config(text=self.player2_name)
        self.player1_button.config(text=f"{self.player1_name}がポイント獲得")
        self.player2_button.config(text=f"{self.player2_name}がポイント獲得")
        
        p1_points, p2_points = self.get_score_display()
        
        self.player1_sets_label.config(text=str(self.player1_sets))
        self.player1_games_label.config(text=str(self.player1_games))
        self.player1_points_label.config(text=p1_points)
        
        self.player2_sets_label.config(text=str(self.player2_sets))
        self.player2_games_label.config(text=str(self.player2_games))
        self.player2_points_label.config(text=p2_points)
        
        if self.game_over:
            self.player1_button.config(state="disabled")
            self.player2_button.config(state="disabled")
    
    def new_game(self):
        self.player1_points = 0
        self.player2_points = 0
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.game_over = False
        
        self.player1_button.config(state="normal")
        self.player2_button.config(state="normal")
        
        self.update_display()


def main():
    root = tk.Tk()
    TennisGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()