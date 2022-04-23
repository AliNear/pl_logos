import os
from manim import *

ASSETS_PATH = os.getcwd() + "/"
ASSETS_PATH.replace("\\", "/")

class PLClubLogos(Scene):
    def construct(self):
        self.prepare()
        self.start_animations()

    def prepare(self):
        background_img = ImageMobject(ASSETS_PATH + "pl_bg.png").scale(1.4)
        logo_img = ImageMobject(ASSETS_PATH + "pl_logo.png").scale(.3)
        logo_img.set_x(-6)
        logo_img.set_y(3.5)
        self.add(background_img)
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
 
    def start_animations(self):
        self.play(
            DrawBorderThenFill(self.svgs[0]),
            AddTextLetterByLetter(self.names[0])
        )
        for i in range(1, len(self.svgs)):
            self.play(
                FadeTransformPieces(self.svgs[i-1], self.svgs[i]),
                FadeTransformPieces(self.names[i-1], self.names[i]),
            )
            self.wait(.2)

    def transition_higher_lower(self):
        pass

    def transition_lower_higher(self):
        pass

