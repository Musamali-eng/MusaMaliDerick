# ============================================
# COMPLETE FIXED SNAKE AI CODE
# ============================================

import pygame
import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim
import sys
import matplotlib.pyplot as plt
import time

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
print("All libraries imported successfully!")

# ============================================
# 1. GAME CONSTANTS
# ============================================
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
GRID_SIZE = 20
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (30, 30, 30)

print(f"Grid: {GRID_SIZE}x{GRID_SIZE}, Cell size: {CELL_SIZE}px")

# ============================================
# 2. SNAKE GAME ENVIRONMENT
# ============================================

class SnakeGame:
    def __init__(self):
        """Initialize the game"""
        self.reset()
    
    def reset(self):
        """Reset the game to start state"""
        center = GRID_SIZE // 2
        self.snake = [(center, center)]
        self.direction = (1, 0)
        self.score = 0
        self.steps_without_food = 0
        self.max_steps = 100
        
        self.food = self._place_food()
        return self._get_state()
    
    def _place_food(self):
        """Place food at random position not on snake"""
        while True:
            food = (random.randint(0, GRID_SIZE-1), 
                   random.randint(0, GRID_SIZE-1))
            if food not in self.snake:
                return food
    
    def _get_state(self):
        """Get the current state as a feature vector"""
        head = self.snake[0]
        dirs = [(1,0), (0,1), (-1,0), (0,-1)]
        current_dir_idx = dirs.index(self.direction)
        
        # Danger detection
        danger = []
        for i in [-1, 0, 1]:
            dir_idx = (current_dir_idx + i) % 4
            new_head = (head[0] + dirs[dir_idx][0], 
                       head[1] + dirs[dir_idx][1])
            
            if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
                new_head[1] < 0 or new_head[1] >= GRID_SIZE or
                new_head in self.snake):
                danger.append(1)
            else:
                danger.append(0)
        
        # Current direction (one-hot)
        dir_one_hot = [0, 0, 0, 0]
        dir_one_hot[current_dir_idx] = 1
        
        # Food direction
        food_x, food_y = self.food
        food_left = 1 if food_x < head[0] else 0
        food_right = 1 if food_x > head[0] else 0
        food_up = 1 if food_y < head[1] else 0
        food_down = 1 if food_y > head[1] else 0
        
        state = np.array(danger + dir_one_hot + [food_left, food_right, food_up, food_down], 
                        dtype=float)
        return state
    
    def step(self, action):
        """Execute an action and return (next_state, reward, done, score)"""
        dirs = [(1,0), (0,1), (-1,0), (0,-1)]
        current_idx = dirs.index(self.direction)
        
        if action == 1:
            current_idx = (current_idx + 1) % 4
        elif action == 2:
            current_idx = (current_idx - 1) % 4
        
        self.direction = dirs[current_idx]
        
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], 
                   head[1] + self.direction[1])
        
        ate_food = (new_head == self.food)
        
        if ate_food:
            self.snake.insert(0, self.food)
            self.food = self._place_food()
            self.score += 1
            self.steps_without_food = 0
            reward = 10
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
            self.steps_without_food += 1
            reward = -0.1
        
        done = False
        
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            done = True
            reward = -10
        elif new_head in self.snake[1:]:
            done = True
            reward = -10
        elif self.steps_without_food > self.max_steps:
            done = True
            reward = -10
        
        return self._get_state(), reward, done, self.score
    
    def render(self, screen):
        """Render the game"""
        screen.fill(BLACK)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # Draw food
        fx, fy = self.food
        pygame.draw.rect(screen, RED, 
                        (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))
        
        # Draw snake
        for i, (sx, sy) in enumerate(self.snake):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(screen, color,
                           (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE-2, CELL_SIZE-2))
        
        # Draw score
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

# ============================================
# 3. DEEP Q-NETWORK
# ============================================

class DQN(nn.Module):
    def __init__(self, input_size=11, hidden_size=256, output_size=3):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

# ============================================
# 4. DQN AGENT
# ============================================

