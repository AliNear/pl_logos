from typing import List
from unittest import result
from manim import *
import os


ASSETS_PATH = os.getcwd() + "/"
ASSETS_PATH.replace("\\", "/")

def big_rect(color):
    rect = Rectangle(
        fill_color=color,
        fill_opacity=1,
        width=14.2,
        height=8,
        stroke_width=0
    )
    rect.z_index = -1
    return rect

def get_submobject_by_id(logo: SVGMobject, near_id:str) -> (Mobject or None):
    for i in logo.submobjects:
        if i.near_id == near_id:
            return i

    return None

def get_submobjects_by_ids(
    logo: SVGMobject,
    near_ids: list[str]
) -> list[Mobject]:
    result = []
    for i in logo.submobjects:
        if i.near_id in near_ids:
            result.append(i)
    return result

class TestTransition(Scene):

    def construct(self):
        logo_1 = SVGMobject(ASSETS_PATH + "/svg/Brighton_&_Hove_Albion.svg")
        logo_2 = SVGMobject(ASSETS_PATH + "/svg/burnley.svg")
        logo_3 = SVGMobject(ASSETS_PATH + "/svg/chelsea.svg")

        rect_1 = big_rect("#005DAA")
        rect_2 = big_rect("#70193d")
        rect_3 = big_rect("#034694")

        self.play(FadeIn(logo_1), FadeIn(rect_1, shift=8*DOWN))
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
            LaggedStart(*animations_2),
            FadeOut(rect_1, shift=14.2*RIGHT),
            FadeIn(rect_2, shift=14.2*RIGHT),
            run_time=1.5
        )
        self.wait(.2)
        n_1 = len(logo_2.submobjects)
        n_2 = len(logo_3.submobjects)
        uncreations = [FadeOut(i) for i in logo_2.submobjects[:n_1-n_2]]

        animations = []
        for i in range(n_2):
            animations.append(FadeTransform(
                logo_2.submobjects[i+(n_1-n_2)],
                logo_3.submobjects[i],
            )) 
        
        self.play(
            LaggedStart(*uncreations, *animations),
            FadeOut(rect_2, shift=8*UP),
            FadeIn(rect_3, shift=8*UP),
            rate_func=rush_from,
            run_time=2
        )
        self.play(FadeOut(logo_3))
        self.wait()

class TestWithBgs(Scene):

    def construct(self):
        logo_1 = SVGMobject(ASSETS_PATH + "svg/arsenal.svg").scale(2)
        logo_2 = SVGMobject(ASSETS_PATH + "svg/chelsea.svg").scale(2)
        red_rect = Rectangle(
            color=RED,
            height=8,
            width=14.2
        )
        red_rect.set_fill(color="#EF0107", opacity=1)
        red_rect.z_index = -1
        blue_rect = Rectangle(width=14.2, height=8)
        blue_rect.set_fill(color="#034694", opacity=1)
        blue_rect.z_index = -1
        self.play(
            Create(logo_1),
            FadeIn(red_rect, shift=14.2*LEFT)
        )
        self.wait(.3)
        self.play(
            FadeTransformPieces(logo_1, logo_2),
            FadeOut(red_rect, shift=8*UP),
            FadeIn(blue_rect, shift=8*UP),
        )

class AnotherTransition(Scene):

    def construct(self):
        logo_1 = SVGMobject(ASSETS_PATH + "svg/chelsea.svg").scale(2)
        logo_2 = SVGMobject(ASSETS_PATH + "svg/Crystal_Palace.svg").scale(2)

        self.play(FadeIn(logo_1, shift=2*DOWN))
        self.wait()

        left_group = []
        right_group = []
        up_group = []
        first = True
        for i in logo_1.submobjects:
            x = i.get_x()
            threshold = .1
            if x < -threshold:
                left_group.append(ApplyMethod(i.shift, 3*LEFT))
            elif x > threshold:
                right_group.append(ApplyMethod(i.shift, 3*RIGHT))
            else:
                direction = first * UP + (not first) * DOWN
                first = not first
                up_group.append(ApplyMethod(i.shift, 2*direction))

        self.play(
            LaggedStart(
                *up_group,
                *left_group,
                *right_group,
            ),
            rate_func=rush_into,
            run_time=1
        )
        self.play(
            FadeTransformPieces(logo_1, logo_2),
            rate_func=rush_from,
            run_time=.9
        )
        self.wait(.2)
        eagle = VGroup(*get_submobjects_by_ids(logo_2, ["eagle_body", "eagle_wing"]))
        ball = VGroup(*get_submobjects_by_ids(logo_2, ["ball_"+str(i) for i in range(1, 7)]))

        self.play(
            ApplyMethod(eagle.shift, 4*UP+6*RIGHT),
            ApplyMethod(ball.shift, 4*UP+6*RIGHT),
        )
        s_ball = set(ball)
        s_eagle = set(eagle)
        s_eagle_ball = s_ball.union(s_eagle)
        s_all = set(logo_2.submobjects)
        s_rest = s_all.difference(s_eagle_ball)
        rest = list(s_rest)
        rest.reverse()
        rest_animation = [ApplyMethod(i.shift, 5*DOWN) for i in rest]
        self.play(
            LaggedStart(*rest_animation)
        )
        self.wait(.5)
        

class FadingToVoid(Scene):

    def construct(self):
        logo_2 = SVGMobject(ASSETS_PATH + "/svg/chelsea.svg")
        logo_1 = SVGMobject(ASSETS_PATH + "/svg/burnley.svg")
        logo_3 = SVGMobject(ASSETS_PATH + "/svg/manchester-city.svg")
        chelsea_color = "#034694"
        rect = big_rect(chelsea_color)
        self.add(rect)
        self.play(
            FadeIn(logo_1, shift=2*DOWN)
        )

        fadings = [ApplyMethod(i.set_color, chelsea_color) for i in logo_1.submobjects]

        self.play(
            LaggedStart(
                *fadings,
                rate_func=rush_into,
                run_time=1.2
            )
        )
        self.wait(.2)
        burnley_colors = []
        for i in logo_2.submobjects:
            burnley_colors.append(i.get_color())
            # i.set_color(BLACK)
        
        appearings = []
        # self.play(FadeIn(logo_2), run_time=.2)

        self.play(
            LaggedStart(
                *[FadeIn(i) for i in logo_2.submobjects],
                rate_func=rush_into,
                run_time=3,
                lag_ratio=.3
            )
        )