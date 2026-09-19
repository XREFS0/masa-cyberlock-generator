"""
MASA CyberLock: Advanced Cryptographic Key & Password Generator
Developer: MASA
"""

import secrets
import string
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaCyberLock(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MASA CyberLock Generator")
        self.geometry("480x600")
        self.resizable(False, False)
        self.configure(fg_color="#090D16")

        self.var_upper = ctk.BooleanVar(value=True)
        self.var_lower = ctk.BooleanVar(value=True)
        self.var_digits = ctk.BooleanVar(value=True)
        self.var_symbols = ctk.BooleanVar(value=True)
        self.var_length = ctk.IntVar(value=16)

        self._build_ui()
        self._generate()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#121829", corner_radius=14)
        header.pack(fill="x", padx=20, pady=(20, 15))

        title = ctk.CTkLabel(
            header,
            text="MASA CYBERLOCK GENERATOR",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color="#06B6D4",
        )
        title.pack(pady=(12, 2))

        subtitle = ctk.CTkLabel(
            header,
            text="Cryptographically Secure Entropy Engine",
            font=ctk.CTkFont(size=11),
            text_color="#94A3B8",
        )
        subtitle.pack(pady=(0, 12))

        output_card = ctk.CTkFrame(self, fg_color="#121829", corner_radius=16)
        output_card.pack(fill="x", padx=20, pady=5)

        self.pass_entry = ctk.CTkEntry(
            output_card,
            font=ctk.CTkFont(family="Consolas", size=17, weight="bold"),
            justify="center",
            height=46,
            corner_radius=10,
            border_color="#1E293B",
            fg_color="#090D16",
        )
        self.pass_entry.pack(fill="x", padx=16, pady=(16, 10))

        meter_row = ctk.CTkFrame(output_card, fg_color="transparent")
        meter_row.pack(fill="x", padx=16, pady=(0, 14))

        self.strength_bar = ctk.CTkProgressBar(meter_row, height=8, corner_radius=4, progress_color="#10B981")
        self.strength_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.strength_lbl = ctk.CTkLabel(
            meter_row,
            text="Very Strong",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#10B981",
        )
        self.strength_lbl.pack(side="right")

        opts_card = ctk.CTkFrame(self, fg_color="#121829", corner_radius=16)
        opts_card.pack(fill="both", expand=True, padx=20, pady=(10, 15))

        slider_header = ctk.CTkFrame(opts_card, fg_color="transparent")
        slider_header.pack(fill="x", padx=16, pady=(14, 5))

        lbl_len_title = ctk.CTkLabel(slider_header, text="PASSWORD LENGTH", font=ctk.CTkFont(size=11, weight="bold"), text_color="#94A3B8")
        lbl_len_title.pack(side="left")

        self.lbl_len_val = ctk.CTkLabel(slider_header, text="16", font=ctk.CTkFont(size=13, weight="bold"), text_color="#06B6D4")
        self.lbl_len_val.pack(side="right")

        self.slider = ctk.CTkSlider(
            opts_card,
            from_=6,
            to=48,
            number_of_steps=42,
            variable=self.var_length,
            command=self._on_slider_change,
            progress_color="#06B6D4",
        )
        self.slider.pack(fill="x", padx=16, pady=(0, 12))

        checks_grid = ctk.CTkFrame(opts_card, fg_color="transparent")
        checks_grid.pack(fill="x", padx=16, pady=5)
        checks_grid.grid_columnconfigure((0, 1), weight=1)

        self._add_checkbox(checks_grid, "Uppercase (A-Z)", self.var_upper, 0, 0)
        self._add_checkbox(checks_grid, "Lowercase (a-z)", self.var_lower, 0, 1)
        self._add_checkbox(checks_grid, "Numbers (0-9)", self.var_digits, 1, 0)
        self._add_checkbox(checks_grid, "Symbols (!@#$)", self.var_symbols, 1, 1)

        actions_row = ctk.CTkFrame(self, fg_color="transparent")
        actions_row.pack(fill="x", padx=20, pady=(0, 20))
        actions_row.grid_columnconfigure((0, 1), weight=1)

        btn_gen = ctk.CTkButton(
            actions_row,
            text="Generate Key",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0891B2",
            hover_color="#0E7490",
            height=42,
            corner_radius=10,
            command=self._generate,
        )
        btn_gen.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        btn_copy = ctk.CTkButton(
            actions_row,
            text="Copy Key",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1E293B",
            hover_color="#334155",
            height=42,
            corner_radius=10,
            command=self._copy_password,
        )
        btn_copy.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _add_checkbox(self, parent, text, var, r, c):
        cb = ctk.CTkCheckBox(
            parent,
            text=text,
            variable=var,
            font=ctk.CTkFont(size=12),
            text_color="#E2E8F0",
            fg_color="#0891B2",
            hover_color="#0E7490",
            command=self._generate,
        )
        cb.grid(row=r, column=c, padx=5, pady=8, sticky="w")

    def _on_slider_change(self, val):
        self.lbl_len_val.configure(text=str(int(val)))
        self._generate()

    def _generate(self):
        pool = ""
        mandatory = []

        if self.var_upper.get():
            pool += string.ascii_uppercase
            mandatory.append(secrets.choice(string.ascii_uppercase))
        if self.var_lower.get():
            pool += string.ascii_lowercase
            mandatory.append(secrets.choice(string.ascii_lowercase))
        if self.var_digits.get():
            pool += string.digits
            mandatory.append(secrets.choice(string.digits))
        if self.var_symbols.get():
            special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            pool += special
            mandatory.append(secrets.choice(special))

        length = int(self.var_length.get())

        if not pool:
            self.pass_entry.delete(0, "end")
            self.pass_entry.insert(0, "Select at least 1 set")
            self.strength_bar.set(0)
            self.strength_lbl.configure(text="None", text_color="#EF4444")
            return

        remaining = max(0, length - len(mandatory))
        generated = mandatory + [secrets.choice(pool) for _ in range(remaining)]
        secrets.SystemRandom().shuffle(generated)
        pw_str = "".join(generated[:length])

        self.pass_entry.delete(0, "end")
        self.pass_entry.insert(0, pw_str)

        # Assess entropy strength
        entropy_pts = len(mandatory) * 20 + min(length * 2, 40)
        prog = min(1.0, entropy_pts / 100.0)
        self.strength_bar.set(prog)

        if prog > 0.8:
            self.strength_lbl.configure(text="Military Grade", text_color="#10B981")
            self.strength_bar.configure(progress_color="#10B981")
        elif prog > 0.5:
            self.strength_lbl.configure(text="Robust", text_color="#38BDF8")
            self.strength_bar.configure(progress_color="#38BDF8")
        else:
            self.strength_lbl.configure(text="Moderate / Weak", text_color="#F59E0B")
            self.strength_bar.configure(progress_color="#F59E0B")

    def _copy_password(self):
        val = self.pass_entry.get()
        if val and "Select" not in val:
            self.clipboard_clear()
            self.clipboard_append(val)
            self.strength_lbl.configure(text="Copied to clipboard!", text_color="#38BDF8")


if __name__ == "__main__":
    app = MasaCyberLock()
    app.mainloop()
