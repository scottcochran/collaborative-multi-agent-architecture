from manim import *


class TitleScene(Scene):
    """Introduction slide with the main title."""
    def construct(self):
        title = Text("Agent Collaboration Protocol", font_size=48, weight=BOLD)
        subtitle = Text("An Implementation", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))


class ComponentsScene(Scene):
    """Display the 6 main components of the system."""
    def construct(self):
        title = Text("Components", font_size=42, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        components = [
            "1. Open Policy Agent",
            "2. Kafka",
            "3. NodeJS BFF",
            "4. React UI",
            "5. Paxos Policy Definitions in REGO",
            "6. Anthropic Claude AI Agent"
        ]

        component_texts = VGroup()
        for comp in components:
            text = Text(comp, font_size=28)
            component_texts.add(text)

        component_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        component_texts.next_to(title, DOWN, buff=0.8)

        for comp_text in component_texts:
            self.play(FadeIn(comp_text, shift=RIGHT), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(component_texts), FadeOut(title))


class ArchitectureOverview(Scene):
    """Visual representation of the system architecture."""
    def construct(self):
        title = Text("System Architecture", font_size=36, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # Create components as boxes
        opa = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.3)
        opa_text = Text("OPA", font_size=20)
        opa_text.move_to(opa.get_center())
        opa_group = VGroup(opa, opa_text)
        opa_group.shift(LEFT * 3 + UP * 1.5)

        kafka = Rectangle(width=2.5, height=1, color=GREEN, fill_opacity=0.3)
        kafka_text = Text("Kafka", font_size=20)
        kafka_text.move_to(kafka.get_center())
        kafka_group = VGroup(kafka, kafka_text)
        kafka_group.shift(UP * 0)

        bff = Rectangle(width=2, height=1, color=YELLOW, fill_opacity=0.3)
        bff_text = Text("NodeJS BFF", font_size=18)
        bff_text.move_to(bff.get_center())
        bff_group = VGroup(bff, bff_text)
        bff_group.shift(LEFT * 3 + DOWN * 1.5)

        ui = Rectangle(width=2, height=1, color=PURPLE, fill_opacity=0.3)
        ui_text = Text("React UI", font_size=20)
        ui_text.move_to(ui.get_center())
        ui_group = VGroup(ui, ui_text)
        ui_group.shift(LEFT * 3 + DOWN * 3)

        agents = Rectangle(width=2.5, height=1, color=ORANGE, fill_opacity=0.3)
        agents_text = Text("Claude Agents", font_size=18)
        agents_text.move_to(agents.get_center())
        agents_group = VGroup(agents, agents_text)
        agents_group.shift(RIGHT * 3)

        # Create components
        self.play(Create(opa_group))
        self.play(Create(kafka_group))
        self.play(Create(bff_group))
        self.play(Create(ui_group))
        self.play(Create(agents_group))

        # Create connections
        arrow1 = Arrow(opa.get_right(), kafka.get_left(), color=WHITE, buff=0.1)
        arrow2 = Arrow(kafka.get_left(), bff.get_right(), color=WHITE, buff=0.1)
        arrow3 = Arrow(bff.get_bottom(), ui.get_top(), color=WHITE, buff=0.1)
        arrow4 = Arrow(kafka.get_right(), agents.get_left(), color=WHITE, buff=0.1)
        arrow5 = Arrow(agents.get_left(), kafka.get_right(), color=WHITE, buff=0.1)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.play(Create(arrow4), Create(arrow5))

        self.wait(3)
        self.play(
            FadeOut(opa_group), FadeOut(kafka_group), FadeOut(bff_group),
            FadeOut(ui_group), FadeOut(agents_group),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
            FadeOut(arrow4), FadeOut(arrow5), FadeOut(title)
        )


class TheoryOfOperation(Scene):
    """Explain the theory of operation."""
    def construct(self):
        title = Text("Theory of Operation", font_size=42, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Paxos explanation
        paxos_text = Text(
            "Paxos procedures for achieving quorum\nare defined in REGO policy files",
            font_size=24,
            line_spacing=1.2
        )
        paxos_text.next_to(title, DOWN, buff=1)
        self.play(FadeIn(paxos_text, shift=UP))
        self.wait(2)

        # Kafka topic
        kafka_topic = Text("agent_quorum", font_size=32, color=GREEN, slant=ITALIC)
        kafka_label = Text("Kafka Topic:", font_size=24)
        kafka_group = VGroup(kafka_label, kafka_topic).arrange(RIGHT, buff=0.3)
        kafka_group.next_to(paxos_text, DOWN, buff=1)

        self.play(Write(kafka_label))
        self.play(Write(kafka_topic))
        self.wait(2)

        # Collaboration explanation
        collab_text = Text(
            "Agents collaborate by exchanging messages\nfollowing Paxos procedures",
            font_size=24,
            line_spacing=1.2
        )
        collab_text.next_to(kafka_group, DOWN, buff=1)
        self.play(FadeIn(collab_text, shift=UP))
        self.wait(2)

        self.play(
            FadeOut(title), FadeOut(paxos_text),
            FadeOut(kafka_group), FadeOut(collab_text)
        )


class AgentAccess(Scene):
    """Show what agents have access to."""
    def construct(self):
        title = Text("Agent LLM Access", font_size=42, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        access_items = [
            "1. Paxos policies in REGO",
            "2. All messages in the quorum topic"
        ]

        access_texts = VGroup()
        for item in access_items:
            text = Text(item, font_size=32)
            access_texts.add(text)

        access_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        access_texts.next_to(title, DOWN, buff=1.5)

        for access_text in access_texts:
            self.play(FadeIn(access_text, shift=RIGHT), run_time=0.7)
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(access_texts), FadeOut(title))


class ControlLogic(Scene):
    """Show what the control logic enforces."""
    def construct(self):
        title = Text("Agent Control Logic", font_size=42, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        subtitle = Text("Enforces:", font_size=32, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle))

        control_items = [
            "1. UUID selection",
            "2. Message schema conformance",
            "3. Paxos policy evaluation",
            "4. Skill access",
            "5. Tool access",
            "6. MCP access"
        ]

        control_texts = VGroup()
        for item in control_items:
            text = Text(item, font_size=28)
            control_texts.add(text)

        control_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        control_texts.next_to(subtitle, DOWN, buff=0.8)

        for control_text in control_texts:
            self.play(FadeIn(control_text, shift=RIGHT), run_time=0.4)

        self.wait(2)
        self.play(FadeOut(control_texts), FadeOut(subtitle), FadeOut(title))


class MessageFlow(Scene):
    """Animated visualization of message flow through Kafka."""
    def construct(self):
        title = Text("Message Flow: Agent Quorum", font_size=36, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))

        # Create Kafka topic representation
        kafka_box = Rectangle(width=8, height=2, color=GREEN, fill_opacity=0.2)
        kafka_label = Text("agent_quorum topic", font_size=24, color=GREEN)
        kafka_label.move_to(kafka_box.get_center())
        kafka_group = VGroup(kafka_box, kafka_label)

        self.play(Create(kafka_group))

        # Create agents
        agent1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.5)
        agent1_label = Text("Agent 1", font_size=16)
        agent1_label.move_to(agent1.get_center())
        agent1_group = VGroup(agent1, agent1_label)
        agent1_group.shift(LEFT * 5 + UP * 1)

        agent2 = Circle(radius=0.4, color=RED, fill_opacity=0.5)
        agent2_label = Text("Agent 2", font_size=16)
        agent2_label.move_to(agent2.get_center())
        agent2_group = VGroup(agent2, agent2_label)
        agent2_group.shift(LEFT * 5 + DOWN * 1)

        agent3 = Circle(radius=0.4, color=PURPLE, fill_opacity=0.5)
        agent3_label = Text("Agent 3", font_size=16)
        agent3_label.move_to(agent3.get_center())
        agent3_group = VGroup(agent3, agent3_label)
        agent3_group.shift(RIGHT * 5)

        self.play(FadeIn(agent1_group), FadeIn(agent2_group), FadeIn(agent3_group))

        # Animate messages
        for _ in range(3):
            msg1 = Dot(color=BLUE).move_to(agent1.get_center())
            msg2 = Dot(color=RED).move_to(agent2.get_center())
            msg3 = Dot(color=PURPLE).move_to(agent3.get_center())

            self.play(
                msg1.animate.move_to(kafka_box.get_center()),
                msg2.animate.move_to(kafka_box.get_center()),
                msg3.animate.move_to(kafka_box.get_center()),
                run_time=0.8
            )
            self.wait(0.3)
            self.remove(msg1, msg2, msg3)

        self.wait(2)
        self.play(
            FadeOut(kafka_group), FadeOut(agent1_group),
            FadeOut(agent2_group), FadeOut(agent3_group), FadeOut(title)
        )


