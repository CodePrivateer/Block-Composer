class ComponentClass(object):
    
    def game_quit(self, state, game_field, screen_handler):

        if state['points'] > state['highscore']:  # Wenn die Punkte h�her sind als der Highscore, setzen Sie den Highscore auf die Punkte
            state['highscore'] = state['points']
            self.save_highscore(state['highscore'])
        game_field.reset_field()  # Setzen Sie das Spielfeld zurück
        screen_handler.game_over_screen()  # Zeigen Sie den Game Over-Bildschirm an
        screen_handler.score_screen(state)  # Zeigen Sie das Scoreboard an
        return state['highscore']
    
    def save_highscore(self, highscore):
        try:
            with open('highscore.txt', 'w') as file:
                file.write(str(highscore))
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

    def load_highscore():
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            print("Die Datei highscore.txt existiert nicht.")
            return 0
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return 0



