import tkinter as tk
import random
#from  import name

# 游戏设置
GAME_WIDTH = 400
GAME_HEIGHT = 400
GRID_SIZE = 20
INITIAL_DELAY = 200

class SnakeGameGUI:
    def __init__(self, name, score, in_game):
        self.window = tk.Toplevel()
        self.window.title("Snake Game "+name)
        self.canvas = tk.Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT, bg="white")
        self.canvas.pack()
        self.window.bind("<KeyPress>", self.on_key_press)
        self.score = score
        self.reset()
        self.name=name
        self.in_game = in_game

    def reset(self):
        self.snake = [(2, 1), (1, 1)]
        self.direction = "Right"
        self.apple = self.generate_apple()
        self.delay = INITIAL_DELAY
        self.score[0] = 0
        self.game_over = False
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        # 绘制网格
        for x in range(0, GAME_WIDTH, GRID_SIZE):
            self.canvas.create_line(x, 0, x, GAME_HEIGHT, fill="gray")
        for y in range(0, GAME_HEIGHT, GRID_SIZE):
            self.canvas.create_line(0, y, GAME_WIDTH, y, fill="gray")

        # 绘制蛇
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * GRID_SIZE, y * GRID_SIZE, (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, fill="green")

        # 绘制苹果
        x, y = self.apple
        self.canvas.create_oval(x * GRID_SIZE, y * GRID_SIZE, (x + 1) * GRID_SIZE, (y + 1) * GRID_SIZE, fill="red")

        # 绘制得分
        self.canvas.create_text(GAME_WIDTH // 2, 10, text="Score: {}".format(self.score[0]), anchor="n",fill='red')

        if self.game_over:
            self.in_game[0] = False
            self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text="Game Over", font=("Arial", 20), fill="red")

    def move_snake(self):
        head = self.snake[0]
        x, y = head

        if self.direction == "Up":
            y -= 1
        elif self.direction == "Down":
            y += 1
        elif self.direction == "Left":
            x -= 1
        elif self.direction == "Right":
            x += 1

        new_head = (x, y)

        if new_head == self.apple:
            self.score[0] += 1
            self.snake.insert(0, new_head)
            self.apple = self.generate_apple()
            self.delay *= 0.9
        elif x < 0 or x >= GAME_WIDTH // GRID_SIZE or y < 0 or y >= GAME_HEIGHT // GRID_SIZE or new_head in self.snake:
            self.game_over = True
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        self.draw()

        if not self.game_over:
            self.window.after(int(self.delay), self.move_snake)

    def on_key_press(self, event):
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

    def generate_apple(self):
        while True:
            x = random.randint(0, GAME_WIDTH // GRID_SIZE - 1)
            y = random.randint(0, GAME_HEIGHT // GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return x, y

    def run(self):
        self.window.after(0, self.move_snake)
        # self.window.mainloop()

def run_game(name, score, in_game):
    game = SnakeGameGUI(name, score, in_game)
    game.run()
    return game.score[0]

