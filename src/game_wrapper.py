from game import SimpleGame
class GameWrapper:
    def __init__(self, game):
        self.iteration = 0
        self.game = game

    def get_distance_from_end(self):
        # distance of pointer from end of array
        return len(self.game.get_array()) - self.game.get_pointer()
    

    def play_step(self, action):
        initial_distance = self.get_distance_from_end()
        if action == 0:
            response = self.game.move_left()
        elif action == 1:
            response = self.game.move_right()
        else:
            raise Exception("Invalid action")
        end_distance = self.get_distance_from_end()
        reward = initial_distance - end_distance
        if response:
            return reward, True, end_distance
        else:
            return reward, False, end_distance
    
    def reset(self):
        self.game = SimpleGame()
        self.iteration += 1



if __name__ == "__main__":
    g = SimpleGame()
    a = GameWrapper(g)
    print(a.get_distance_from_end())