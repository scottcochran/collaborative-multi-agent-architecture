from manim import *

class CollaborativeAIPresentation(Scene):
    def calculate_reading_time(self, *mobjects, min_time=2.0):
        """
        Calculate reading time based on word count at 100 words per minute.

        Args:
            *mobjects: Text objects or VGroups to count words from
            min_time: Minimum wait time in seconds (default 2.0)

        Returns:
            Reading time in seconds
        """
        word_count = 0

        def count_words_recursive(obj):
            nonlocal word_count
            if isinstance(obj, Text):
                # Get the text string and count words
                text_str = obj.original_text if hasattr(obj, 'original_text') else str(obj)
                word_count += len(text_str.split())
            elif isinstance(obj, VGroup):
                for item in obj:
                    count_words_recursive(item)

        for obj in mobjects:
            count_words_recursive(obj)

        # Calculate time: 100 words per minute = 0.6 seconds per word
        reading_time = word_count * 0.6

        # Ensure minimum time
        return max(reading_time, min_time)

    def construct(self):
        # Title Slide
        self.show_title_slide()

        # Principles
        self.show_principles()

        # Architecture Overview
        self.show_architecture()

        # Communication Layer
        self.show_communication()

        # Agent Components
        self.show_agent_components()

        # Deployment
        self.show_deployment()

        # Observability
        self.show_observability()

    def show_title_slide(self):
        title = Text("Collaborative AI System", font_size=48, gradient=(BLUE, GREEN))
        subtitle = Text("Architecture Overview", font_size=32).next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        wait_time = self.calculate_reading_time(title, subtitle)
        self.wait(wait_time)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_principles(self):
        title = Text("Core Principles", font_size=40, color=BLUE).to_edge(UP)

        principles = VGroup(
            Text("• AI-First Model", font_size=28),
            Text("  - Replace hard-coded business logic", font_size=24),
            Text("  - Policy-aware behavior", font_size=24),
            Text("• Declarative Policy (REGO)", font_size=28),
            Text("• Distributed Enforcement (OPA WASM)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(principles, shift=UP, lag_ratio=0.1))
        wait_time = self.calculate_reading_time(title, principles)
        self.wait(wait_time)
        self.play(FadeOut(title), FadeOut(principles))

    def show_architecture(self):
        title = Text("System Architecture", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))

        # Create main components as rectangles
        policy_box = Rectangle(width=2.5, height=1.2, color=YELLOW, fill_opacity=0.2)
        policy_text = Text("Policy Layer\n(OPA/REGO)", font_size=20).move_to(policy_box)
        policy_group = VGroup(policy_box, policy_text).shift(UP * 2)

        consensus_box = Rectangle(width=2.5, height=1.2, color=GREEN, fill_opacity=0.2)
        consensus_text = Text("Consensus\n(Paxos)", font_size=20).move_to(consensus_box)
        consensus_group = VGroup(consensus_box, consensus_text).shift(LEFT * 3)

        kafka_box = Rectangle(width=2.5, height=1.2, color=RED, fill_opacity=0.2)
        kafka_text = Text("Messaging\n(Kafka)", font_size=20).move_to(kafka_box)
        kafka_group = VGroup(kafka_box, kafka_text)

        agent_box = Rectangle(width=2.5, height=1.2, color=BLUE, fill_opacity=0.2)
        agent_text = Text("AI Agents\n(Claude)", font_size=20).move_to(agent_box)
        agent_group = VGroup(agent_box, agent_text).shift(RIGHT * 3)

        # Create arrows showing relationships
        arrow1 = Arrow(policy_group.get_bottom(), consensus_group.get_top(), color=WHITE)
        arrow2 = Arrow(policy_group.get_bottom(), kafka_group.get_top(), color=WHITE)
        arrow3 = Arrow(policy_group.get_bottom(), agent_group.get_top(), color=WHITE)
        arrow4 = Arrow(consensus_group.get_right(), kafka_group.get_left(), color=WHITE)
        arrow5 = Arrow(kafka_group.get_right(), agent_group.get_left(), color=WHITE)

        # Animate components
        self.play(Create(policy_group))
        self.play(
            Create(consensus_group),
            Create(kafka_group),
            Create(agent_group),
            lag_ratio=0.2
        )
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
            Create(arrow4),
            Create(arrow5),
            lag_ratio=0.1
        )

        wait_time = self.calculate_reading_time(title, policy_text, consensus_text, kafka_text, agent_text)
        self.wait(wait_time)
        self.play(
            FadeOut(title),
            FadeOut(policy_group),
            FadeOut(consensus_group),
            FadeOut(kafka_group),
            FadeOut(agent_group),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            FadeOut(arrow4),
            FadeOut(arrow5),
        )

    def show_communication(self):
        title = Text("Kafka Topics", font_size=40, color=RED).to_edge(UP)
        self.play(Write(title))

        # Create topic circles
        topics = VGroup(
            self.create_topic_node("Quorum", YELLOW, "30d retention"),
            self.create_topic_node("Agent", BLUE, "7d retention"),
            self.create_topic_node("Task", GREEN, "24h retention"),
            self.create_topic_node("Audit", PURPLE, "Permanent"),
        ).arrange_in_grid(rows=2, cols=2, buff=1.5).shift(DOWN * 0.5)

        self.play(FadeIn(topics, lag_ratio=0.2))

        # Show agent subtopics
        subtopics = VGroup(
            Text("• main", font_size=18),
            Text("• audit", font_size=18),
            Text("• cot", font_size=18),
            Text("• context", font_size=18),
            Text("• memory", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).scale(0.8).next_to(topics[1], RIGHT, buff=0.5)

        self.play(FadeIn(subtopics, shift=LEFT))

        wait_time = self.calculate_reading_time(title, topics, subtopics)
        self.wait(wait_time)
        self.play(FadeOut(title), FadeOut(topics), FadeOut(subtopics))

    def create_topic_node(self, name, color, retention):
        circle = Circle(radius=0.8, color=color, fill_opacity=0.3)
        text = Text(name, font_size=24).move_to(circle)
        retention_text = Text(retention, font_size=14, color=GRAY).next_to(circle, DOWN, buff=0.1)
        return VGroup(circle, text, retention_text)

    def show_agent_components(self):
        title = Text("Agent Components", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))

        # Create component list with categories
        components = VGroup(
            Text("Core:", font_size=28, color=YELLOW),
            Text("  • LLM Runtime (Claude)", font_size=22),
            Text("  • Kafka Producer/Consumer", font_size=22),
            Text("  • OPA Client/WASM", font_size=22),
            # Text("", font_size=22),
            Text("Safety:", font_size=28, color=RED),
            Text("  • Policy Enforcement Hooks", font_size=22),
            Text("  • Guardrails & Earmuffs", font_size=22),
            Text("  • Evaluation Hooks", font_size=22),
            # Text("", font_size=22),
            Text("Consensus:", font_size=28, color=GREEN),
            Text("  • Quorum Awareness", font_size=22),
            Text("  • Multi-channel Support", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(components, shift=UP, lag_ratio=0.05))
        wait_time = self.calculate_reading_time(title, components)
        self.wait(wait_time)
        self.play(FadeOut(title), FadeOut(components))

    def show_deployment(self):
        title = Text("Deployment Options", font_size=40, color=GREEN).to_edge(UP)
        self.play(Write(title))

        # Create deployment boxes
        docker_box = self.create_deployment_box("Docker", ["agent-network"], BLUE).shift(LEFT * 3.5 + DOWN * 0.5)
        helm_box = self.create_deployment_box("Helm Charts", ["Kafka", "OPA", "Agents"], GREEN).shift(DOWN * 0.5)
        mcp_box = self.create_deployment_box("MCP", ["Kafka", "OPA"], PURPLE).shift(RIGHT * 3.5 + DOWN * 0.5)

        deployments = VGroup(docker_box, helm_box, mcp_box)

        self.play(FadeIn(deployments, lag_ratio=0.2))
        wait_time = self.calculate_reading_time(title, deployments)
        self.wait(wait_time)
        self.play(FadeOut(title), FadeOut(deployments))

    def create_deployment_box(self, name, items, color):
        title_text = Text(name, font_size=28, color=color)
        item_texts = VGroup(*[Text(f"• {item}", font_size=20) for item in items])
        item_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(title_text, DOWN, buff=0.2)

        group = VGroup(title_text, item_texts)
        box = SurroundingRectangle(group, color=color, buff=0.3, corner_radius=0.1)
        return VGroup(box, group)

    def show_observability(self):
        title = Text("Observability Stack", font_size=40, color=ORANGE).to_edge(UP)
        self.play(Write(title))

        # Create observability diagram
        grafana_circle = Circle(radius=1.2, color=ORANGE, fill_opacity=0.2).shift(UP * 0.5)
        grafana_text = Text("Grafana", font_size=28).move_to(grafana_circle)
        grafana_subtitle = Text("Dashboards & Visualization", font_size=16, color=GRAY).next_to(grafana_circle, DOWN, buff=0.1)
        grafana_group = VGroup(grafana_circle, grafana_text, grafana_subtitle)

        otel_circle = Circle(radius=1.2, color=BLUE, fill_opacity=0.2).shift(DOWN * 2)
        otel_text = Text("OpenTelemetry", font_size=24).move_to(otel_circle)
        otel_subtitle = Text("Tracing & Metrics", font_size=16, color=GRAY).next_to(otel_circle, DOWN, buff=0.1)
        otel_group = VGroup(otel_circle, otel_text, otel_subtitle)

        arrow = Arrow(otel_group.get_top(), grafana_group.get_bottom(), color=WHITE)

        self.play(Create(otel_group))
        self.play(Create(arrow))
        self.play(Create(grafana_group))

        wait_time = self.calculate_reading_time(title, grafana_text, grafana_subtitle, otel_text, otel_subtitle)
        self.wait(wait_time)

        # Final reference
        self.play(FadeOut(title), FadeOut(grafana_group), FadeOut(otel_group), FadeOut(arrow))

        final_text = VGroup(
            Text("Collaborative AI System", font_size=48, gradient=(BLUE, GREEN)),
            Text("Built for distributed, policy-aware AI agents", font_size=24, color=GRAY),
        ).arrange(DOWN, buff=0.5)

        self.play(FadeIn(final_text))
        wait_time = self.calculate_reading_time(final_text)
        self.wait(wait_time)
        self.play(FadeOut(final_text))
