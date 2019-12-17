import pygame
import time
pygame.font.init()

class Grid:

    board = [[0 for i in range(9)] for j in range(9)]

    def __init__(
        self,
        rows,
        cols,
        width,
        height,
        win,
        ):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                      for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in
                      range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        (row, col) = self.selected
        self.cubes[row][col].set(val)
        self.update_model()

    def draw(self):

        # Draw Grid Lines
        self.win.fill((255, 255, 255))
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap),
                             (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i
                             * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def draw_white(self):
        (row, col) = self.selected
        self.cubes[row][col].draw_white(self.win)
        self.update_model()
        pygame.display.update()
        pygame.time.delay(100)

    def select(self, row, col):

        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        (row, col) = self.selected
        self.cubes[row][col].value = 0
        self.update_model()

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """

        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            (row, col) = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(10)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:

    rows = 9
    cols = 9

    def __init__(
        self,
        value,
        row,
        col,
        width,
        height,
        ):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont('comicsans', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not self.value == 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + gap / 2 - text.get_width() / 2, y + gap / 2 - text.get_height() / 2))

        if self.selected:
            pygame.draw.rect(win, (255, 255, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g):
        fnt = pygame.font.SysFont('comicsans', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + gap / 2 - text.get_width() / 2, y + gap / 2 - text.get_height() / 2))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_white(self, win):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

    def set(self, val):
        self.value = val


def valid(bo, num, pos):

    # Check row
    for cl in range(len(bo[0])):
        if bo[pos[0]][cl] == num and pos[1] != cl:
            return False

    # Check column
    for rw in range(len(bo)):
        if bo[rw][pos[1]] == num and pos[0] != rw:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def write_board(win, board):
    board.draw()
    fnt = pygame.font.SysFont('comicsans', 20)
    text = fnt.render('Enter your question and press "Enter" to get the solution.' , 1, (100, 100, 100))
    win.blit(text, (20, 560))
    text = fnt.render('"Backspace" to delete a number in a cell.', 1,(100, 100, 100))
    win.blit(text, (20, 580))


def write_invalid(win, board):
    board.draw()
    fnt = pygame.font.SysFont('comicsans', 40)
    text = fnt.render('Invalid Question!', 1, (255, 0, 0))
    win.blit(text, (20, 560))


def main():
    win = pygame.display.set_mode((550, 600))
    pygame.display.set_caption('Sudoku')
    board = Grid(9, 9, 550, 550, win)
    key = None
    run = True

    while run:

        write_board(win, board)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_RETURN:
                    key = None

                    # Solve board
                    if not board.solve_gui():
                        write_invalid(win, board)
                        run = False

        if board.selected and key != None:
            board.place(key)
            key = None

main()
pygame.quit()