import os
from manim import *

ASSETS_PATH = os.getcwd() + "/svg/"
ASSETS_PATH.replace("\\", "/")

class SVGTest(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        files = os.listdir(ASSETS_PATH)
        svg = SVGMobject(ASSETS_PATH + files.pop(0))
        self.play(DrawBorderThenFill(svg))
        for i in files:
            svg_2 = SVGMobject(ASSETS_PATH + i)
            self.play(
                FadeTransformPieces(svg, svg_2)
            )
            self.wait(.2)
            svg = svg_2