class FullPresentation(Scene):
    """Complete presentation combining all scenes."""
    def construct(self):
        # 1. Title Scene
        title = Text("Agent Collaboration Protocol", font_size=48, weight=BOLD)
        subtitle = Text("An Implementation", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)

        # 2. Components Scene
        comp_title = Text("Components", font_size=42, weight=BOLD)
        comp_title.to_edge(UP)
        self.play(Write(comp_title))

        components = VGroup(
            Text("1. Open Policy Agent", font_size=26),
            Text("2. Kafka", font_size=26),
            Text("3. NodeJS BFF", font_size=26),
            Text("4. React UI", font_size=26),
            Text("5. Paxos Policy (REGO)", font_size=26),
            Text("6. Claude AI Agents", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        components.next_to(comp_title, DOWN, buff=0.8)

        for comp in components:
            self.play(FadeIn(comp, shift=RIGHT), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(components), FadeOut(comp_title))
        self.wait(0.5)

        # 3. Architecture Overview
        arch_title = Text("System Architecture", font_size=36, weight=BOLD)
        arch_title.to_edge(UP)
        self.play(Write(arch_title))

        # Create components as boxes
        opa = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.3)
        opa_text = Text("OPA", font_size=20)
        opa_text.move_to(opa.get_center())
        opa_group = VGroup(opa, opa_text).shift(LEFT * 3 + UP * 1.5)

        kafka = Rectangle(width=2.5, height=1, color=GREEN, fill_opacity=0.3)
        kafka_text = Text("Kafka", font_size=20)
        kafka_text.move_to(kafka.get_center())
        kafka_group = VGroup(kafka, kafka_text)

        bff = Rectangle(width=2, height=1, color=YELLOW, fill_opacity=0.3)
        bff_text = Text("NodeJS BFF", font_size=18)
        bff_text.move_to(bff.get_center())
        bff_group = VGroup(bff, bff_text).shift(LEFT * 3 + DOWN * 1.5)

        ui = Rectangle(width=2, height=1, color=PURPLE, fill_opacity=0.3)
        ui_text = Text("React UI", font_size=20)
        ui_text.move_to(ui.get_center())
        ui_group = VGroup(ui, ui_text).shift(LEFT * 3 + DOWN * 3)

        agents = Rectangle(width=2.5, height=1, color=ORANGE, fill_opacity=0.3)
        agents_text = Text("Claude Agents", font_size=18)
        agents_text.move_to(agents.get_center())
        agents_group = VGroup(agents, agents_text).shift(RIGHT * 3)

        self.play(Create(opa_group), Create(kafka_group), Create(bff_group),
                  Create(ui_group), Create(agents_group))

        arrow1 = Arrow(opa.get_right(), kafka.get_left(), color=WHITE, buff=0.1)
        arrow2 = Arrow(kafka.get_left(), bff.get_right(), color=WHITE, buff=0.1)
        arrow3 = Arrow(bff.get_bottom(), ui.get_top(), color=WHITE, buff=0.1)
        arrow4 = Arrow(kafka.get_right(), agents.get_left(), color=WHITE, buff=0.1)
        arrow5 = Arrow(agents.get_left(), kafka.get_right(), color=WHITE, buff=0.1)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3),
                  Create(arrow4), Create(arrow5))
        self.wait(3)

        self.play(FadeOut(VGroup(opa_group, kafka_group, bff_group, ui_group,
                                 agents_group, arrow1, arrow2, arrow3, arrow4,
                                 arrow5, arch_title)))
        self.wait(0.5)

        # 4. Theory of Operation
        theory_title = Text("Theory of Operation", font_size=42, weight=BOLD)
        theory_title.to_edge(UP)
        self.play(Write(theory_title))

        paxos_text = Text(
            "Paxos procedures for achieving quorum\nare defined in REGO policy files",
            font_size=24, line_spacing=1.2
        )
        paxos_text.next_to(theory_title, DOWN, buff=1)
        self.play(FadeIn(paxos_text, shift=UP))
        self.wait(1.5)

        kafka_topic = Text("agent_quorum", font_size=32, color=GREEN, slant=ITALIC)
        kafka_label = Text("Kafka Topic:", font_size=24)
        kafka_topic_group = VGroup(kafka_label, kafka_topic).arrange(RIGHT, buff=0.3)
        kafka_topic_group.next_to(paxos_text, DOWN, buff=1)

        self.play(Write(kafka_label), Write(kafka_topic))
        self.wait(1.5)

        collab_text = Text(
            "Agents collaborate by exchanging messages\nfollowing Paxos procedures",
            font_size=24, line_spacing=1.2
        )
        collab_text.next_to(kafka_topic_group, DOWN, buff=1)
        self.play(FadeIn(collab_text, shift=UP))
        self.wait(2)

        self.play(FadeOut(VGroup(theory_title, paxos_text, kafka_topic_group, collab_text)))
        self.wait(0.5)

        # 5. Agent Access
        access_title = Text("Agent LLM Access", font_size=42, weight=BOLD)
        access_title.to_edge(UP)
        self.play(Write(access_title))

        access_texts = VGroup(
            Text("1. Paxos policies in REGO", font_size=32),
            Text("2. All messages in the quorum topic", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        access_texts.next_to(access_title, DOWN, buff=1.5)

        for access_text in access_texts:
            self.play(FadeIn(access_text, shift=RIGHT), run_time=0.7)
            self.wait(0.5)

        self.wait(2)
        self.play(FadeOut(access_texts), FadeOut(access_title))
        self.wait(0.5)

        # 6. Control Logic
        control_title = Text("Agent Control Logic", font_size=42, weight=BOLD)
        control_title.to_edge(UP)
        self.play(Write(control_title))

        control_subtitle = Text("Enforces:", font_size=32, color=YELLOW)
        control_subtitle.next_to(control_title, DOWN, buff=0.5)
        self.play(FadeIn(control_subtitle))

        control_texts = VGroup(
            Text("1. UUID selection", font_size=28),
            Text("2. Message schema conformance", font_size=28),
            Text("3. Paxos policy evaluation", font_size=28),
            Text("4. Skill access", font_size=28),
            Text("5. Tool access", font_size=28),
            Text("6. MCP access", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        control_texts.next_to(control_subtitle, DOWN, buff=0.8)

        for control_text in control_texts:
            self.play(FadeIn(control_text, shift=RIGHT), run_time=0.4)

        self.wait(2)
        self.play(FadeOut(VGroup(control_texts, control_subtitle, control_title)))
        self.wait(0.5)

        # 7. Message Flow
        flow_title = Text("Message Flow: Agent Quorum", font_size=36, weight=BOLD)
        flow_title.to_edge(UP)
        self.play(Write(flow_title))

        kafka_box = Rectangle(width=8, height=2, color=GREEN, fill_opacity=0.2)
        kafka_flow_label = Text("agent_quorum topic", font_size=24, color=GREEN)
        kafka_flow_label.move_to(kafka_box.get_center())
        kafka_flow_group = VGroup(kafka_box, kafka_flow_label)
        self.play(Create(kafka_flow_group))

        agent1 = Circle(radius=0.4, color=BLUE, fill_opacity=0.5)
        agent1_label = Text("Agent 1", font_size=16)
        agent1_label.move_to(agent1.get_center())
        agent1_group = VGroup(agent1, agent1_label).shift(LEFT * 5 + UP * 1)

        agent2 = Circle(radius=0.4, color=RED, fill_opacity=0.5)
        agent2_label = Text("Agent 2", font_size=16)
        agent2_label.move_to(agent2.get_center())
        agent2_group = VGroup(agent2, agent2_label).shift(LEFT * 5 + DOWN * 1)

        agent3 = Circle(radius=0.4, color=PURPLE, fill_opacity=0.5)
        agent3_label = Text("Agent 3", font_size=16)
        agent3_label.move_to(agent3.get_center())
        agent3_group = VGroup(agent3, agent3_label).shift(RIGHT * 5)

        self.play(FadeIn(agent1_group), FadeIn(agent2_group), FadeIn(agent3_group))

        for _ in range(3):
            msg1 = Dot(color=BLUE).move_to(agent1.get_center())
            msg2 = Dot(color=RED).move_to(agent2.get_center())
            msg3 = Dot(color=PURPLE).move_to(agent3.get_center())

            self.play(
                msg1.animate.move_to(kafka_box.get_center()),
                msg2.animate.move_to(kafka_box.get_center()),
                msg3.animate.move_to(kafka_box.get_center()),
                run_time=0.8
            )
            self.wait(0.3)
            self.remove(msg1, msg2, msg3)

        self.wait(2)
        self.play(FadeOut(VGroup(kafka_flow_group, agent1_group, agent2_group,
                                 agent3_group, flow_title)))

        # Final outro
        self.wait(0.5)
        final_text = Text("Agent Collaboration Protocol", font_size=40, weight=BOLD)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text))
        self.wait(0.5)


# To render individual scenes:
# manim -pql architecture.py TitleScene
# manim -pql architecture.py ComponentsScene
# manim -pql architecture.py ArchitectureOverview
# manim -pql architecture.py TheoryOfOperation
# manim -pql architecture.py AgentAccess
# manim -pql architecture.py ControlLogic
# manim -pql architecture.py MessageFlow

# To render the complete presentation:
# manim -pql architecture.py FullPresentation