class DQNAgent:
    def __init__(self, state_size=11, action_size=3):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=100000)
        
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
        self.learning_rate = 0.001
        self.gamma = 0.9
        self.batch_size = 64
        
        self.model = DQN(state_size, 256, action_size).to(device)
        self.target_model = DQN(state_size, 256, action_size).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        
        self.update_target_model()
        
        self.scores = []
        self.avg_scores = []
        self.losses = []
        self.epsilon_history = []
        
        print("Agent initialized!")
    
    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, training=True):
        if training and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = torch.FloatTensor(state).unsqueeze(0).to(device)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()
    
    def replay(self):
        if len(self.memory) < self.batch_size:
            return 0
        
        batch = random.sample(self.memory, self.batch_size)
        
        states = torch.FloatTensor([e[0] for e in batch]).to(device)
        actions = torch.LongTensor([e[1] for e in batch]).to(device)
        rewards = torch.FloatTensor([e[2] for e in batch]).to(device)
        next_states = torch.FloatTensor([e[3] for e in batch]).to(device)
        dones = torch.BoolTensor([e[4] for e in batch]).to(device)
        
        current_q = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_q = self.target_model(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * ~dones
        
        loss = nn.MSELoss()(current_q, target_q)
        
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        
        return loss.item()
    
    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# ============================================
# 5. RENDERING FUNCTIONS
# ============================================

def render_episode(env, agent, screen, clock):
    """Helper function to render a single episode"""
    state = env.reset()
    done = False
    steps = 0
    
    while not done:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        action = agent.act(state, training=False)
        state, reward, done, score = env.step(action)
        env.render(screen)
        clock.tick(30)
        steps += 1
        
        # Safety limit
        if steps > 1000:
            break
    
    print(f"  Episode Score: {score}, Steps: {steps}")
    pygame.time.wait(500)

def render_ai_game(agent, episodes=1, speed=30):
    """Watch the AI play the game with rendering"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Snake - Playing")
    clock = pygame.time.Clock()
    
    env = SnakeGame()
    total_scores = []
    
    for episode in range(episodes):
        print(f"Episode {episode + 1}/{episodes}")
        state = env.reset()
        done = False
        steps = 0
        
        while not done:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_SPACE:
                        # Simple pause by waiting for another key
                        paused = True
                        while paused:
                            for pause_event in pygame.event.get():
                                if pause_event.type == pygame.KEYDOWN:
                                    paused = False
                                if pause_event.type == pygame.QUIT:
                                    pygame.quit()
                                    return
            
            action = agent.act(state, training=False)
            next_state, reward, done, score = env.step(action)
            state = next_state
            env.render(screen)
            clock.tick(speed)
            steps += 1
            
            if steps > 1000:
                break
        
        total_scores.append(score)
        print(f"  Score: {score}, Steps: {steps}")
        time.sleep(1)
    
    avg_score = np.mean(total_scores) if total_scores else 0
    print(f"\nAverage Score over {episodes} episodes: {avg_score:.2f}")
    pygame.quit()

# ============================================
# 6. TRAINING FUNCTIONS
# ============================================

def train_agent(episodes=100, render_every=50, verbose=True, save_checkpoints=True):
    """Train the DQN agent"""
    env = SnakeGame()
    agent = DQNAgent()
    
    print("STARTING TRAINING")
    print("="*50)
    print(f"Episodes: {episodes}")
    print(f"Render every: {render_every} episodes")
    print()
    
    pygame_initialized = False
    screen = None
    clock = None
    
    best_score = 0
    consecutive_no_improvement = 0
    early_stop_threshold = 30
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        steps = 0
        episode_loss = 0
        
        while not done:
            if pygame_initialized:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return agent
            
            action = agent.act(state)
            next_state, reward, done, score = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            loss = agent.replay()
            episode_loss += loss
            state = next_state
            total_reward += reward
            steps += 1
            
            # Safety limit
            if steps > 1000:
                done = True
        
        agent.update_epsilon()
        
        if episode % 10 == 0:
            agent.update_target_model()
        
        agent.scores.append(score)
        avg_score = np.mean(agent.scores[-100:]) if len(agent.scores) >= 100 else np.mean(agent.scores)
        agent.avg_scores.append(avg_score)
        agent.epsilon_history.append(agent.epsilon)
        
        if score > best_score:
            best_score = score
            consecutive_no_improvement = 0
            if save_checkpoints:
                save_checkpoint(agent, episode, "best_model.pth")
        else:
            consecutive_no_improvement += 1
        
        # Early stopping
        if consecutive_no_improvement > early_stop_threshold and avg_score > 10:
            print(f"\nEarly stopping at episode {episode} - no improvement for {early_stop_threshold} episodes")
            break
        
        if verbose and episode % 10 == 0:
            avg_loss = episode_loss / steps if steps > 0 else 0
            print(f"Episode {episode:3d}/{episodes} | Score: {score:2d} | "
                  f"Avg Score: {avg_score:5.2f} | Best: {best_score:2d} | "
                  f"Epsilon: {agent.epsilon:.3f} | Steps: {steps:3d} | "
                  f"Loss: {avg_loss:.4f}")
        
        # Render if needed
        if episode % render_every == 0 and episode > 0:
            try:
                if not pygame_initialized:
                    pygame.init()
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    pygame.display.set_caption("AI Snake - Training")
                    clock = pygame.time.Clock()
                    pygame_initialized = True
                
                print(f"\nRendering episode {episode}...")
                render_episode(env, agent, screen, clock)
            except Exception as e:
                print(f" Rendering error: {e}")
                print("Continuing training without rendering...")
                if pygame_initialized:
                    pygame.quit()
                    pygame_initialized = False
    
    if pygame_initialized:
        pygame.quit()
    
    print("\n Training Complete!")
    print(f"Best Score: {best_score}")
    print(f"Final Average Score: {avg_score:.2f}")
    print(f"Final Epsilon: {agent.epsilon:.3f}")
    
    return agent

def full_training(episodes=500, render_every=50):
    """Full training with rendering at intervals"""
    env = SnakeGame()
    agent = DQNAgent()
    
    print("FULL TRAINING")
    print("="*60)
    print(f"Total Episodes: {episodes}")
    print(f"Visualization every: {render_every} episodes")
    print()
    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Snake - Training")
    clock = pygame.time.Clock()
    pygame_initialized = True
    
    best_score = 0
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        steps = 0
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return agent
            
            action = agent.act(state)
            next_state, reward, done, score = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            total_reward += reward
            steps += 1
            
            if steps > 1000:
                done = True
        
        agent.update_epsilon()
        
        if episode % 10 == 0:
            agent.update_target_model()
        
        agent.scores.append(score)
        avg_score = np.mean(agent.scores[-100:]) if len(agent.scores) >= 100 else np.mean(agent.scores)
        agent.avg_scores.append(avg_score)
        agent.epsilon_history.append(agent.epsilon)
        
        if score > best_score:
            best_score = score
            save_checkpoint(agent, episode, "best_model.pth")
        
        if episode % 10 == 0:
            print(f"Episode {episode:3d}/{episodes} | Score: {score:2d} | "
                  f"Avg: {avg_score:5.2f} | Best: {best_score:2d} | "
                  f"Eps: {agent.epsilon:.3f}")
        
        if episode % render_every == 0 and episode > 0:
            print(f"\nRendering episode {episode}...")
            try:
                render_episode(env, agent, screen, clock)
            except Exception as e:
                print(f"Rendering error: {e}")
                print("Continuing training...")
    
    pygame.quit()
    return agent

# ============================================
# 7. SAVE AND LOAD FUNCTIONS
# ============================================

def save_checkpoint(agent, episode, filename="checkpoint.pth"):
    """Save a training checkpoint"""
    torch.save({
        'episode': episode,
        'model_state_dict': agent.model.state_dict(),
        'optimizer_state_dict': agent.optimizer.state_dict(),
        'epsilon': agent.epsilon,
        'scores': agent.scores,
        'avg_scores': agent.avg_scores,
    }, filename)

def load_checkpoint(agent, filename="checkpoint.pth"):
    """Load a training checkpoint"""
    checkpoint = torch.load(filename)
    agent.model.load_state_dict(checkpoint['model_state_dict'])
    agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    agent.epsilon = checkpoint['epsilon']
    agent.scores = checkpoint['scores']
    agent.avg_scores = checkpoint['avg_scores']
    return agent, checkpoint['episode']

def save_model(agent, filename="snake_dqn.pth"):
    """Save the trained model"""
    torch.save({
        'model_state_dict': agent.model.state_dict(),
        'optimizer_state_dict': agent.optimizer.state_dict(),
        'epsilon': agent.epsilon,
        'scores': agent.scores,
        'avg_scores': agent.avg_scores,
    }, filename)
    print(f" Model saved to {filename}")

def load_model(filename="snake_dqn.pth"):
    """Load a trained model"""
    agent = DQNAgent()
    checkpoint = torch.load(filename, map_location=device)
    agent.model.load_state_dict(checkpoint['model_state_dict'])
    agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    agent.epsilon = checkpoint['epsilon']
    agent.scores = checkpoint['scores']
    agent.avg_scores = checkpoint['avg_scores']
    agent.update_target_model()
    print(f" Model loaded from {filename}")
    print(f"Epsilon: {agent.epsilon:.3f}")
    print(f"Best Score: {max(agent.scores) if agent.scores else 0}")
    return agent

# ============================================
# 8. VISUALIZATION FUNCTIONS
# ============================================

def plot_training_results(agent):
    """Plot training metrics"""
    if not agent.scores:
        print("No training data to plot")
        return
    
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(agent.scores, alpha=0.6, label='Episode Score')
    plt.plot(agent.avg_scores, color='red', linewidth=2, label='Avg Score (100 ep)')
    plt.title('Training Scores')
    plt.xlabel('Episode')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 3, 2)
    plt.plot(agent.avg_scores, color='green', linewidth=2)
    plt.title('Average Score')
    plt.xlabel('Episode')
    plt.ylabel('Average Score')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 3, 3)
    plt.plot(agent.epsilon_history, color='purple', linewidth=2)
    plt.title('Exploration Rate (Epsilon)')
    plt.xlabel('Episode')
    plt.ylabel('Epsilon')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ============================================
# 9. INTERACTIVE DEMO
# ============================================

def interactive_demo():
    """Interactive menu to test different scenarios"""
    print("\n" + "="*60)
    print("SNAKE AI DEMO")
    print("="*60)
    print("1. Train new model (fast - 100 episodes)")
    print("2. Train new model (full - 500 episodes)")
    print("3. Watch AI play (use trained model)")
    print("4. Load saved model and test")
    print("5. Compare random vs AI")
    print("6. Exit")
    print("="*60)
    
    choice = input("\nSelect option (1-6): ").strip()
    
    if choice == '1':
        print("\nTraining fast model...")
        agent = train_agent(episodes=100, render_every=20)
        save_model(agent, "fast_model.pth")
        
        print("\nWatching AI play...")
        render_ai_game(agent, episodes=2)
        
        print("\nPlotting results...")
        plot_training_results(agent)
        
    elif choice == '2':
        print("\nTraining full model...")
        agent = full_training(episodes=500, render_every=100)
        save_model(agent, "full_model.pth")
        
        print("\nWatching AI play...")
        render_ai_game(agent, episodes=3)
        
        print("\nPlotting results...")
        plot_training_results(agent)
        
    elif choice == '3':
        print("\nLoading trained model...")
        try:
            agent = load_model("best_model.pth")
        except FileNotFoundError:
            print("No trained model found. Training first...")
            agent = train_agent(episodes=100)
            save_model(agent, "best_model.pth")
        
        render_ai_game(agent, episodes=3)
    
    elif choice == '4':
        filename = input("Model filename (default: best_model.pth): ").strip()
        if not filename:
            filename = "best_model.pth"
        
        try:
            agent = load_model(filename)
            render_ai_game(agent, episodes=3)
            plot_training_results(agent)
        except FileNotFoundError:
            print(f" File '{filename}' not found!")
        except Exception as e:
            print(f" Error loading model: {e}")
    
    elif choice == '5':
        print("\nRandom vs AI Comparison")
        print("="*40)
        
        # Test random agent
        print("\nRandom Agent:")
        random_agent = DQNAgent()
        random_agent.epsilon = 1.0
        random_scores = []
        for _ in range(3):
            env = SnakeGame()
            state = env.reset()
            done = False
            while not done:
                action = random_agent.act(state, training=True)
                state, reward, done, score = env.step(action)
            random_scores.append(score)
            print(f"  Score: {score}")
        print(f"  Average Random Score: {np.mean(random_scores):.2f}")
        
        # Test trained AI
        print("\nTrained AI:")
        try:
            ai_agent = load_model("best_model.pth")
            render_ai_game(ai_agent, episodes=3)
        except FileNotFoundError:
            print("No trained model found. Training first...")
            ai_agent = train_agent(episodes=100)
            save_model(ai_agent, "best_model.pth")
            render_ai_game(ai_agent, episodes=2)
    
    elif choice == '6':
        print("Goodbye!")
        return
    
    else:
        print("Invalid choice")
        interactive_demo()

# ============================================
# 10. MAIN EXECUTION
# ============================================

def run_complete_pipeline():
    """Run the entire project from start to finish"""
    print("\n" + "="*60)
    print("COMPLETE RL SNAKE PROJECT")
    print("="*60)
    print("This will train the AI and show results")
    print("="*60 + "\n")
    
    # 1. Quick test
    print("Step 1: Testing environment...")
    test_env = SnakeGame()
    state = test_env.reset()
    print(f" Environment works! State size: {len(state)}")
    
    # 2. Train
    print("\nStep 2: Training AI (100 episodes)...")
    agent = train_agent(episodes=100, render_every=20, verbose=True)
    
    # 3. Save model
    print("\nStep 3: Saving model...")
    save_model(agent, "snake_ai_trained.pth")
    
    # 4. Show results
    print("\nStep 4: Visualizing results...")
    plot_training_results(agent)
    
    # 5. Render gameplay
    print("\nStep 5: Watching AI play...")
    render_ai_game(agent, episodes=2)
    
    print("\n" + "="*60)
    print("🎉 COMPLETE! All done!")
    print("="*60)
    print("\nYou can now:")
    print("- Load the model: agent = load_model('snake_ai_trained.pth')")
    print("- Watch it play: render_ai_game(agent)")
    print("- Continue training: train_agent(episodes=200)")

# ============================================
# 11. KEY CONCEPTS EXPLANATION
# ============================================

def explain_concepts():
    """Print key RL concepts"""
    print("\n" + "="*60)
    print("KEY REINFORCEMENT LEARNING CONCEPTS")
    print("="*60)
    
    concepts = {
        "Agent": "The snake AI that learns to play",
        "Environment": "The snake game world",
        "State": "11 features describing game situation",
        "Action": "3 possible moves: Straight, Right, Left",
        "Reward": "+10 for food, -0.1 per step, -10 for death",
        "Policy": "Strategy to choose actions (epsilon-greedy)",
        "Q-Value": "Expected future reward for each action",
        "Experience Replay": "Remember past experiences and learn from them",
        "Target Network": "Separate network for stable learning",
        "Bellman Equation": "Q(s,a) = r + γ * max Q(s',a')",
        "Exploration": "Trying new actions (epsilon)",
        "Exploitation": "Using learned knowledge",
    }
    
    for concept, explanation in concepts.items():
        print(f"\n🔹 {concept}:")
        print(f"   {explanation}")
    
    print("\n" + "="*60)
    print("DQN LEARNING PROCESS:")
    print("1. Agent observes state (11 features)")
    print("2. Chooses action (epsilon-greedy)")
    print("3. Gets reward and next state")
    print("4. Stores experience in memory")
    print("5. Samples random batch from memory")
    print("6. Updates Q-network using Bellman equation")
    print("7. Periodically updates target network")
    print("8. Decays epsilon for less exploration")
    print("="*60)

# ============================================
# 12. START THE PROGRAM
# ============================================

if __name__ == "__main__":
    print("\n" + ""*30)
    print("SNAKE AI - REINFORCEMENT LEARNING")
    print(*30)
    
    explain_concepts()
    
    print("\nChoose an option:")
    print("1. Quick start (train and play)")
    print("2. Interactive demo")
    print("3. Just watch AI play")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == '1':
        run_complete_pipeline()
    elif choice == '2':
        interactive_demo()
    elif choice == '3':
        try:
            agent = load_model("best_model.pth")
            render_ai_game(agent, episodes=5)
        except FileNotFoundError:
            print("No trained model found. Training first...")
            agent = train_agent(episodes=100)
            save_model(agent, "best_model.pth")
            render_ai_game(agent, episodes=3)
    else:
        print("Invalid choice. Running interactive demo...")
        interactive_demo()