import asyncio
import random
import json
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input, TabbedContent, TabPane
from textual.containers import Center, Vertical
from textual.binding import Binding

class ValentineApp(App):
    BINDINGS = [ Binding("q", "quit", "Quit"), ]

    CSS = """
    Screen { layers: main confetti heart rain; background: #2d0a0a; }
    #menu_screen { layer: main; width: 100%; height: 100%; background: #2d0a0a; }
    #proposal_screen { display: none; layer: main; width: 100%; height: 100%; }
    TabbedContent { height: 100%; background: #2d0a0a; }
    TabPane { background: #2d0a0a; align: center middle; layout: vertical; }

    #top_left_roses, #top_right_roses, #bottom_left_roses, #bottom_right_roses { layer: main; color: #ff0000; }
    #top_left_roses { dock: top; text-align: left; }
    #top_right_roses { dock: top; text-align: right; }
    #bottom_left_roses { dock: bottom; text-align: left; }
    #bottom_right_roses { dock: bottom; text-align: right; }

    #main_card { layer: main; width: 90%; height: auto; max-width: 50; border: double #f472b6; background: #2d0a0a; padding: 1; content-align: center middle; box-sizing: border-box; }

    #proposal_message { color: #ffb7c5; text-align: center; margin-bottom: 1; text-style: bold; width: 100%; }
    #proposal_text { color: #ff69b4; text-align: center; text-style: bold italic; margin: 1 0; width: 100%; }
    #beating_hearts, #beating_hearts_2 { color: #f472b6; text-align: center; margin-bottom: 1; height: 1; }

    #tears_flood { layer: rain; display: none; background: #001f3f; color: #3b82f6; width: 100%; height: 0; dock: bottom; content-align: center top; overflow: hidden; }
    #growing_heart { layer: heart; display: none; width: 100%; height: 100%; content-align: center middle; background: transparent; }
    #falling_hearts { layer: rain; display: none; width: 100%; height: 100%; background: transparent; }
    #falling_confetti { layer: confetti; display: none; width: 100%; height: 100%; background: transparent; }
    #falling_sparkles { layer: rain; display: none; width: 100%; height: 100%; background: transparent; }
    #success_message { layer: heart; display: none; width: 100%; height: 100%; content-align: center middle; background: #2d0a0a; border: double #f472b6; padding: 1; }

    .rose_corner { color: #ff0000; height: 1; }
    Button { width: 70%; min-width: 15; margin: 0 1; background: #b91d1d; color: white; border: solid #f472b6; }
    Button:hover { background: #d63031; text-style: bold; }
    .hidden { display: none; }

    #menu_title { color: #ff69b4; text-align: center; text-style: bold; height: 3; content-align: center middle; border: double #f472b6; background: #3d1515; padding: 1; }
    .input_label { color: #ffb7c5; width: 90%; margin-top: 1; text-align: center; }
    Input { margin: 1 1; width: 90%; max-width: 50; background: #3d1515; border: solid #f472b6; color: #ffb7c5; }
    #messages_display { width: 90%; max-width: 80; height: auto; border: solid #f472b6; background: #3d1515; color: #ffb7c5; overflow: auto; margin: 1 1; padding: 1; }
    """

    def __init__(self):
        super().__init__()
        self.messages = self._load_messages()
        self.custom_proposal = "Will you be my Valentine's? ❤️"
        self.custom_name = "Your Name"
        self.current_screen = "menu"

    def _load_messages(self):
        try:
            with open("valentine_messages.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_messages(self):
        with open("valentine_messages.json", "w") as f:
            json.dump(self.messages, f)

    def compose(self) -> ComposeResult:
        yield Static("🌹🌹🌹", id="top_left_roses")
        yield Static("🌹🌹🌹", id="top_right_roses")

        # Global animation layers (must be outside proposal screen)
        yield Static("😭 💧 😭 💧 😭 💧", id="tears_flood")
        yield Static("", id="growing_heart")
        yield Static("", id="falling_hearts")
        yield Static("", id="falling_confetti")
        yield Static("", id="falling_sparkles")
        yield Static("", id="success_message")

        # Menu with tabs
        with Static(id="menu_screen"):
            yield Static("💖 VALENTINE'S 2026 💖", id="menu_title")
            with TabbedContent(initial="send_valentine_tab"):
                with TabPane("💌 Send Valentine", id="send_valentine_tab"):
                    with Vertical():
                        yield Static("Customize Your Valentine Proposal", classes="input_label")
                        yield Input(id="name_input", placeholder="Recipient's name...")
                        yield Static("Your proposal:", classes="input_label")
                        yield Input(id="proposal_input", placeholder=self.custom_proposal)
                        with Center():
                            yield Button("Send Valentine ✨", id="send_proposal_btn")
                with TabPane("💐 View Messages", id="view_messages_tab"):
                    with Vertical():
                        yield Static("Saved Messages", classes="input_label")
                        yield Static("", id="messages_display")
                        with Center():
                            yield Button("Clear All", id="clear_messages_btn")
                with TabPane("🎨 Gallery", id="gallery_tab"):
                    with Vertical():
                        yield Static("Valentine's Gallery", classes="input_label")
                        yield Static("See confetti, sparkles & hearts!", id="gallery_text")
                        with Center():
                            yield Button("View Demo ✨", id="demo_btn")

        # Proposal screen (hidden initially)
        with Static(id="proposal_screen"):
            with Static(id="main_card"):
                yield Static("✨ MOMENT OF TRUTH ✨", id="proposal_message")
                yield Static("", id="beating_hearts")
                yield Static(self.custom_proposal, id="proposal_text")
                yield Static("", id="beating_hearts_2")
                with Center(id="buttons_container"):
                    yield Button("YES! ✨", id="yes_btn", variant="success")
                    yield Button("No 😔", id="no_btn")
                yield Static("", id="message_area")
            yield Static("🌹🌹🌹", id="bottom_left_roses")
            yield Static("🌹🌹🌹", id="bottom_right_roses")

    def on_mount(self) -> None:
        self.set_interval(0.5, self._animate_beating_hearts)
        self._refresh_messages_display()

    def _animate_beating_hearts(self) -> None:
        patterns = ["💖 💖 💖", "❤️  ❤️  ❤️", "💕 💕 💕", "💗 💗 💗"]
        for heart in self.query("#beating_hearts, #beating_hearts_2"):
            heart.update(random.choice(patterns))

    def _refresh_messages_display(self):
        display = self.query_one("#messages_display")
        if not self.messages:
            display.update("Send a Valentine to start!")
        else:
            text = ""
            for i, m in enumerate(self.messages, 1):
                text += f"💌 #{i}\nFrom: {m['from']}\nTo: {m['to']}\nMsg: {m['message']}\nReply: {m['response']}\n\n"
            display.update(text)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn = event.button.id

        if btn == "send_proposal_btn":
            await self._handle_send_proposal()
            return

        if btn == "clear_messages_btn":
            self.messages = []
            self._save_messages()
            self._refresh_messages_display()
            return

        if btn == "demo_btn":
            await self._show_demo_effects()
            return

        if btn == "yes_btn":
            self.query_one("#yes_btn").add_class("hidden")
            self.query_one("#no_btn").add_class("hidden")
            self.query_one("#proposal_screen").styles.display = "none"
            self.query_one("#main_card").styles.display = "none"
            await self._grow_and_burst_heart()
            return

        if btn == "no_btn":
            proposal = self.query_one("#proposal_text")
            proposal.update("[b]HEART SHATTERED[/b]")
            self.query_one("#yes_btn").add_class("hidden")
            self.query_one("#no_btn").add_class("hidden")
            asyncio.create_task(self.flood_with_tears())
            await self.type_text("The world went dark. 😭\nSilence louder than words...\nMy heart is drowning...")
            self.messages.append({"from": self.custom_name, "to": "Unknown", "message": self.custom_proposal, "response": "No... 😔"})
            self._save_messages()
            await asyncio.sleep(3)
            self.query_one("#proposal_screen").styles.display = "none"
            self.query_one("#menu_screen").styles.display = "block"
            self._refresh_messages_display()
            return

    async def _handle_send_proposal(self):
        name_input = self.query_one("#name_input", Input)
        proposal_input = self.query_one("#proposal_input", Input)
        self.custom_name = name_input.value or "Your Name"
        self.custom_proposal = proposal_input.value or "Will you be my Valentine's? ❤️"
        self.query_one("#proposal_text").update(self.custom_proposal)
        self.query_one("#menu_screen").styles.display = "none"
        self.query_one("#proposal_screen").styles.display = "block"
        self.current_screen = "proposal"

    async def _show_demo_effects(self):
        self.query_one("#menu_screen").styles.display = "none"
        asyncio.create_task(self.fall_confetti())
        asyncio.create_task(self.fall_sparkles())
        asyncio.create_task(self.rain_hearts())
        await asyncio.sleep(5)
        self.query_one("#falling_confetti").styles.display = "none"
        self.query_one("#falling_sparkles").styles.display = "none"
        self.query_one("#falling_hearts").styles.display = "none"
        self.query_one("#menu_screen").styles.display = "block"

    async def _grow_and_burst_heart(self):
        heart_widget = self.query_one("#growing_heart")
        heart_widget.styles.display = "block"
        frames = [
            "❤️","❤️ ❤️","❤️  ❤️\n ❤️ ❤️","❤️   ❤️\n❤️   ❤️\n ❤️ ❤️",
            "❤️    ❤️\n❤️    ❤️\n❤️    ❤️\n ❤️  ❤️\n  ❤️ ❤️"
        ]
        for f in frames:
            heart_widget.update(f)
            await asyncio.sleep(0.12)
        await asyncio.sleep(0.25)
        for frame in ["💥 ✨ 💥","✨ 💥 ✨","💥 ✨ 💥"] * 3:
            heart_widget.update(frame)
            await asyncio.sleep(0.12)
        heart_widget.styles.display = "none"

        # show success text first so it's not obscured, then start particles
        await self._show_success_message()

        # start background particle animations (finite runs)
        asyncio.create_task(self.rain_hearts())
        asyncio.create_task(self.fall_confetti())
        asyncio.create_task(self.fall_sparkles())

        self.messages.append({"from": self.custom_name, "to": "You", "message": self.custom_proposal, "response": "YES! YES! YES!"})
        self._save_messages()

        await asyncio.sleep(4)
        # cleanup and return to menu
        self.query_one("#success_message").styles.display = "none"
        self.query_one("#falling_hearts").styles.display = "none"
        self.query_one("#falling_confetti").styles.display = "none"
        self.query_one("#falling_sparkles").styles.display = "none"
        self.query_one("#proposal_screen").styles.display = "none"
        self.query_one("#menu_screen").styles.display = "block"
        self._refresh_messages_display()

    async def rain_hearts(self):
        falling = self.query_one("#falling_hearts")
        falling.styles.display = "block"
        width, height = 80, 25
        hearts = [{"x": random.randint(0, width-2), "y": random.randint(-10,0), "speed": random.uniform(0.3,1.5), "heart": random.choice(["❤️","💕","💖","💗","💓"])} for _ in range(15)]
        for _ in range(120):
            grid = [" " * width for _ in range(height)]
            for h in hearts:
                h["y"] += h["speed"]
                if h["y"] > height: h["y"] = -random.randint(1,5); h["x"] = random.randint(0,width-2)
                if 0 <= h["y"] < height:
                    y = int(h["y"]); x = h["x"]; s = h["heart"]
                    if x + len(s) <= width: grid[y] = grid[y][:x] + s + grid[y][x+len(s):]
            falling.update("\n".join(grid))
            await asyncio.sleep(0.08)
        falling.styles.display = "none"

    async def fall_confetti(self):
        conf = self.query_one("#falling_confetti")
        conf.styles.display = "block"
        width, height = 80, 25
        items = [{"x": random.randint(0,width-2), "y": random.randint(-10,0), "speed": random.uniform(0.2,1.2), "s": random.choice(["🎉","🎊","✨","⭐","🌟"])} for _ in range(20)]
        for _ in range(150):
            grid = [" " * width for _ in range(height)]
            for it in items:
                it["y"] += it["speed"]
                if it["y"] > height: it["y"] = -random.randint(1,5); it["x"] = random.randint(0,width-2)
                if 0 <= it["y"] < height:
                    y = int(it["y"]); x = it["x"]
                    if x < width: grid[y] = grid[y][:x] + it["s"] + grid[y][x+1:]
            conf.update("\n".join(grid))
            await asyncio.sleep(0.08)
        conf.styles.display = "none"

    async def fall_sparkles(self):
        sp = self.query_one("#falling_sparkles")
        sp.styles.display = "block"
        width, height = 80, 25
        items = [{"x": random.randint(0,width-2), "y": random.randint(-10,0), "speed": random.uniform(0.15,0.8), "s": random.choice(["✨","💫","⭐","🌟"])} for _ in range(15)]
        for _ in range(120):
            grid = [" " * width for _ in range(height)]
            for it in items:
                it["y"] += it["speed"]
                if it["y"] > height: it["y"] = -random.randint(1,5); it["x"] = random.randint(0,width-2)
                if 0 <= it["y"] < height:
                    y = int(it["y"]); x = it["x"]
                    if x < width: grid[y] = grid[y][:x] + it["s"] + grid[y][x+1:]
            sp.update("\n".join(grid))
            await asyncio.sleep(0.1)
        sp.styles.display = "none"

    async def _show_success_message(self):
        msg = self.query_one("#success_message")
        msg.styles.display = "block"
        text = "✨ YES! YES! YES! ✨\n\n💖 You've made me\nthe luckiest\nperson alive 💖\n\nLet's write\nour story 🌹\n\n❤️ Happy\nValentine's\nDay ❤️"
        out = ""
        for c in text:
            out += c
            msg.update(out)
            await asyncio.sleep(0.03)

    async def flood_with_tears(self):
        tears = self.query_one("#tears_flood")
        tears.styles.display = "block"
        lines = 1
        for h in range(1, 101, 2):
            tears.styles.height = f"{h}%"
            tears.update("\n".join(["😭 💧 😭 💧"] * lines))
            lines += 1
            await asyncio.sleep(0.08)
        tears.styles.display = "none"

    async def type_text(self, message: str):
        display = self.query_one("#message_area")
        s = ""
        for ch in message:
            s += ch
            display.update(s)
            await asyncio.sleep(0.04)

if __name__ == "__main__":
    app = ValentineApp()
    app.run()