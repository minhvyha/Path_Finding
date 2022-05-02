# source code in the description
import pygame


from queue import PriorityQueue

pygame.init()
WIDTH = 500
LENGTH = 800
BORDER = 183
ROW = 50
GAP = WIDTH // ROW
COL = LENGTH // GAP
win = pygame.display.set_mode((LENGTH - 28, WIDTH - 30))

start_image = pygame.image.load('Start.png').convert_alpha()
reset_image = pygame.image.load('Reset.png').convert_alpha()

RED = (255, 0, 0)
GREEN = (60, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 120)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (180, 180, 180)
DGREY = (50, 50, 50)
TURQUOISE = (64, 224, 208)
b = (245, 0, 0)

font = pygame.font.SysFont('comicsans', 26)
font2 = pygame.font.SysFont('comicsans', 16)
font3 = pygame.font.SysFont('comicsans', 23)
font4 = pygame.font.SysFont('comicsans', 13)
text1 = font.render('Path Finding', True, RED)
text2 = font3.render('Visualisation', True, RED)

text3 = font2.render('Minh Vy Ha Version', True, b)
text4 = font4.render('CREDIT: TECH WITH TIM', 1, b)
text5 = font4.render('A* Algorithm', 1, b)


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.func = False
        self.image = pygame.transform.scale(
            image,
            (int(width * scale), int(height * scale)),
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def fun(self, pos):
        if self.rect.collidepoint(pos):
            self.func = True
        return


start_button = Button(8, 300, start_image, 0.21)
reset_button = Button(20, 350, reset_image, 0.45)


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            end.end()

            reconstruct(came_from, end, draw)
            start.start()
            return True
        for neighbor in current.neighbor:
            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                came_from[neighbor] = current
                f_score[neighbor] = g_score[neighbor] + h(
                    neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.open()
        draw()

        if current != start:
            current.close()
    return False


def make_grid():
    grid = []

    for i in range(ROW):
        grid.append([])
        for j in range(COL):
            node = Node(i, j)
            grid[i].append(node)
    return grid


def draw_grid():

    for i in range(ROW):
        pygame.draw.line(win, DGREY, (BORDER, i * GAP), (LENGTH, i * GAP))
    for i in range(COL):
        pygame.draw.line(win, DGREY, (i * GAP + BORDER, 0),
                         (i * GAP + BORDER, LENGTH))


def draw(grid):
    win.fill(GREY)
    win.blit(text1, (BORDER // 2 - text1.get_width() // 2, 10))
    win.blit(text2, (BORDER // 2 - text2.get_width() // 2, 45))
    win.blit(text3, (BORDER // 2 - text3.get_width() // 2, 85))
    win.blit(text4, (BORDER // 2 - text4.get_width() // 2, 120))
    win.blit(text5, (BORDER // 2 - text5.get_width() // 2, 145))
    start_button.draw()
    reset_button.draw()
    for i in range(ROW):
        grid[i][0].color = BLACK
        grid[i][COL - 22].color = BLACK
        grid[i][0].access = False
        grid[i][COL - 22].access = False

    for i in range(COL):
        grid[0][i].color = BLACK
        grid[ROW - 4][i].color = BLACK
        grid[0][i].access = False
        grid[ROW - 4][i].access = False

    for rows in grid:
        for node in rows:
            node.draw()
    draw_grid()
    pygame.display.update()


def get_cliked_pos(pos):
    dcol = BORDER // GAP
    x, y = pos
    row = y // GAP
    col = (x // GAP) - dcol
    return row, col


def main():

    grid = make_grid()
    start = None
    end = None
    run = True
    count = 0
    started = False
    while run:

        draw(grid)
        if start_button.func == True and count > 1:
            for row in grid:
                for node in row:
                    if node.color == YELLOW or node.color == WHITE or node.color == BLUE:
                        node.reset()
                        node.draw()

            start_button.func = False
            for row in grid:
                for node in row:
                    node.update_neighbor(grid)
            algorithm(lambda: draw(grid), grid, start, end)
        if reset_button.func == True:

            count = 0
            reset_button.func = False
            start = None
            end = None
            grid = make_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                x, y = pos
                row, col = get_cliked_pos((x, y))
                node = grid[row][col]
                if x < BORDER:
                    if count > 1:
                        start_button.fun(pos)
                    reset_button.fun(pos)
                    continue
                if node.access == False:

                    continue
                if not start and node != end:
                    start = node
                    start.start()

                elif not end and node != start:
                    end = node
                    end.end()
                elif node != start and node != end:
                    node.barrier()
                count += 1
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_cliked_pos(pos)

                if grid[row][col] == start:
                    start = None
                    count += 1
                elif grid[row][col] == end:
                    end = None
                    count += 1
                elif grid[row][col].is_barrier():
                    count += 1
                grid[row][col].reset()

    pygame.quit()


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GAP
        self.y = row * GAP
        self.color = GREY
        self.neighbor = []
        self.access = True

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == WHITE

    def is_open(self):
        return self.color == GREY

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == TURQUOISE

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = GREY

    def close(self):
        self.color = WHITE

    def open(self):
        self.color = YELLOW

    def barrier(self):
        self.color = BLACK

    def start(self):
        self.color = TURQUOISE

    def end(self):
        self.color = RED

    def block(self):
        self.access = False

    def path(self):
        self.color = BLUE

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x + BORDER, self.y, GAP, GAP))

    def update_neighbor(self, grid):
        self.neighbor = []
        if self.row < ROW - 1 and not grid[self.row +
                                           1][self.col].is_barrier():
            self.neighbor.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbor.append(grid[self.row - 1][self.col])

        if self.col < COL - 1 and not grid[self.row][self.col +
                                                     1].is_barrier():
            self.neighbor.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbor.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

if __name__ == "__main__":
  main()
