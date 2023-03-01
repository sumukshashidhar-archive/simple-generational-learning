import torch
from collections import deque
from game_wrapper import GameWrapper as Game
import numpy as np
import random

MAX_MEM = 100_000
BATCH_SIZE = 10
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        # control randomness
        self.epsilon = 0
        # control discount rate
        self.gamma = 0.0
        # memory
        self.memory = deque(maxlen=MAX_MEM)
        # model
        self.model = None
        # trainer
        self.trainer = None

    def get_state(self, game: Game):
        return np.array(game.get_distance_from_end(), dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 10 - self.n_games
        final_move = 0
        if random.randint(0, 50) < self.epsilon:
            final_move = random.randint(0, 1)
        else:
            # get prediction from NN
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = 1 if prediction >= 0.5 else 0
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        # get old state
        state_old = agent.get_state(game)
        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                # agent.model.save()
            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)



if __name__ == "__main__":
    train()


