class ActionTennisGame {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // Game constants
        this.CANVAS_WIDTH = 800;
        this.CANVAS_HEIGHT = 500;
        this.PADDLE_WIDTH = 10;
        this.PADDLE_HEIGHT = 80;
        this.BALL_SIZE = 12;
        this.PLAYER_SPEED = 8;
        this.CPU_SPEED = 6;
        this.BALL_SPEED = 6;
        
        // Game state
        this.running = false;
        this.paused = false;
        this.playerScore = 0;
        this.cpuScore = 0;
        
        // Smash system
        this.playerPrevX = 0;
        this.playerPrevY = 0;
        this.playerVelocityX = 0;
        this.playerVelocityY = 0;
        this.cpuPrevX = 0;
        this.cpuPrevY = 0;
        this.cpuVelocityX = 0;
        this.cpuVelocityY = 0;
        this.playerChargeTime = 0;
        this.cpuChargeTime = 0;
        this.playerSmashCount = 0;
        this.cpuSmashCount = 0;
        this.smashEffects = [];
        this.ballTrail = [];
        
        // Player paddle (left side)
        this.playerX = 20;
        this.playerY = this.CANVAS_HEIGHT / 2 - this.PADDLE_HEIGHT / 2;
        
        // CPU paddle (right side)
        this.cpuX = this.CANVAS_WIDTH - 30;
        this.cpuY = this.CANVAS_HEIGHT / 2 - this.PADDLE_HEIGHT / 2;
        
        // Ball
        this.ballX = this.CANVAS_WIDTH / 2;
        this.ballY = this.CANVAS_HEIGHT / 2;
        this.ballDx = this.BALL_SPEED;
        this.ballDy = Math.random() > 0.5 ? 3 : -3;
        this.ballSpeedMultiplier = 1.0;
        this.ballSmashEffect = 0;
        this.ballColor = '#FFEB3B';
        
        // Key states
        this.keysPressed = new Set();
        
