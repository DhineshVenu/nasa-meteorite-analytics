from manim import *


class MeteoriteExplainerScene(Scene):

    def construct(self):
        # Dark background for high-contrast presentation
        self.camera.background_color = "#0B0E14"

        # 1. Header Title & Glowing Divider
        title = Text(
            "NASA Meteorite Landings Analytics",
            font="Sans-Serif",
            font_size=36,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP, buff=0.8)

        line = Line(
            start=LEFT * 5, end=RIGHT * 5, color=BLUE_D, stroke_width=2
        ).next_to(title, DOWN, buff=0.2)

        self.play(
            Write(title, run_time=1.2), Create(line, run_time=1.0), rate_func=smooth
        )
        self.wait(0.3)

        # 2. Metric Cards Setup
        stats_data = [
            ("Total Recorded Landings", "45,000+", BLUE_B),
            ("Heaviest Impact", "Hoba (60,000 kg)", RED_A),
            ("Primary Composition", "Iron & Chondrites", GREEN_B),
        ]

        cards = []
        for label, val, col in stats_data:
            # Rounded background card
            box = RoundedRectangle(
                corner_radius=0.15,
                height=1.2,
                width=11.0,
                fill_color="#161B22",
                fill_opacity=0.8,
                stroke_color=col,
                stroke_width=1.5,
            )

            # Left label
            lbl_text = Text(
                label, font_size=20, color=LIGHT_GRAY, weight=MEDIUM
            ).move_to(box.get_left() + RIGHT * 2.2)

            # Right value
            val_text = Text(
                val, font_size=22, color=col, weight=BOLD
            ).move_to(box.get_right() + LEFT * 2.5)

            card_content = VGroup(box, lbl_text, val_text)
            cards.append(card_content)

        # Arrange cards vertically
        card_stack = (
            VGroup(*cards).arrange(DOWN, buff=0.35).next_to(line, DOWN, buff=0.6)
        )

        # Animate card entries smoothly
        for card in card_stack:
            self.play(
                FadeIn(card, shift=UP * 0.3),
                run_time=0.8,
                rate_func=smooth,
            )
            self.wait(0.2)

        self.wait(1.0)

        # 3. Interactive Callout Highlight (Hoba Meteorite)
        hoba_card = card_stack[1]
        self.play(
            hoba_card.animate.scale(1.05),
            Indicate(hoba_card[2], color=RED_B, scale_factor=1.2),
            run_time=1.2,
        )
        self.wait(0.5)

        self.play(hoba_card.animate.scale(1 / 1.05), run_time=0.5)

        # 4. Outro Animation
        self.wait(1.5)
        self.play(
            FadeOut(card_stack, shift=DOWN * 0.4),
            FadeOut(title, shift=UP * 0.3),
            Uncreate(line),
            run_time=1.0,
        )
        self.wait(0.5)
