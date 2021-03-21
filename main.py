from tkinter import *
import random

root = Tk()
root.title("Snake")
root.iconbitmap('Snake.ico')

WIDTH = 600


HEIGHT = 400


BODY_EL = 20

GAME_RUN = True


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#3498db")
c.grid()
c.focus_set()

class Body(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,x + BODY_EL, y + BODY_EL,fill="green")

class Snake(object):
    def __init__(self, segments):
        self.segments = segments

        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.mapping["Right"]

    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,x1 + self.vector[0] * BODY_EL, y1 + self.vector[1] * BODY_EL,x2 + self.vector[0] * BODY_EL, y2 + self.vector[1] * BODY_EL)

    def add_segment(self):
        score.increment()
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - BODY_EL
        y = last_seg[3] - BODY_EL
        self.segments.insert(0, Body(x, y))

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)

def create_snake():
    segments = [Body(BODY_EL, BODY_EL),Body(BODY_EL * 2, BODY_EL),Body(BODY_EL * 3, BODY_EL)]
    return Snake(segments)


class Score(object):


    def __init__(self):
        self.score = 0
        self.x = 55
        self.y = 15
        c.create_text(self.x, self.y, text="Счёт: {}".format(self.score), font="Arial 20",
                      fill="#34495e", tag="score", state='hidden')


    def increment(self):
        c.delete("score")
        self.score += 1
        c.create_text(self.x, self.y, text="Счёт: {}".format(self.score), font="Arial 20",
                      fill="#34495e", tag="score")


    def reset(self):
        c.delete("score")
        self.score = 0


score = Score()

def create_block():
    global BLOCK
    posx = BODY_EL * random.randint(1, (WIDTH - BODY_EL) / BODY_EL)
    posy = BODY_EL * random.randint(1, (HEIGHT - BODY_EL) / BODY_EL)
    BLOCK = c.create_oval(posx, posy,posx + BODY_EL, posy + BODY_EL,fill="green")

def create_danger():
    global DANGER
    posx = BODY_EL * random.randint(1, (WIDTH - BODY_EL) / BODY_EL)
    posy = BODY_EL * random.randint(1, (HEIGHT - BODY_EL) / BODY_EL)
    DANGER = c.create_rectangle(posx, posy,posx + BODY_EL, posy + BODY_EL,fill="Red")


def main():
    global GAME_RUN
    if GAME_RUN:
        s.move()


        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords


        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            GAME_RUN = False


        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            c.delete(DANGER)
            create_block()
            create_danger()

        elif head_coords == c.coords(DANGER):
		       GAME_RUN = False





        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    GAME_RUN = False

        root.after(100, main)

    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        set_state(close_but, 'normal')


def set_state(item, state):
    c.itemconfigure(item, state=state)
    c.itemconfigure(BLOCK, state='hidden')



def clicked(event):
    global GAME_RUN
    s.reset_snake()
    GAME_RUN = True
    c.delete(BLOCK)
    c.delete(DANGER)
    score.reset()
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    c.itemconfigure(close_but, state='hidden')
    start_game()


def start_game():
    global s
    create_block()
    create_danger()
    s = create_snake()


    c.bind("<KeyPress>", s.change_direction)
    main()


def close_win(root):
    exit()


game_over_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="You looser\n  ha-ha!!",font='Arial 20', fill='red',state='hidden')


restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3,
                             font='Arial 25',
                             fill='#34495e',
                             text="New game",
                             state='hidden')

close_but = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 5, font='Arial 25',
                          fill='#34495e',
                          text="EXIT",
                          state='hidden')


c.tag_bind(restart_text, "<Button-1>", clicked)
c.tag_bind(close_but, "<Button-1>", close_win)


start_game()


root.mainloop()