        this.setupEventListeners();
        this.drawCourt();
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            this.keysPressed.add(e.key);
        });
        
        document.addEventListener('keyup', (e) => {
            this.keysPressed.delete(e.key);
        });
        
        // Prevent default arrow key behavior
        document.addEventListener('keydown', (e) => {
            if(['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                e.preventDefault();
            }
        });
    }
    
    drawCourt() {
        this.ctx.fillStyle = '#2E7D32';
        this.ctx.fillRect(0, 0, this.CANVAS_WIDTH, this.CANVAS_HEIGHT);
        
        // Court outline
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 3;
        this.ctx.strokeRect(5, 5, this.CANVAS_WIDTH - 10, this.CANVAS_HEIGHT - 10);
        
        // Center line
        this.ctx.setLineDash([10, 5]);
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(this.CANVAS_WIDTH / 2, 5);
        this.ctx.lineTo(this.CANVAS_WIDTH / 2, this.CANVAS_HEIGHT - 5);
        this.ctx.stroke();
        
        // Center circle
        this.ctx.beginPath();
        this.ctx.arc(this.CANVAS_WIDTH / 2, this.CANVAS_HEIGHT / 2, 30, 0, 2 * Math.PI);
        this.ctx.stroke();
        this.ctx.setLineDash([]);
    }
    
    resetBall() {
        this.ballX = this.CANVAS_WIDTH / 2;
        this.ballY = this.CANVAS_HEIGHT / 2;
        this.ballDx = Math.random() > 0.5 ? this.BALL_SPEED : -this.BALL_SPEED;
        this.ballDy = (Math.random() - 0.5) * 6;
        
        this.ballSpeedMultiplier = 1.0;
        this.ballSmashEffect = 0;
        this.ballColor = '#FFEB3B';
        this.smashEffects = [];
        this.ballTrail = [];
    }
    
    updatePlayer() {
        this.playerPrevX = this.playerX;
        this.playerPrevY = this.playerY;
        
        // Player movement
        if (this.keysPressed.has('ArrowUp') && this.playerY > 5) {
            this.playerY -= this.PLAYER_SPEED;
        }
        if (this.keysPressed.has('ArrowDown') && this.playerY < this.CANVAS_HEIGHT - this.PADDLE_HEIGHT - 5) {
            this.playerY += this.PLAYER_SPEED;
        }
        if (this.keysPressed.has('ArrowLeft') && this.playerX > 5) {
            this.playerX -= this.PLAYER_SPEED;
        }
        if (this.keysPressed.has('ArrowRight') && this.playerX < this.CANVAS_WIDTH / 2 - this.PADDLE_WIDTH - 5) {
            this.playerX += this.PLAYER_SPEED;
        }
        
        // Calculate velocity
        this.playerVelocityX = this.playerX - this.playerPrevX;
        this.playerVelocityY = this.playerY - this.playerPrevY;
        
        // Update charge time
        if (Math.abs(this.playerVelocityX) > 0 || Math.abs(this.playerVelocityY) > 0) {
            this.playerChargeTime++;
        } else {
            this.playerChargeTime = Math.max(0, this.playerChargeTime - 2);
        }
        
        this.playerChargeTime = Math.min(this.playerChargeTime, 60);
    }
    
    updateCpu() {
        this.cpuPrevX = this.cpuX;
        this.cpuPrevY = this.cpuY;
        
        // Simple AI
        const ballCenterY = this.ballY;
        const cpuCenterY = this.cpuY + this.PADDLE_HEIGHT / 2;
        const error = (Math.random() - 0.5) * 4;
        const targetY = ballCenterY + error;
        
        let cpuSpeed = this.CPU_SPEED;
        if (this.ballDx > 0 && this.ballX > this.CANVAS_WIDTH * 0.6 && Math.random() < 0.1) {
            cpuSpeed = this.CPU_SPEED * 1.5;
        }
        
        if (cpuCenterY < targetY - 5) {
            this.cpuY += cpuSpeed;
        } else if (cpuCenterY > targetY + 5) {
            this.cpuY -= cpuSpeed;
        }
        
        // Keep CPU within bounds
        if (this.cpuY < 5) this.cpuY = 5;
        if (this.cpuY > this.CANVAS_HEIGHT - this.PADDLE_HEIGHT - 5) {
            this.cpuY = this.CANVAS_HEIGHT - this.PADDLE_HEIGHT - 5;
        }
        
        // Calculate CPU velocity
        this.cpuVelocityX = this.cpuX - this.cpuPrevX;
        this.cpuVelocityY = this.cpuY - this.cpuPrevY;
        
        // Update CPU charge time
        if (Math.abs(this.cpuVelocityY) > 0) {
            this.cpuChargeTime++;
        } else {
            this.cpuChargeTime = Math.max(0, this.cpuChargeTime - 2);
        }
        
        this.cpuChargeTime = Math.min(this.cpuChargeTime, 60);
    }
    
    updateBall() {
        // Add to trail
        this.ballTrail.push({x: this.ballX, y: this.ballY});
        if (this.ballTrail.length > 8) {
            this.ballTrail.shift();
        }
        
        // Move ball
        const effectiveDx = this.ballDx * this.ballSpeedMultiplier;
        const effectiveDy = this.ballDy * this.ballSpeedMultiplier;
        
        this.ballX += effectiveDx;
        this.ballY += effectiveDy;
        
        // Decrease smash effect
        if (this.ballSmashEffect > 0) {
            this.ballSmashEffect--;
            if (this.ballSmashEffect === 0) {
                this.ballSpeedMultiplier = 1.0;
                this.ballColor = '#FFEB3B';
            }
        }
        
        // Wall collisions
        if (this.ballY <= this.BALL_SIZE / 2 + 5 || this.ballY >= this.CANVAS_HEIGHT - this.BALL_SIZE / 2 - 5) {
            this.ballDy = -this.ballDy;
        }
        
        // Player paddle collision
        if (this.ballX - this.BALL_SIZE / 2 <= this.playerX + this.PADDLE_WIDTH &&
            this.ballX + this.BALL_SIZE / 2 >= this.playerX &&
            this.ballY + this.BALL_SIZE / 2 >= this.playerY &&
            this.ballY - this.BALL_SIZE / 2 <= this.playerY + this.PADDLE_HEIGHT &&
            this.ballDx < 0) {
            
            let isSmash = false;
            let smashPower = 1.0;
            
            // Check for smash
            if (this.playerVelocityX > 0) {
                isSmash = true;
                smashPower = 1.5 + (this.playerChargeTime / 60.0) * 1.0;
            }
            
            if ((this.ballDy > 0 && this.playerVelocityY < 0) || 
                (this.ballDy < 0 && this.playerVelocityY > 0)) {
                isSmash = true;
                smashPower = Math.max(smashPower, 1.3 + (this.playerChargeTime / 60.0) * 0.7);
            }
            
            // Calculate hit position
            const hitPos = (this.ballY - (this.playerY + this.PADDLE_HEIGHT / 2)) / (this.PADDLE_HEIGHT / 2);
            this.ballDx = Math.abs(this.ballDx) * smashPower;
            this.ballDy = hitPos * 4 * smashPower;
            
            if (isSmash) {
                this.executeSmash('Player', smashPower);
                this.playerChargeTime = 0;
            }
        }
        
        // CPU paddle collision
        if (this.ballX + this.BALL_SIZE / 2 >= this.cpuX &&
            this.ballX - this.BALL_SIZE / 2 <= this.cpuX + this.PADDLE_WIDTH &&
            this.ballY + this.BALL_SIZE / 2 >= this.cpuY &&
            this.ballY - this.BALL_SIZE / 2 <= this.cpuY + this.PADDLE_HEIGHT &&
            this.ballDx > 0) {
            
            let isSmash = false;
            let smashPower = 1.0;
            
            // CPU smash logic
            if (this.cpuVelocityX < 0) {
                isSmash = true;
                smashPower = 1.3 + (this.cpuChargeTime / 60.0) * 0.5;
            }
            
            if (Math.abs(this.cpuVelocityY) > this.CPU_SPEED * 0.5) {
                isSmash = true;
                smashPower = Math.max(smashPower, 1.2 + (this.cpuChargeTime / 60.0) * 0.4);
            }
            
            const hitPos = (this.ballY - (this.cpuY + this.PADDLE_HEIGHT / 2)) / (this.PADDLE_HEIGHT / 2);
            this.ballDx = -Math.abs(this.ballDx) * smashPower;
            this.ballDy = hitPos * 4 * smashPower;
            
            if (isSmash) {
                this.executeSmash('CPU', smashPower);
                this.cpuChargeTime = 0;
            }
        }
        
        // Score points
        if (this.ballX < 0) {
            this.cpuScore++;
            this.resetBall();
            this.updateScore();
            this.checkGameOver();
        } else if (this.ballX > this.CANVAS_WIDTH) {
            this.playerScore++;
            this.resetBall();
            this.updateScore();
            this.checkGameOver();
        }
    }
    
    executeSmash(player, power) {
        if (player === 'Player') {
            this.playerSmashCount++;
        } else {
            this.cpuSmashCount++;
        }
        
        this.ballSmashEffect = 30;
        this.ballSpeedMultiplier = power;
        
        // Change ball color
        if (power >= 2.0) {
            this.ballColor = '#FF0000';
        } else if (power >= 1.5) {
            this.ballColor = '#FF8C00';
        } else {
            this.ballColor = '#FFA500';
        }
        
        // Create smash effects
        for (let i = 0; i < 8; i++) {
            this.smashEffects.push({
                x: this.ballX + 20 * (power - 1) * (Math.random() - 0.5) * 2,
                y: this.ballY + 20 * (power - 1) * (Math.random() - 0.5) * 2,
                life: 20,
                color: player === 'Player' ? '#FFD700' : '#FF4444'
            });
        }
        
        this.updateSmashStats();
    }
    
    draw() {
        // Clear and draw court
        this.drawCourt();
        
        // Draw ball trail
        this.ballTrail.forEach((pos, index) => {
            const alpha = (index + 1) / this.ballTrail.length;
            const size = this.BALL_SIZE * alpha * 0.7;
            this.ctx.fillStyle = `rgba(255, 255, 0, ${alpha * 0.5})`;
            this.ctx.fillRect(pos.x - size / 2, pos.y - size / 2, size, size);
        });
        
        // Draw smash effects
        this.smashEffects.forEach((effect, index) => {
            if (effect.life > 0) {
                const size = effect.life * 0.5;
                this.ctx.fillStyle = effect.color;
                this.ctx.fillRect(effect.x - size, effect.y - size, size * 2, size * 2);
                effect.life--;
            } else {
                this.smashEffects.splice(index, 1);
            }
        });
        
        // Draw player paddle
        const playerColor = this.playerChargeTime > 30 ? '#FF4081' : 
                           this.playerChargeTime > 15 ? '#9C27B0' : '#2196F3';
        this.ctx.fillStyle = playerColor;
        this.ctx.fillRect(this.playerX, this.playerY, this.PADDLE_WIDTH, this.PADDLE_HEIGHT);
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(this.playerX, this.playerY, this.PADDLE_WIDTH, this.PADDLE_HEIGHT);
        
        // Draw CPU paddle
        const cpuColor = this.cpuChargeTime > 30 ? '#FF9800' : 
                        this.cpuChargeTime > 15 ? '#E91E63' : '#F44336';
        this.ctx.fillStyle = cpuColor;
        this.ctx.fillRect(this.cpuX, this.cpuY, this.PADDLE_WIDTH, this.PADDLE_HEIGHT);
        this.ctx.strokeRect(this.cpuX, this.cpuY, this.PADDLE_WIDTH, this.PADDLE_HEIGHT);
        
        // Draw ball
        this.ctx.fillStyle = this.ballColor;
        this.ctx.fillRect(this.ballX - this.BALL_SIZE / 2, this.ballY - this.BALL_SIZE / 2, 
                         this.BALL_SIZE, this.BALL_SIZE);
        this.ctx.strokeRect(this.ballX - this.BALL_SIZE / 2, this.ballY - this.BALL_SIZE / 2, 
                           this.BALL_SIZE, this.BALL_SIZE);
        
        // Draw charge bars
        this.drawChargeBar(this.playerX - 10, this.playerY - 15, this.playerChargeTime);
        this.drawChargeBar(this.cpuX - 10, this.cpuY - 15, this.cpuChargeTime);
    }
    
    drawChargeBar(x, y, chargeTime) {
        if (chargeTime > 0) {
            const barWidth = 60;
            const barHeight = 6;
            const chargeRatio = Math.min(chargeTime / 60.0, 1.0);
            const chargeWidth = barWidth * chargeRatio;
            
            // Background
            this.ctx.fillStyle = '#333333';
            this.ctx.fillRect(x, y, barWidth, barHeight);
            this.ctx.strokeStyle = 'white';
            this.ctx.strokeRect(x, y, barWidth, barHeight);
            
            // Charge bar
            const chargeColor = chargeRatio > 0.5 ? '#FF4081' : 
                               chargeRatio > 0.25 ? '#9C27B0' : '#2196F3';
            this.ctx.fillStyle = chargeColor;
            this.ctx.fillRect(x, y, chargeWidth, barHeight);
        }
    }
    
    updateScore() {
        document.getElementById('player-score').textContent = `Player: ${this.playerScore}`;
        document.getElementById('cpu-score').textContent = `CPU: ${this.cpuScore}`;
    }
    
    updateSmashStats() {
        document.getElementById('smash-stats').textContent = 
            `Player Smashes: ${this.playerSmashCount} | CPU Smashes: ${this.cpuSmashCount}`;
    }
    
    checkGameOver() {
        if (this.playerScore >= 10) {
            this.running = false;
            this.ctx.fillStyle = 'yellow';
            this.ctx.font = '36px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('🏆 YOU WIN! 🏆', this.CANVAS_WIDTH / 2, this.CANVAS_HEIGHT / 2);
            document.getElementById('startBtn').textContent = 'ゲーム開始';
            document.getElementById('startBtn').disabled = false;
        } else if (this.cpuScore >= 10) {
            this.running = false;
            this.ctx.fillStyle = 'red';
            this.ctx.font = '36px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('💻 CPU WINS! 💻', this.CANVAS_WIDTH / 2, this.CANVAS_HEIGHT / 2);
            document.getElementById('startBtn').textContent = 'ゲーム開始';
            document.getElementById('startBtn').disabled = false;
        }
    }
    
    gameLoop() {
        if (this.running && !this.paused) {
            this.updatePlayer();
            this.updateCpu();
            this.updateBall();
        }
        
        this.draw();
        
        if (this.running) {
            requestAnimationFrame(() => this.gameLoop());
        }
    }
    
    start() {
        if (!this.running) {
            this.running = true;
            this.paused = false;
            document.getElementById('startBtn').textContent = '実行中...';
            document.getElementById('startBtn').disabled = true;
            this.gameLoop();
        }
    }
    
    togglePause() {
        if (this.running) {
            this.paused = !this.paused;
            document.getElementById('pauseBtn').textContent = this.paused ? '再開' : '一時停止';
        }
    }
    
    reset() {
        this.running = false;
        this.paused = false;
        this.playerScore = 0;
        this.cpuScore = 0;
        this.playerChargeTime = 0;
        this.cpuChargeTime = 0;
        this.playerSmashCount = 0;
        this.cpuSmashCount = 0;
        this.ballSpeedMultiplier = 1.0;
        this.ballSmashEffect = 0;
        this.ballColor = '#FFEB3B';
        this.smashEffects = [];
        this.ballTrail = [];
        
        this.playerY = this.CANVAS_HEIGHT / 2 - this.PADDLE_HEIGHT / 2;
        this.cpuY = this.CANVAS_HEIGHT / 2 - this.PADDLE_HEIGHT / 2;
        this.resetBall();
        
        this.updateScore();
        this.updateSmashStats();
        
        document.getElementById('startBtn').textContent = 'ゲーム開始';
        document.getElementById('startBtn').disabled = false;
        document.getElementById('pauseBtn').textContent = '一時停止';
        
        this.draw();
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const game = new ActionTennisGame(canvas);
    
    document.getElementById('startBtn').addEventListener('click', () => game.start());
    document.getElementById('pauseBtn').addEventListener('click', () => game.togglePause());
    document.getElementById('resetBtn').addEventListener('click', () => game.reset());
    
    // Initial draw
    game.draw();
});