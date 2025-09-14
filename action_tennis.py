import tkinter as tk
import random

class ActionTennisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Tennis Game - Player vs CPU")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1B5E20")
        self.root.resizable(False, False)
        
        # Game constants
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 500
        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 80
        self.BALL_SIZE = 12
        self.PLAYER_SPEED = 8
        self.CPU_SPEED = 6
        self.BALL_SPEED = 6
        
        # Game state
        self.running = False
        self.player_score = 0
        self.cpu_score = 0
        self.game_paused = False
        
        # Smash system variables
        self.player_prev_x = 0
        self.player_prev_y = 0
        self.player_velocity_x = 0
        self.player_velocity_y = 0
        self.cpu_prev_x = 0
        self.cpu_prev_y = 0
        self.cpu_velocity_x = 0
        self.cpu_velocity_y = 0
        self.player_charge_time = 0
        self.cpu_charge_time = 0
        self.player_smash_count = 0
        self.cpu_smash_count = 0
        self.smash_effects = []
        self.ball_trail = []
        
        # Player paddle (left side)
        self.player_x = 20
        self.player_y = self.CANVAS_HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        
        # CPU paddle (right side)
        self.cpu_x = self.CANVAS_WIDTH - 30
        self.cpu_y = self.CANVAS_HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        
        # Ball
        self.ball_x = self.CANVAS_WIDTH // 2
        self.ball_y = self.CANVAS_HEIGHT // 2
        self.ball_dx = self.BALL_SPEED
        self.ball_dy = random.choice([-3, -2, -1, 1, 2, 3])
        self.ball_speed_multiplier = 1.0
        self.ball_smash_effect = 0
        self.ball_color = "#FFEB3B"
        
        # Key states
        self.keys_pressed = set()
        
        self.setup_ui()
        self.bind_keys()
        self.reset_ball()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#1B5E20")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🎾 Action Tennis vs CPU 🎾",
                              font=("Arial", 24, "bold"), bg="#1B5E20", fg="white")
        title_label.pack(pady=10)
        
        # Canvas for game
        self.canvas = tk.Canvas(main_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                               bg="#2E7D32", bd=3, relief=tk.RAISED)
        self.canvas.pack(pady=20)
        
        # Draw court
        self.draw_court()
        
        # Score display
        score_frame = tk.Frame(main_frame, bg="#1B5E20")
        score_frame.pack(pady=10)
        
        self.score_label = tk.Label(score_frame, text=f"Player: {self.player_score}  |  CPU: {self.cpu_score}",
                                   font=("Arial", 20, "bold"), bg="#1B5E20", fg="white")
        self.score_label.pack()
        
        # Smash stats display
        self.smash_label = tk.Label(score_frame, text=f"Player Smashes: {self.player_smash_count}  |  CPU Smashes: {self.cpu_smash_count}",
                                   font=("Arial", 12, "bold"), bg="#1B5E20", fg="#FFD700")
        self.smash_label.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg="#1B5E20")
        button_frame.pack(pady=15)
        
        self.start_button = tk.Button(button_frame, text="ゲーム開始", command=self.start_game,
                                     bg="#4CAF50", fg="black", font=("Arial", 14, "bold"),
                                     width=12, height=2, relief=tk.RAISED, bd=3,
                                     activebackground="#45a049", activeforeground="black")
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.pause_button = tk.Button(button_frame, text="一時停止", command=self.toggle_pause,
                                     bg="#FF9800", fg="black", font=("Arial", 14, "bold"),
                                     width=12, height=2, relief=tk.RAISED, bd=3,
                                     activebackground="#e68900", activeforeground="black")
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = tk.Button(button_frame, text="リセット", command=self.reset_game,
                                     bg="#F44336", fg="black", font=("Arial", 14, "bold"),
                                     width=12, height=2, relief=tk.RAISED, bd=3,
                                     activebackground="#da190b", activeforeground="black")
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # Instructions
        self.create_instructions(main_frame)
        
        # Game objects (will be created when game starts)
        self.player_paddle = None
        self.cpu_paddle = None
        self.ball = None
        
    def create_instructions(self, parent):
        instructions_frame = tk.Frame(parent, bg="#1B5E20")
        instructions_frame.pack(pady=15)
        
        instructions_label = tk.Label(instructions_frame, 
                                    text="🎮 操作方法", 
                                    font=("Arial", 16, "bold"), 
                                    bg="#1B5E20", fg="white")
        instructions_label.pack(pady=(0, 10))
        
        instructions_bg = tk.Frame(instructions_frame, bg="#F0F8FF", relief=tk.RAISED, bd=2)
        instructions_bg.pack(padx=20, pady=5)
        
        instructions_text = tk.Text(instructions_bg, 
                                  height=4, width=80, 
                                  font=("Arial", 11),
                                  bg="#F0F8FF", fg="#333333",
                                  relief=tk.FLAT, bd=0,
                                  wrap=tk.WORD, state=tk.DISABLED)
        instructions_text.pack(padx=15, pady=10)
        
        instructions_content = """🕹️ 矢印キー: ↑（上移動） ↓（下移動） ← ←（左移動） →（右移動）
🎯 目標: CPU相手にボールを打ち返してポイントを獲得しよう！
🏆 勝利条件: 先に10ポイント獲得したプレイヤーの勝利
⚡ 🔥SMASH🔥: ボールの進行方向と逆に動きながら打つとスマッシュ発動！
💪 チャージ: 同じ方向に動き続けるとパワーアップ、スマッシュがより強力に！"""
        
        instructions_text.config(state=tk.NORMAL)
        instructions_text.insert(tk.END, instructions_content)
        instructions_text.config(state=tk.DISABLED)
    
    def draw_court(self):
        # Court outline
        self.canvas.create_rectangle(5, 5, self.CANVAS_WIDTH-5, self.CANVAS_HEIGHT-5, 
                                   outline="white", width=3)
        # Center line
        self.canvas.create_line(self.CANVAS_WIDTH//2, 5, self.CANVAS_WIDTH//2, self.CANVAS_HEIGHT-5,
                               fill="white", width=2, dash=(10, 5))
        # Center circle
        self.canvas.create_oval(self.CANVAS_WIDTH//2 - 30, self.CANVAS_HEIGHT//2 - 30,
                               self.CANVAS_WIDTH//2 + 30, self.CANVAS_HEIGHT//2 + 30,
                               outline="white", width=2)
    
    def bind_keys(self):
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.focus_set()
    
    def on_key_press(self, event):
        self.keys_pressed.add(event.keysym)
    
    def on_key_release(self, event):
        self.keys_pressed.discard(event.keysym)
    
    def start_game(self):
        if not self.running:
            self.running = True
            self.game_paused = False
            self.start_button.config(text="実行中...", state="disabled")
            self.create_game_objects()
            self.game_loop()
    
    def toggle_pause(self):
        if self.running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.pause_button.config(text="再開")
            else:
                self.pause_button.config(text="一時停止")
    
    def reset_game(self):
        self.running = False
        self.game_paused = False
        self.player_score = 0
        self.cpu_score = 0
        
        # Reset smash system
        self.player_charge_time = 0
        self.cpu_charge_time = 0
        self.player_smash_count = 0
        self.cpu_smash_count = 0
        self.ball_speed_multiplier = 1.0
        self.ball_smash_effect = 0
        self.ball_color = "#FFEB3B"
        self.smash_effects = []
        self.ball_trail = []
        
        self.update_score()
        self.smash_label.config(text=f"Player Smashes: {self.player_smash_count}  |  CPU Smashes: {self.cpu_smash_count}")
        self.start_button.config(text="ゲーム開始", state="normal")
        self.pause_button.config(text="一時停止")
        self.reset_positions()
        self.canvas.delete("game_object")
        self.canvas.delete("ball_trail")
        self.canvas.delete("smash_effect")
        self.canvas.delete("smash_text")
    
    def reset_positions(self):
        self.player_y = self.CANVAS_HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        self.cpu_y = self.CANVAS_HEIGHT // 2 - self.PADDLE_HEIGHT // 2
        self.reset_ball()
    
    def reset_ball(self):
        self.ball_x = self.CANVAS_WIDTH // 2
        self.ball_y = self.CANVAS_HEIGHT // 2
        self.ball_dx = self.BALL_SPEED if random.choice([True, False]) else -self.BALL_SPEED
        self.ball_dy = random.choice([-3, -2, -1, 1, 2, 3])
        
        # Reset ball effects
        self.ball_speed_multiplier = 1.0
        self.ball_smash_effect = 0
        self.ball_color = "#FFEB3B"
        self.smash_effects = []
        self.ball_trail = []
    
    def create_game_objects(self):
        self.canvas.delete("game_object")
        
        # Player paddle (blue)
        self.player_paddle = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + self.PADDLE_WIDTH, self.player_y + self.PADDLE_HEIGHT,
            fill="#2196F3", outline="white", width=2, tags="game_object"
        )
        
        # CPU paddle (red)
        self.cpu_paddle = self.canvas.create_rectangle(
            self.cpu_x, self.cpu_y,
            self.cpu_x + self.PADDLE_WIDTH, self.cpu_y + self.PADDLE_HEIGHT,
            fill="#F44336", outline="white", width=2, tags="game_object"
        )
        
        # Ball
        self.ball = self.canvas.create_oval(
            self.ball_x - self.BALL_SIZE//2, self.ball_y - self.BALL_SIZE//2,
            self.ball_x + self.BALL_SIZE//2, self.ball_y + self.BALL_SIZE//2,
            fill="#FFEB3B", outline="white", width=2, tags="game_object"
        )
    
    def update_player(self):
        # Store previous position for velocity calculation
        self.player_prev_x = self.player_x
        self.player_prev_y = self.player_y
        
        # Handle player movement with arrow keys
        move_up = "Up" in self.keys_pressed and self.player_y > 5
        move_down = "Down" in self.keys_pressed and self.player_y < self.CANVAS_HEIGHT - self.PADDLE_HEIGHT - 5
        move_left = "Left" in self.keys_pressed and self.player_x > 5
        move_right = "Right" in self.keys_pressed and self.player_x < self.CANVAS_WIDTH // 2 - self.PADDLE_WIDTH - 5
        
        if move_up:
            self.player_y -= self.PLAYER_SPEED
        if move_down:
            self.player_y += self.PLAYER_SPEED
        if move_left:
            self.player_x -= self.PLAYER_SPEED
        if move_right:
            self.player_x += self.PLAYER_SPEED
        
        # Calculate velocity
        self.player_velocity_x = self.player_x - self.player_prev_x
        self.player_velocity_y = self.player_y - self.player_prev_y
        
        # Update charge time based on consistent movement
        if abs(self.player_velocity_x) > 0 or abs(self.player_velocity_y) > 0:
            self.player_charge_time += 1
        else:
            self.player_charge_time = max(0, self.player_charge_time - 2)
        
        # Cap charge time
        self.player_charge_time = min(self.player_charge_time, 60)  # 1 second at 60fps
        
        # Update paddle position
        if self.player_paddle:
            # Visual charge effect
            paddle_color = "#2196F3"
            if self.player_charge_time > 30:
                paddle_color = "#FF4081"  # Pink for charged
            elif self.player_charge_time > 15:
                paddle_color = "#9C27B0"  # Purple for half-charged
                
            self.canvas.coords(self.player_paddle,
                             self.player_x, self.player_y,
                             self.player_x + self.PADDLE_WIDTH, self.player_y + self.PADDLE_HEIGHT)
            self.canvas.itemconfig(self.player_paddle, fill=paddle_color)
    
    def update_cpu(self):
        # Store previous position for velocity calculation
        self.cpu_prev_x = self.cpu_x
        self.cpu_prev_y = self.cpu_y
        
        # Enhanced AI: follow the ball with some lag for realism
        ball_center_y = self.ball_y
        cpu_center_y = self.cpu_y + self.PADDLE_HEIGHT // 2
        
        # Add some randomness to CPU movement
        error = random.randint(-2, 2)
        target_y = ball_center_y + error
        
        # CPU attempts smash when ball is coming towards it
        cpu_speed = self.CPU_SPEED
        if (self.ball_dx > 0 and self.ball_x > self.CANVAS_WIDTH * 0.6 and 
            random.random() < 0.1):  # 10% chance to attempt smash
            cpu_speed = self.CPU_SPEED * 1.5  # Move faster for smash setup
        
        if cpu_center_y < target_y - 5:
            self.cpu_y += cpu_speed
        elif cpu_center_y > target_y + 5:
            self.cpu_y -= cpu_speed
        
        # Keep CPU paddle within bounds
        if self.cpu_y < 5:
            self.cpu_y = 5
        elif self.cpu_y > self.CANVAS_HEIGHT - self.PADDLE_HEIGHT - 5:
            self.cpu_y = self.CANVAS_HEIGHT - self.PADDLE_HEIGHT - 5
        
        # Calculate CPU velocity
        self.cpu_velocity_x = self.cpu_x - self.cpu_prev_x
        self.cpu_velocity_y = self.cpu_y - self.cpu_prev_y
        
        # Update CPU charge time
        if abs(self.cpu_velocity_y) > 0:
            self.cpu_charge_time += 1
        else:
            self.cpu_charge_time = max(0, self.cpu_charge_time - 2)
        
        self.cpu_charge_time = min(self.cpu_charge_time, 60)
        
        # Update paddle position
        if self.cpu_paddle:
            # Visual charge effect for CPU
            paddle_color = "#F44336"
            if self.cpu_charge_time > 30:
                paddle_color = "#FF9800"  # Orange for charged
            elif self.cpu_charge_time > 15:
                paddle_color = "#E91E63"  # Pink for half-charged
                
            self.canvas.coords(self.cpu_paddle,
                             self.cpu_x, self.cpu_y,
                             self.cpu_x + self.PADDLE_WIDTH, self.cpu_y + self.PADDLE_HEIGHT)
            self.canvas.itemconfig(self.cpu_paddle, fill=paddle_color)
    
    def update_ball(self):
        # Add current position to trail
        self.ball_trail.append((self.ball_x, self.ball_y))
        if len(self.ball_trail) > 8:  # Keep only recent positions
            self.ball_trail.pop(0)
        
        # Apply speed multiplier for effects
        effective_dx = self.ball_dx * self.ball_speed_multiplier
        effective_dy = self.ball_dy * self.ball_speed_multiplier
        
        # Move ball
        self.ball_x += effective_dx
        self.ball_y += effective_dy
        
        # Decrease smash effect over time
        if self.ball_smash_effect > 0:
            self.ball_smash_effect -= 1
            if self.ball_smash_effect == 0:
                self.ball_speed_multiplier = 1.0
                self.ball_color = "#FFEB3B"
        
        # Ball collision with top/bottom walls
        if self.ball_y <= self.BALL_SIZE//2 + 5 or self.ball_y >= self.CANVAS_HEIGHT - self.BALL_SIZE//2 - 5:
            self.ball_dy = -self.ball_dy
        
        # Ball collision with player paddle
        if (self.ball_x - self.BALL_SIZE//2 <= self.player_x + self.PADDLE_WIDTH and
            self.ball_x + self.BALL_SIZE//2 >= self.player_x and
            self.ball_y + self.BALL_SIZE//2 >= self.player_y and
            self.ball_y - self.BALL_SIZE//2 <= self.player_y + self.PADDLE_HEIGHT and
            self.ball_dx < 0):
            
            # Check for smash (player moving opposite to ball direction)
            is_smash = False
            smash_power = 1.0
            
            # Horizontal smash check
            if self.player_velocity_x > 0:  # Player moving right while ball comes from right
                is_smash = True
                smash_power = 1.5 + (self.player_charge_time / 60.0) * 1.0  # Up to 2.5x
            
            # Vertical smash check (ball moving down, player moving up)
            if self.ball_dy > 0 and self.player_velocity_y < 0:
                is_smash = True
                smash_power = max(smash_power, 1.3 + (self.player_charge_time / 60.0) * 0.7)
            elif self.ball_dy < 0 and self.player_velocity_y > 0:
                is_smash = True
                smash_power = max(smash_power, 1.3 + (self.player_charge_time / 60.0) * 0.7)
            
            # Calculate hit position for angle change
            hit_pos = (self.ball_y - (self.player_y + self.PADDLE_HEIGHT//2)) / (self.PADDLE_HEIGHT//2)
            self.ball_dx = abs(self.ball_dx) * smash_power
            self.ball_dy = hit_pos * 4 * smash_power
            
            if is_smash:
                self.execute_smash("Player", smash_power)
                self.player_charge_time = 0  # Reset charge after smash
        
        # Ball collision with CPU paddle
        if (self.ball_x + self.BALL_SIZE//2 >= self.cpu_x and
            self.ball_x - self.BALL_SIZE//2 <= self.cpu_x + self.PADDLE_WIDTH and
            self.ball_y + self.BALL_SIZE//2 >= self.cpu_y and
            self.ball_y - self.BALL_SIZE//2 <= self.cpu_y + self.PADDLE_HEIGHT and
            self.ball_dx > 0):
            
            # Check for CPU smash
            is_smash = False
            smash_power = 1.0
            
            # CPU smash logic (simpler than player)
            if self.cpu_velocity_x < 0:  # CPU moving left while ball comes from left
                is_smash = True
                smash_power = 1.3 + (self.cpu_charge_time / 60.0) * 0.5  # CPU is less powerful
            
            if abs(self.cpu_velocity_y) > self.CPU_SPEED * 0.5:  # Fast vertical movement
                is_smash = True
                smash_power = max(smash_power, 1.2 + (self.cpu_charge_time / 60.0) * 0.4)
            
            # Calculate hit position for angle change
            hit_pos = (self.ball_y - (self.cpu_y + self.PADDLE_HEIGHT//2)) / (self.PADDLE_HEIGHT//2)
            self.ball_dx = -abs(self.ball_dx) * smash_power
            self.ball_dy = hit_pos * 4 * smash_power
            
            if is_smash:
                self.execute_smash("CPU", smash_power)
                self.cpu_charge_time = 0
        
        # Score points
        if self.ball_x < 0:
            self.cpu_score += 1
            self.reset_ball()
            self.update_score()
            self.check_game_over()
        elif self.ball_x > self.CANVAS_WIDTH:
            self.player_score += 1
            self.reset_ball()
            self.update_score()
            self.check_game_over()
        
        # Update ball visual effects
        self.update_ball_visuals()
    
    def execute_smash(self, player, power):
        # Update smash stats
        if player == "Player":
            self.player_smash_count += 1
        else:
            self.cpu_smash_count += 1
        
        # Apply visual effects
        self.ball_smash_effect = 30  # Effect duration in frames
        self.ball_speed_multiplier = power
        
        # Change ball color based on smash power
        if power >= 2.0:
            self.ball_color = "#FF0000"  # Red for super smash
        elif power >= 1.5:
            self.ball_color = "#FF8C00"  # Orange for strong smash
        else:
            self.ball_color = "#FFA500"  # Light orange for normal smash
        
        # Create smash effect
        smash_x = self.ball_x
        smash_y = self.ball_y
        
        # Add explosion effect
        for _ in range(8):
            effect_x = smash_x + 20 * (power - 1) * random.uniform(0.5, 1.5) * (1 if random.random() > 0.5 else -1)
            effect_y = smash_y + 20 * (power - 1) * random.uniform(0.5, 1.5) * (1 if random.random() > 0.5 else -1)
            self.smash_effects.append({
                'x': effect_x,
                'y': effect_y,
                'life': 20,
                'color': '#FFD700' if player == "Player" else '#FF4444'
            })
        
        # Show smash text
        smash_text = "🔥SMASH!🔥" if power < 2.0 else "💥MEGA SMASH!💥"
        text_color = "#FFD700" if player == "Player" else "#FF4444"
        
        self.canvas.create_text(smash_x, smash_y - 30, text=smash_text, 
                               font=("Arial", 16, "bold"), fill=text_color,
                               tags="smash_text")
        self.root.after(1000, lambda: self.canvas.delete("smash_text"))
        
        # Update smash display
        self.smash_label.config(text=f"Player Smashes: {self.player_smash_count}  |  CPU Smashes: {self.cpu_smash_count}")
    
    def update_ball_visuals(self):
        if not self.ball:
            return
            
        # Draw ball trail
        self.canvas.delete("ball_trail")
        for i, (trail_x, trail_y) in enumerate(self.ball_trail[:-1]):
            alpha = (i + 1) / len(self.ball_trail)
            trail_size = int(self.BALL_SIZE * alpha * 0.7)
            trail_color = f"#{int(255 * alpha):02x}{int(255 * alpha):02x}00"
            self.canvas.create_oval(
                trail_x - trail_size//2, trail_y - trail_size//2,
                trail_x + trail_size//2, trail_y + trail_size//2,
                fill=trail_color, outline="", tags="ball_trail"
            )
        
        # Update smash effects
        self.canvas.delete("smash_effect")
        for effect in self.smash_effects[:]:
            if effect['life'] > 0:
                size = int(effect['life'] * 0.5)
                self.canvas.create_oval(
                    effect['x'] - size, effect['y'] - size,
                    effect['x'] + size, effect['y'] + size,
                    fill=effect['color'], outline="", tags="smash_effect"
                )
                effect['life'] -= 1
            else:
                self.smash_effects.remove(effect)
        
        # Update ball position and color
        self.canvas.coords(self.ball,
                         self.ball_x - self.BALL_SIZE//2, self.ball_y - self.BALL_SIZE//2,
                         self.ball_x + self.BALL_SIZE//2, self.ball_y + self.BALL_SIZE//2)
        self.canvas.itemconfig(self.ball, fill=self.ball_color)
    
    def update_score(self):
        self.score_label.config(text=f"Player: {self.player_score}  |  CPU: {self.cpu_score}")
    
    def check_game_over(self):
        if self.player_score >= 10:
            self.running = False
            self.canvas.create_text(self.CANVAS_WIDTH//2, self.CANVAS_HEIGHT//2,
                                  text="🏆 YOU WIN! 🏆", font=("Arial", 36, "bold"),
                                  fill="yellow", tags="game_object")
            self.start_button.config(text="ゲーム開始", state="normal")
        elif self.cpu_score >= 10:
            self.running = False
            self.canvas.create_text(self.CANVAS_WIDTH//2, self.CANVAS_HEIGHT//2,
                                  text="💻 CPU WINS! 💻", font=("Arial", 36, "bold"),
                                  fill="red", tags="game_object")
            self.start_button.config(text="ゲーム開始", state="normal")
    
    def game_loop(self):
        if self.running and not self.game_paused:
            self.update_player()
            self.update_cpu()
            self.update_ball()
            
            # Add charge display for player
            self.canvas.delete("charge_bar")
            if self.player_charge_time > 0:
                # Draw charge bar above player paddle
                bar_width = 60
                bar_height = 6
                bar_x = self.player_x - 10
                bar_y = self.player_y - 15
                
                charge_ratio = min(self.player_charge_time / 60.0, 1.0)
                charge_width = int(bar_width * charge_ratio)
                
                # Background bar
                self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                           fill="#333333", outline="white", tags="charge_bar")
                
                # Charge bar (color changes with level)
                if charge_ratio > 0.5:
                    charge_color = "#FF4081"  # Pink for full charge
                elif charge_ratio > 0.25:
                    charge_color = "#9C27B0"  # Purple for half charge
                else:
                    charge_color = "#2196F3"  # Blue for low charge
                    
                if charge_width > 0:
                    self.canvas.create_rectangle(bar_x, bar_y, bar_x + charge_width, bar_y + bar_height,
                                               fill=charge_color, outline="", tags="charge_bar")
                
            # CPU charge bar
            if self.cpu_charge_time > 0:
                bar_width = 60
                bar_height = 6
                bar_x = self.cpu_x - 10
                bar_y = self.cpu_y - 15
                
                cpu_charge_ratio = min(self.cpu_charge_time / 60.0, 1.0)
                cpu_charge_width = int(bar_width * cpu_charge_ratio)
                
                # Background bar
                self.canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                           fill="#333333", outline="white", tags="charge_bar")
                
                # CPU charge bar (orange theme)
                if cpu_charge_ratio > 0.5:
                    cpu_charge_color = "#FF9800"
                elif cpu_charge_ratio > 0.25:
                    cpu_charge_color = "#E91E63"
                else:
                    cpu_charge_color = "#F44336"
                    
                if cpu_charge_width > 0:
                    self.canvas.create_rectangle(bar_x, bar_y, bar_x + cpu_charge_width, bar_y + bar_height,
                                               fill=cpu_charge_color, outline="", tags="charge_bar")
        
        if self.running:
            self.root.after(16, self.game_loop)  # ~60 FPS


def main():
    root = tk.Tk()
    ActionTennisGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()