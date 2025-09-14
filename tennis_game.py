class TennisGame:
    def __init__(self, player1_name="Player 1", player2_name="Player 2"):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.game_over = False
        
    def get_score_display(self):
        score_map = {0: "0", 1: "15", 2: "30", 3: "40"}
        
        if self.player1_points >= 3 and self.player2_points >= 3:
            if self.player1_points == self.player2_points:
                return "Deuce"
            elif self.player1_points > self.player2_points:
                return f"Advantage {self.player1_name}"
            else:
                return f"Advantage {self.player2_name}"
        
        p1_score = score_map.get(self.player1_points, "40")
        p2_score = score_map.get(self.player2_points, "40")
        
        return f"{p1_score} - {p2_score}"
    
    def point_won_by(self, player):
        if self.game_over:
            return
            
        if player == 1:
            self.player1_points += 1
        else:
            self.player2_points += 1
            
        self._check_game_won()
    
    def _check_game_won(self):
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
                
                print(f"\nGame won by {winner_name}!")
                self._check_set_won()
    
    def _check_set_won(self):
        if (self.player1_games >= 6 or self.player2_games >= 6):
            if abs(self.player1_games - self.player2_games) >= 2:
                if self.player1_games > self.player2_games:
                    self.player1_sets += 1
                    winner_name = self.player1_name
                else:
                    self.player2_sets += 1
                    winner_name = self.player2_name
                
                print(f"Set won by {winner_name}!")
                self.player1_games = 0
                self.player2_games = 0
                
                self._check_match_won()
    
    def _check_match_won(self):
        if self.player1_sets >= 2 or self.player2_sets >= 2:
            winner = self.player1_name if self.player1_sets > self.player2_sets else self.player2_name
            print(f"\nMATCH WON BY {winner.upper()}!")
            self.game_over = True
    
    def get_full_score(self):
        return {
            'point_score': self.get_score_display(),
            'games': f"{self.player1_games} - {self.player2_games}",
            'sets': f"{self.player1_sets} - {self.player2_sets}",
            'game_over': self.game_over
        }
    
    def display_score(self):
        score = self.get_full_score()
        print(f"\nSets: {score['sets']}")
        print(f"Games: {score['games']}")
        print(f"Points: {score['point_score']}")


def main():
    print("=== Classic Tennis Game ===")
    player1 = input("Enter Player 1 name (or press Enter for 'Player 1'): ").strip() or "Player 1"
    player2 = input("Enter Player 2 name (or press Enter for 'Player 2'): ").strip() or "Player 2"
    
    game = TennisGame(player1, player2)
    
    print(f"\nGame started between {player1} and {player2}")
    print("Commands: '1' for Player 1 point, '2' for Player 2 point, 'q' to quit")
    
    while not game.game_over:
        game.display_score()
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == 'q':
            print("Game quit.")
            break
        elif command == '1':
            game.point_won_by(1)
        elif command == '2':
            game.point_won_by(2)
        else:
            print("Invalid command. Use '1', '2', or 'q'.")
    
    if game.game_over:
        game.display_score()


if __name__ == "__main__":
    main()