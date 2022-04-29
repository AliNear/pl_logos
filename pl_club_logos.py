import os
from secrets import choice
from manim import *

ASSETS_PATH = os.getcwd() + "/"
ASSETS_PATH.replace("\\", "/")

def get_big_rect(color):
    rect = Rectangle(
        fill_color=color,
        fill_opacity=1,
        width=14.2,
        height=8,
        stroke_width=0
    )
    rect.z_index = -1
    return rect

def get_random_direction(i: int) -> np.ndarray:
    choices = [
        8 * UP,
        14.2 * RIGHT,
        8 * DOWN,
        14.2 * RIGHT,
        14.2 * LEFT,
        8 * DOWN,
        14.2 * LEFT,
        8 * UP,
        14.2 * RIGHT,
        8 * DOWN,
    ]
    return choices[i%len(choices)]

class PLClubLogos(Scene):
    def construct(self):
        self.prepare()
        self.start_animations()

    def prepare(self):
        # background_img = ImageMobject(ASSETS_PATH + "pl_bg.png").scale(1.4)
        logo_img = ImageMobject(ASSETS_PATH + "pl_logo.png").scale(.3)
        logo_img.set_x(-6)
        logo_img.set_y(3.5)
        #Current logo
        self.current = 0
        # self.add(background_img)
        self.add(logo_img)
        #Loading logos
        files = os.listdir(ASSETS_PATH + "/svg/")
        self.svgs = [SVGMobject(ASSETS_PATH + "/svg/" + i).scale(2) for i in files]
        #Norwich and Leicester have some special treatement :p
        for i in self.svgs:
            if i.file_name == "leicester-city.svg":
                i.submobjects[0].set_stroke(width=10)
            if i.file_name == "norwich-city.svg":
                i.set_stroke(width=.8)
                i.submobjects[0].set_stroke(width=8)

        #Loading club names
        self.names = []
        with open(ASSETS_PATH + "clubs.txt") as clubs:
            for i in clubs.readlines():
                name = Text(
                    i,
                    font="Premier League",
                    color=WHITE
                ).scale(.7)
                name.set_y(-2.8)
                self.names.append(name)
        #Creating backgrounds
        self.backgrounds = []
        with open(ASSETS_PATH + "colors.txt") as colors:
            for i in colors.readlines():
                self.backgrounds.append(get_big_rect(i))
 
    def start_animations(self):
        self.play(
            DrawBorderThenFill(self.svgs[0]),
            AddTextLetterByLetter(self.names[0]),
            FadeIn(self.backgrounds[0], shift=get_random_direction(self.current))
        )
        self.current += 1
        for i in range(1, 5):
            self.normal_transition()
        self.transition_higher_lower()
        self.transition_lower_higher()
    
    def normal_transition(self):
        direction = get_random_direction(self.current)
        self.play(
            FadeTransformPieces(self.svgs[self.current-1], self.svgs[self.current]),
            FadeTransformPieces(self.names[self.current-1], self.names[self.current]),
            FadeOut(self.backgrounds[self.current-1], shift=direction),
            FadeIn(self.backgrounds[self.current], shift=direction)
        )
        self.current += 1
        self.wait(.2)


    def transition_higher_lower(self):
        logo_1 = self.svgs[self.current-1]
        logo_2 = self.svgs[self.current]
        rect_1 = self.backgrounds[self.current-1]
        rect_2 = self.backgrounds[self.current]
        n_1 = len(logo_1.submobjects)
        n_2 = len(logo_2.submobjects)
        uncreations = [FadeOut(i) for i in logo_1.submobjects[:n_1-n_2]]

        animations = []
        for i in range(n_2):
            animations.append(FadeTransform(
                logo_1.submobjects[i+(n_1-n_2)],
                logo_2.submobjects[i],
            )) 
        
        self.play(
            FadeTransformPieces(self.names[self.current-1], self.names[self.current]),
            LaggedStart(*uncreations, *animations),
            FadeOut(rect_1, shift=8*UP),
            FadeIn(rect_2, shift=8*UP),
            rate_func=rush_from,
            run_time=2
        )
        self.wait(.2)
        self.current += 1
    def transition_lower_higher(self):
        logo_1 = self.svgs[self.current-1]
        logo_2 = self.svgs[self.current]
        rect_1 = self.backgrounds[self.current-1]
        rect_2 = self.backgrounds[self.current]
        n = len(logo_1.submobjects)
        animations = []
        for i in range(n):
            animations.append(FadeTransform(
                logo_1.submobjects[i],
                logo_2.submobjects[i],
            )) 
        animations_2 = [DrawBorderThenFill(i) for i in logo_2.submobjects[n:]]
        self.play(LaggedStart(*animations),rate_fun=rush_from, run_time=.5)
        self.play(
            FadeTransformPieces(self.names[self.current-1], self.names[self.current]),
            LaggedStart(*animations_2),
            FadeOut(rect_1, shift=14.2*RIGHT),
            FadeIn(rect_2, shift=14.2*RIGHT),
            run_time=1.5
        )
        self.wait(.2)
 

