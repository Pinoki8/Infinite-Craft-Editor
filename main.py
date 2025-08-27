import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import gzip
import re


class ModernICEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("IC Editor")
        self.root.geometry("900x600")
        self.root.configure(bg="#2a2a2a")
        
        self.colors = {
            'bg_dark': '#2a2a2a',
            'bg_medium': '#3a3a3a',
            'bg_light': '#4a4a4a',
            'accent': '#66d9a6',
            'accent_dark': '#4db88a',
            'text_light': '#ffffff',
            'text_gray': '#cccccc',
            'error': '#ff6b6b',
            'warning': '#ffd93d'
        }
        
        self.content = ""
        self.current_name = ""
        self.crafts = []
        
        self.setup_styles()
        self.create_interface()
        self.open_file()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Modern.TButton',
                           background=self.colors['accent'],
                           foreground='#2a2a2a',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['accent_dark']),
                                ('pressed', self.colors['accent_dark'])])
        
        self.style.configure('Delete.TButton',
                           background=self.colors['error'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Delete.TButton',
                      background=[('active', '#ff5252'),
                                ('pressed', '#ff5252')])
        
        self.style.configure('Vertical.TScrollbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_dark'],
                           bordercolor=self.colors['bg_medium'],
                           arrowcolor=self.colors['bg_dark'],
                           darkcolor=self.colors['accent'],
                           lightcolor=self.colors['accent'])

    def create_interface(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_container, 
                              text="IC Editor", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_dark'])
        title_label.pack(pady=(0, 20))
        
        content_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        content_frame.pack(fill="both", expand=True)
        
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)

    def create_left_panel(self, parent):
        left_panel = tk.Frame(parent, bg=self.colors['bg_medium'], relief='flat', bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        
        header_frame = tk.Frame(left_panel, bg=self.colors['accent'], height=40)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame,
                               text="FILE CONTROLS",
                               font=('Segoe UI', 12, 'bold'),
                               fg='#2a2a2a',
                               bg=self.colors['accent'])
        header_label.pack(expand=True)
        
        content_frame = tk.Frame(left_panel, bg=self.colors['bg_medium'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(content_frame,
                text="Save Name",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(0, 5))
        
        self.save_name_var = tk.StringVar()
        self.save_name_entry = tk.Entry(content_frame,
                                       textvariable=self.save_name_var,
                                       font=('Segoe UI', 10),
                                       bg=self.colors['bg_light'],
                                       fg=self.colors['text_gray'],
                                       insertbackground=self.colors['accent'],
                                       relief='flat',
                                       bd=5,
                                       width=25)
        self.save_name_entry.pack(fill="x", pady=(0, 20))
        
        self.save_name_entry.bind("<FocusIn>", self._clear_placeholder)
        self.save_name_entry.bind("<FocusOut>", self._restore_placeholder)
        
        add_btn = ttk.Button(content_frame,
                            text="+ Add Craft",
                            style='Modern.TButton',
                            command=self.add_craft_dialog)
        add_btn.pack(fill="x", pady=(0, 10))
        
        save_btn = ttk.Button(content_frame,
                             text="💾 Save File",
                             style='Modern.TButton',
                             command=self.save_file)
        save_btn.pack(fill="x")
        
        tk.Label(content_frame,
                text="Statistics",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(30, 5))
        
        self.stats_label = tk.Label(content_frame,
                                   text="Crafts: 0",
                                   font=('Segoe UI', 10),
                                   fg=self.colors['text_gray'],
                                   bg=self.colors['bg_medium'])
        self.stats_label.pack(anchor="w")
        
        watermark_label = tk.Label(content_frame,
                                  text="Made by Pin0ki0",
                                  font=('Segoe UI', 8, 'italic'),
                                  fg=self.colors['accent'],
                                  bg=self.colors['bg_medium'])
        watermark_label.pack(side="bottom", anchor="w", pady=(20, 0))

    def create_right_panel(self, parent):
        right_panel = tk.Frame(parent, bg=self.colors['bg_medium'], relief='flat', bd=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        header_frame = tk.Frame(right_panel, bg=self.colors['accent'], height=40)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame,
                               text="CRAFTS LIST",
                               font=('Segoe UI', 12, 'bold'),
                               fg='#2a2a2a',
                               bg=self.colors['accent'])
        header_label.pack(expand=True)
        
        self.create_scrollable_crafts_area(right_panel)

    def create_scrollable_crafts_area(self, parent):
        canvas_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        canvas_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.canvas = tk.Canvas(canvas_frame, 
                               bg=self.colors['bg_medium'],
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, 
                                 orient="vertical", 
                                 command=self.canvas.yview,
                                 style='Vertical.TScrollbar')
        
        self.crafts_container = tk.Frame(self.canvas, bg=self.colors['bg_medium'])
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.crafts_container, anchor="nw")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.crafts_container.bind("<Configure>", self._on_frame_configure)

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _clear_placeholder(self, event):
        if self.save_name_var.get() == self.current_name and self.save_name_entry.cget("fg") == self.colors['text_gray']:
            self.save_name_entry.delete(0, tk.END)
            self.save_name_entry.config(fg=self.colors['text_light'])

    def _restore_placeholder(self, event):
        if not self.save_name_var.get():
            self.save_name_var.set(self.current_name)
            self.save_name_entry.config(fg=self.colors['text_gray'])

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("IC files", "*.ic")])
        if not file_path:
            self.root.destroy()
            return

        try:
            with gzip.open(file_path, "rb") as f:
                self.content = f.read().decode("utf-8", errors="ignore")

            match = re.search(r'"name":"(.*?)"', self.content)
            self.current_name = match.group(1) if match else "unknown"

            self.save_name_var.set(self.current_name)
            self.save_name_entry.config(fg=self.colors['text_gray'])

            self.update_crafts_list()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file:\n{e}")
            self.root.destroy()

    def update_crafts_list(self):
        for widget in self.crafts_container.winfo_children():
            widget.destroy()

        self.crafts = []

        text_matches = list(re.finditer(r'"text":"(.*?)"', self.content))
        for match in text_matches:
            text_value = match.group(1)

            after_text = self.content[match.end():]
            emoji_match = re.search(r'"emoji":"(.*?)"', after_text)
            emoji_value = emoji_match.group(1) if emoji_match else "❓"

            self.crafts.append((text_value, emoji_value))

        for i, (text_value, emoji_value) in enumerate(self.crafts):
            self.create_craft_item(text_value, emoji_value, i)

        self.stats_label.config(text=f"Crafts: {len(self.crafts)}")
        
        self.crafts_container.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_craft_item(self, text_value, emoji_value, index):
        bg_color = self.colors['bg_light'] if index % 2 == 0 else self.colors['bg_dark']
        
        item_frame = tk.Frame(self.crafts_container, 
                             bg=bg_color, 
                             relief='flat',
                             bd=1,
                             height=50)
        item_frame.pack(fill="x", padx=10, pady=2)
        item_frame.pack_propagate(False)
        
        emoji_label = tk.Label(item_frame,
                              text=emoji_value,
                              font=('Segoe UI', 16),
                              bg=bg_color,
                              width=3)
        emoji_label.pack(side="left", padx=(10, 5), pady=10)
        
        text_label = tk.Label(item_frame,
                             text=text_value,
                             font=('Segoe UI', 11),
                             fg=self.colors['text_light'],
                             bg=bg_color,
                             anchor="w")
        text_label.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)
        
        def on_enter(event):
            item_frame.config(bg=self.colors['accent'])
            emoji_label.config(bg=self.colors['accent'])
            text_label.config(bg=self.colors['accent'], fg='#2a2a2a')
            
        def on_leave(event):
            item_frame.config(bg=bg_color)
            emoji_label.config(bg=bg_color)
            text_label.config(bg=bg_color, fg=self.colors['text_light'])
        
        for widget in [item_frame, emoji_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, t=text_value: self.edit_craft_dialog(t))

    def create_modern_dialog(self, title, width=400, height=300):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.resizable(False, False)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        return dialog

    def add_craft_dialog(self):
        dialog = self.create_modern_dialog("Add New Craft", 450, 470)
        
        content_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = tk.Label(content_frame,
                              text="Add New Craft",
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_medium'])
        title_label.pack(pady=(0, 20))
        
        tk.Label(content_frame,
                text="Craft Name",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(0, 5))
        
        name_entry = tk.Entry(content_frame,
                             font=('Segoe UI', 11),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'],
                             insertbackground=self.colors['accent'],
                             relief='flat',
                             bd=5)
        name_entry.pack(fill="x", pady=(0, 15))
        name_entry.focus()
        
        tk.Label(content_frame,
                text="Emoji",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(0, 5))
        
        emoji_entry = tk.Entry(content_frame,
                              font=('Segoe UI', 11),
                              bg=self.colors['bg_light'],
                              fg=self.colors['text_light'],
                              insertbackground=self.colors['accent'],
                              relief='flat',
                              bd=5)
        emoji_entry.pack(fill="x", pady=(0, 15))
        emoji_entry.insert(0, "🌍")
        
        adv_var = tk.BooleanVar(value=False)
        adv_check = tk.Checkbutton(content_frame,
                                  text="Use Custom ID",
                                  variable=adv_var,
                                  font=('Segoe UI', 10),
                                  fg=self.colors['text_light'],
                                  bg=self.colors['bg_medium'],
                                  selectcolor=self.colors['bg_light'],
                                  activebackground=self.colors['bg_medium'],
                                  activeforeground=self.colors['text_light'])
        adv_check.pack(anchor="w", pady=(10, 5))
        
        id_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        id_frame.pack(fill="x", pady=(0, 15))
        
        id_label = tk.Label(id_frame,
                           text="Custom ID",
                           font=('Segoe UI', 11, 'bold'),
                           fg=self.colors['text_light'],
                           bg=self.colors['bg_medium'])
        
        id_entry = tk.Entry(id_frame,
                           font=('Segoe UI', 11),
                           bg=self.colors['bg_light'],
                           fg=self.colors['text_light'],
                           insertbackground=self.colors['accent'],
                           relief='flat',
                           bd=5)
        
        def toggle_id():
            if adv_var.get():
                id_label.pack(anchor="w", pady=(5, 5))
                id_entry.pack(fill="x")
            else:
                id_label.pack_forget()
                id_entry.pack_forget()
        
        adv_var.trace_add("write", lambda *args: toggle_id())
        
        btn_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        def on_ok():
            name = name_entry.get().strip()
            emoji = emoji_entry.get().strip() or "🌍"
            
            if not name:
                messagebox.showwarning("Warning", "Craft name cannot be empty")
                return
            
            if adv_var.get():
                craft_id = id_entry.get().strip()
                if not craft_id.isdigit():
                    craft_id = "0"
            else:
                all_ids = [int(m.group(1)) for m in re.finditer(r'"id":(\d+)', self.content)]
                craft_id = str(max(all_ids) + 1) if all_ids else "0"
            
            insert_pos = self.content.rfind("]}")
            if insert_pos == -1:
                messagebox.showerror("Error", "Could not find end of crafts array (]}).")
                dialog.destroy()
                return
            
            addition = f',{{"id":{craft_id},"text":"{name}","emoji":"{emoji}"}}'
            self.content = self.content[:insert_pos] + addition + self.content[insert_pos:]
            
            self.update_crafts_list()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        cancel_btn = ttk.Button(btn_frame,
                               text="Cancel",
                               style='Modern.TButton',
                               command=on_cancel)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        ok_btn = ttk.Button(btn_frame,
                           text="Add Craft",
                           style='Modern.TButton',
                           command=on_ok)
        ok_btn.pack(side="right")
        
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())

    def edit_craft_dialog(self, craft_name):
        text_match = re.search(rf'"text":"{re.escape(craft_name)}"', self.content)
        if not text_match:
            messagebox.showerror("Error", f"Craft not found: {craft_name}")
            return

        start = self.content.rfind("{", 0, text_match.start())
        end = self.content.find("}", text_match.end())
        if start == -1 or end == -1:
            messagebox.showerror("Error", "Could not find complete craft block.")
            return

        block = self.content[start:end+1]

        id_match = re.search(r'"id":(\d+)', block)
        text_match = re.search(r'"text":"(.*?)"', block)
        emoji_match = re.search(r'"emoji":"(.*?)"', block)

        craft_id = id_match.group(1) if id_match else "?"
        craft_text = text_match.group(1) if text_match else ""
        craft_emoji = emoji_match.group(1) if emoji_match else "🌍"

        dialog = self.create_modern_dialog("Edit Craft", 450, 400)
        
        content_frame = tk.Frame(dialog, bg=self.colors['bg_medium'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = tk.Label(content_frame,
                              text=f"Edit Craft (ID: {craft_id})",
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_medium'])
        title_label.pack(pady=(0, 20))
        
        tk.Label(content_frame,
                text="Craft Name",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(0, 5))
        
        text_entry = tk.Entry(content_frame,
                             font=('Segoe UI', 11),
                             bg=self.colors['bg_light'],
                             fg=self.colors['text_light'],
                             insertbackground=self.colors['accent'],
                             relief='flat',
                             bd=5)
        text_entry.pack(fill="x", pady=(0, 15))
        text_entry.insert(0, craft_text)
        text_entry.focus()
        text_entry.select_range(0, tk.END)
        
        tk.Label(content_frame,
                text="Emoji",
                font=('Segoe UI', 11, 'bold'),
                fg=self.colors['text_light'],
                bg=self.colors['bg_medium']).pack(anchor="w", pady=(0, 5))
        
        emoji_entry = tk.Entry(content_frame,
                              font=('Segoe UI', 11),
                              bg=self.colors['bg_light'],
                              fg=self.colors['text_light'],
                              insertbackground=self.colors['accent'],
                              relief='flat',
                              bd=5)
        emoji_entry.pack(fill="x", pady=(0, 15))
        emoji_entry.insert(0, craft_emoji)
        
        btn_frame = tk.Frame(content_frame, bg=self.colors['bg_medium'])
        btn_frame.pack(fill="x", pady=(20, 0))
        
        def on_ok():
            new_text = text_entry.get().strip()
            new_emoji = emoji_entry.get().strip() or "🌍"
            
            if not new_text:
                messagebox.showwarning("Warning", "Craft name cannot be empty")
                return
            
            new_block = re.sub(r'"text":".*?"', f'"text":"{new_text}"', block)
            new_block = re.sub(r'"emoji":".*?"', f'"emoji":"{new_emoji}"', new_block)
            
            self.content = self.content[:start] + new_block + self.content[end+1:]
            self.update_crafts_list()
            dialog.destroy()
        
        def on_delete():
            result = messagebox.askyesno("Confirm Delete", 
                                       f"Are you sure you want to delete '{craft_text}'?",
                                       icon='warning')
            if result:
                before = self.content[:start]
                after = self.content[end+1:]
                
                if before.endswith(","):
                    before = before[:-1]
                
                self.content = before + after
                self.update_crafts_list()
                dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        delete_btn = ttk.Button(btn_frame,
                               text="Delete",
                               style='Delete.TButton',
                               command=on_delete)
        delete_btn.pack(side="left")
        
        cancel_btn = ttk.Button(btn_frame,
                               text="Cancel",
                               style='Modern.TButton',
                               command=on_cancel)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        ok_btn = ttk.Button(btn_frame,
                           text="Save Changes",
                           style='Modern.TButton',
                           command=on_ok)
        ok_btn.pack(side="right")
        
        dialog.bind('<Return>', lambda e: on_ok())
        dialog.bind('<Escape>', lambda e: on_cancel())

    def save_file(self):
        new_name = self.save_name_var.get().strip()
        if new_name != self.current_name:
            self.content = re.sub(r'"name":"(.*?)"', f'"name":"{new_name}"', self.content, count=1)
            self.current_name = new_name

        save_path = filedialog.asksaveasfilename(
            defaultextension=".ic", 
            filetypes=[("IC files", "*.ic")]
        )
        if not save_path:
            return

        try:
            with gzip.open(save_path, "wb") as f_out:
                f_out.write(self.content.encode("utf-8"))
            messagebox.showinfo("Success", f"File saved successfully!\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernICEditor(root)
    root.mainloop()