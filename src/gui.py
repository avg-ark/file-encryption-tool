import customtkinter as ctk
import tkinter as tk
import random
import math

ctk.set_appearance_mode("dark")


class ArksEncrypPreview(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ark's Encryp")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.width = 1000
        self.height = 650
        self.particles = []
        self.animation_progress = 0
        self.can_click = False
        self.splash_visible = True

        self.canvas = tk.Canvas(self, bg="#020617", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.create_text_particles("Ark's Encryp")
        self.animate_dust()

        self.bind("<Button-1>", self.enter_app)

    def create_text_particles(self, text):
        temp = tk.Canvas(self, width=self.width, height=self.height)
        temp.update()

        font = ("Segoe UI", 72, "bold")
        temp.create_text(
            self.width // 2,
            self.height // 2,
            text=text,
            font=font,
            fill="white"
        )

        self.update()

        # Manually create particle target positions in text-like layout
        target_points = []
        start_x = 250
        start_y = 300

        for i in range(420):
            x = start_x + (i % 70) * 7
            y = start_y + (i // 70) * 10

            # create a rough text cloud band
            if random.random() > 0.25:
                target_points.append((x, y))

        for tx, ty in target_points:
            self.particles.append({
                "x": random.randint(0, self.width),
                "y": random.randint(0, self.height),
                "tx": tx,
                "ty": ty,
                "r": random.uniform(1.5, 3.2),
                "color": random.choice(["#38bdf8", "#60a5fa", "#e0f2fe"]),
                "float": random.uniform(0, math.pi * 2)
            })

    def animate_dust(self):
        self.canvas.delete("all")

        self.animation_progress += 0.006

        if self.animation_progress > 1:
            self.animation_progress = 1
            self.can_click = True

        eased = self.ease_out_cubic(self.animation_progress)

        for p in self.particles:
            float_offset = math.sin(p["float"] + self.animation_progress * 10) * 3

            x = p["x"] + (p["tx"] - p["x"]) * eased
            y = p["y"] + (p["ty"] - p["y"]) * eased + float_offset

            self.canvas.create_oval(
                x,
                y,
                x + p["r"],
                y + p["r"],
                fill=p["color"],
                outline=""
            )

        # Glow title appears gradually after dust forms
        if self.animation_progress > 0.65:
            alpha_text = int((self.animation_progress - 0.65) / 0.35 * 255)
            alpha_text = min(alpha_text, 255)

            self.canvas.create_text(
                self.width // 2,
                290,
                text="Ark's Encryp",
                font=("Segoe UI", 62, "bold"),
                fill="#e0f2fe"
            )

            self.canvas.create_text(
                self.width // 2,
                370,
                text="Secure. Minimal. Encrypted.",
                font=("Segoe UI", 18),
                fill="#94a3b8"
            )

        if self.can_click:
            self.canvas.create_text(
                self.width // 2,
                455,
                text="Click anywhere to begin",
                font=("Segoe UI", 15, "bold"),
                fill="#38bdf8"
            )

        self.after(25, self.animate_dust)

    def ease_out_cubic(self, t):
        return 1 - pow(1 - t, 3)

    def ease_in_out_cubic(self, t):
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2

    def create_main_app(self):
        self.main_frame = ctk.CTkFrame(self, width=1000, height=650, fg_color="#020617")
        self.main_frame.place(x=1000, y=0)

        sidebar = ctk.CTkFrame(self.main_frame, width=230, height=610, corner_radius=25, fg_color="#0f172a")
        sidebar.place(x=25, y=20)

        ctk.CTkLabel(sidebar, text="Ark's Encryp", font=("Segoe UI", 26, "bold")).place(x=30, y=35)

        for i, item in enumerate(["Dashboard", "Encrypt", "Decrypt", "Activity", "Settings"]):
            ctk.CTkButton(
                sidebar,
                text=item,
                width=170,
                height=42,
                corner_radius=14,
                fg_color="#1e293b",
                hover_color="#2563eb"
            ).place(x=30, y=130 + i * 58)

        main_card = ctk.CTkFrame(self.main_frame, width=700, height=610, corner_radius=30, fg_color="#0f172a")
        main_card.place(x=275, y=20)

        ctk.CTkLabel(main_card, text="Secure File Encryption", font=("Segoe UI", 32, "bold")).place(x=40, y=35)

        drop_box = ctk.CTkFrame(
            main_card,
            width=610,
            height=120,
            corner_radius=25,
            fg_color="#111827",
            border_width=2,
            border_color="#1d4ed8"
        )
        drop_box.place(x=45, y=120)

        ctk.CTkLabel(drop_box, text="📂 Drag your file here or browse", font=("Segoe UI", 20, "bold")).place(
            relx=0.5, rely=0.45, anchor="center"
        )

        ctk.CTkButton(drop_box, text="Browse File", width=140, height=36, corner_radius=14).place(
            relx=0.5, rely=0.75, anchor="center"
        )

        ctk.CTkLabel(main_card, text="Access Password", font=("Segoe UI", 14, "bold")).place(x=50, y=275)
        ctk.CTkEntry(main_card, width=520, height=45, corner_radius=14, show="*").place(x=50, y=305)

        ctk.CTkLabel(main_card, text="Encryption Password", font=("Segoe UI", 14, "bold")).place(x=50, y=370)
        ctk.CTkEntry(main_card, width=520, height=45, corner_radius=14, show="*").place(x=50, y=400)

        ctk.CTkButton(main_card, text="Encrypt File", width=170, height=50, corner_radius=18, fg_color="#16a34a").place(x=80, y=520)
        ctk.CTkButton(main_card, text="Decrypt File", width=170, height=50, corner_radius=18, fg_color="#dc2626").place(x=270, y=520)
        ctk.CTkButton(main_card, text="View File", width=170, height=50, corner_radius=18, fg_color="#2563eb").place(x=460, y=520)

    def enter_app(self, event=None):
        if not self.can_click or not self.splash_visible:
            return

        self.splash_visible = False
        self.create_main_app()
        self.slide_step = 0
        self.slide_transition()

    def slide_transition(self):
        self.slide_step += 0.018

        if self.slide_step >= 1:
            self.canvas.destroy()
            self.main_frame.place(x=0, y=0)
            return

        eased = self.ease_in_out_cubic(self.slide_step)

        splash_x = int(-1000 * eased)
        main_x = int(1000 - 1000 * eased)

        self.canvas.place(x=splash_x, y=0)
        self.main_frame.place(x=main_x, y=0)

        self.after(16, self.slide_transition)


if __name__ == "__main__":
    app = ArksEncrypPreview()
    app.mainloop()