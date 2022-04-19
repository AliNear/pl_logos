from manim import Circle, Create, Scene


class SecondSpell(Scene):
    def construct(self):
        c = Circle()
        self.play(Create(c))
        self.wait()

    def prepare(self):
        pass
