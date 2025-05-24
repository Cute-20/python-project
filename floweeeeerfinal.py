import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from PIL import Image, ImageTk
import sv_ttk  # Modern theme for tkinter

class ModernFlowerInventory:
    def __init__(self, root):
        self.root = root
        self.root.title("BloomTrack - Modern Flower Inventory")
        self.root.geometry("1300x800")
        
        # Set dark theme by default
        sv_ttk.set_theme("dark")
        
        # Custom colors
        self.primary_color = "#7E57C2"  # Deep purple
        self.secondary_color = "#26A69A"  # Teal
        self.accent_color = "#FF7043"  # Deep orange
        self.bg_color = "#121212"  # Dark background
        self.card_color = "#1E1E1E"  # Card background
        self.text_color = "#FFFFFF"  # White text
        
        # Sample initial data
        self.flowers = {
            "Rose": {"quantity": 50, "expiry": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"), 
                    "threshold": 20, "condition": "Fresh", "water_level": 80, "last_watered": datetime.now().strftime("%Y-%m-%d %H:%M"), "price": 2.99},
            "Tulip": {"quantity": 30, "expiry": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"), 
                     "threshold": 15, "condition": "Fresh", "water_level": 60, "last_watered": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), "price": 1.99},
            "Lily": {"quantity": 25, "expiry": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), 
                    "threshold": 10, "condition": "Wilting", "water_level": 20, "last_watered": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "price": 3.49},
            "Orchid": {"quantity": 15, "expiry": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"), 
                      "threshold": 5, "condition": "Fresh", "water_level": 70, "last_watered": datetime.now().strftime("%Y-%m-%d %H:%M"), "price": 4.99},
        "sunflower": {"quantity": 25, "expiry": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"), 
                    "threshold": 10, "condition": "Wilting", "water_level": 20, "last_watered": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "price": 3.49},
        }
        
        self.sales_data = {
            "Rose": [10, 12, 15, 8, 20],
            "Tulip": [5, 8, 6, 10, 7],
            "Lily": [3, 5, 7, 4, 6],
            "Orchid": [2, 3, 4, 5, 2]
        }
        
        self.watering_history = []
        self.sales_history = []
        
        self.setup_ui()
        self.check_alerts()
        
        # Bind theme toggle to F1 key
        self.root.bind("<F1>", self.toggle_theme)
    
    def toggle_theme(self, event=None):
        current_theme = sv_ttk.get_theme()
        new_theme = "light" if current_theme == "dark" else "dark"
        sv_ttk.set_theme(new_theme)
        
        # Update colors based on theme
        if new_theme == "dark":
            self.bg_color = "#121212"
            self.card_color = "#1E1E1E"
            self.text_color = "#FFFFFF"
        else:
            self.bg_color = "#F5F5F5"
            self.card_color = "#FFFFFF"
            self.text_color = "#000000"
        
        # Update UI elements
        self.update_ui_colors()
    
    def update_ui_colors(self):
        # Update background colors
        self.root.configure(bg=self.bg_color)
        for tab in [self.inventory_tab, self.sales_tab, self.analytics_tab, self.watering_tab]:
            tab.configure(style="Custom.TFrame")
        
        # Update treeview styles
        self.style.configure("Treeview", background=self.card_color, fieldbackground=self.card_color, foreground=self.text_color)
        self.style.configure("Treeview.Heading", background=self.primary_color, foreground="white")
        
        # Update button styles
        self.style.configure("TButton", background=self.secondary_color, foreground="white")
        self.style.map("TButton", 
                      background=[('active', self.accent_color), ('!disabled', self.secondary_color)],
                      foreground=[('active', 'white'), ('!disabled', 'white')])
        
        # Update alert frame
        self.alerts_frame.configure(bg="#FFF3E0" if sv_ttk.get_theme() == "light" else "#263238")
        self.alerts_label.configure(bg="#FFF3E0" if sv_ttk.get_theme() == "light" else "#263238")
        
        # Redraw plots with updated colors
        self.update_analytics_plot()
    
    def setup_ui(self):
        # Custom style configuration
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background=self.bg_color)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 5])
        self.style.configure("TButton", font=("Segoe UI", 9), padding=8)
        
        # Header
        self.header = ttk.Frame(self.root, style="Custom.TFrame")
        self.header.pack(fill="x", padx=10, pady=10)
        
        self.title_label = ttk.Label(self.header, text="Blossom Flower Inventory System", font=("Segoe UI", 24, "bold"), 
                                   foreground=self.primary_color, background=self.bg_color)
        self.title_label.pack(side="left")
        
        self.date_label = ttk.Label(self.header, text=datetime.now().strftime("%A, %B %d, %Y"), 
                                   font=("Segoe UI", 10), background=self.bg_color)
        self.date_label.pack(side="right")
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.root, style="TNotebook")
        
        # Inventory Tab
        self.inventory_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.tab_control.add(self.inventory_tab, text="🌷 Inventory")
        self.setup_inventory_tab()
        
        # Sales Tab
        self.sales_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.tab_control.add(self.sales_tab, text="💰 Sales")
        self.setup_sales_tab()
        
        # Analytics Tab
        self.analytics_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.tab_control.add(self.analytics_tab, text="📊 Analytics")
        self.setup_analytics_tab()
        
        # Watering Tab
        self.watering_tab = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.tab_control.add(self.watering_tab, text="💧 Watering")
        self.setup_watering_tab()
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=(0, 10))
        
        # Status bar
        self.status_bar = ttk.Frame(self.root, style="Custom.TFrame", height=25)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_label = ttk.Label(self.status_bar, text="Ready", background=self.bg_color)
        self.status_label.pack(side="left", padx=10)
        
        # Update UI colors based on theme
        self.update_ui_colors()
    
    def setup_inventory_tab(self):
        # Inventory Treeview with modern styling
        columns = ("Flower", "Quantity", "Price", "Condition", "Water Level", "Expiry Date", "Threshold")
        self.inventory_tree = ttk.Treeview(self.inventory_tab, columns=columns, show="headings", selectmode="browse", style="Treeview")
        
        # Configure columns
        col_widths = [120, 80, 80, 100, 100, 120, 100]
        for col, width in zip(columns, col_widths):
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=width, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.inventory_tab, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.inventory_tree.pack(pady=20, padx=10, fill="both", expand=True)
        
        # Update inventory display
        self.update_inventory_display()
        
        # Buttons Frame with modern card styling
        btn_frame = ttk.Frame(self.inventory_tab, style="Card.TFrame")
        btn_frame.pack(pady=10, padx=10, fill="x")
        
        # Action buttons with icons
        buttons = [
            ("➕ Add", self.add_flower),
            ("✏️ Update", self.update_flower),
            ("🗑️ Delete", self.delete_flower),
            ("📦 Restock", self.restock_flowers),
            ("💦 Water All", self.water_all_flowers),
            ("🔄 Refresh", self.refresh_data)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text, command=command, style="TButton")
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            btn_frame.columnconfigure(i, weight=1)
        
        # Alerts Card
        self.alerts_frame = ttk.Frame(self.inventory_tab, style="Alert.TFrame")
        self.alerts_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(self.alerts_frame, text="🚨 Alerts", font=("Segoe UI", 10, "bold"), 
                 background="#263238", foreground="white").pack(pady=5, fill="x")
        
        self.alerts_label = ttk.Label(self.alerts_frame, text="", foreground="white", 
                                     wraplength=600, background="#263238", font=("Segoe UI", 9), 
                                     justify="left")
        self.alerts_label.pack(pady=5, padx=10, fill="x")
        
        # Configure custom styles
        self.style.configure("Card.TFrame", background=self.card_color, borderwidth=1, relief="solid")
        self.style.configure("Alert.TFrame", background="#263238", borderwidth=1, relief="solid")
    
    def setup_watering_tab(self):
        # Watering system controls in a card
        control_card = ttk.Frame(self.watering_tab, style="Card.TFrame")
        control_card.pack(fill="x", pady=10, padx=10)
        
        ttk.Label(control_card, text="💧 Watering Controls", font=("Segoe UI", 12, "bold"), 
                 background=self.card_color).pack(pady=(5, 15), fill="x")
        
        # Flower selection
        flower_frame = ttk.Frame(control_card, style="Custom.TFrame")
        flower_frame.pack(fill="x", pady=5)
        
        ttk.Label(flower_frame, text="Select Flower:", background=self.card_color).pack(side="left", padx=5)
        
        self.water_flower_var = tk.StringVar()
        self.water_flower_dropdown = ttk.Combobox(flower_frame, textvariable=self.water_flower_var, 
                                                values=list(self.flowers.keys()), state="readonly")
        self.water_flower_dropdown.pack(side="left", padx=5, fill="x", expand=True)
        self.water_flower_dropdown.current(0)
        
        # Water amount slider
        slider_frame = ttk.Frame(control_card, style="Custom.TFrame")
        slider_frame.pack(fill="x", pady=5)
        
        ttk.Label(slider_frame, text="Water Amount (%):", background=self.card_color).pack(side="left", padx=5)
        
        self.water_amount_var = tk.IntVar(value=25)
        self.water_amount_slider = ttk.Scale(slider_frame, from_=10, to=100, 
                                            variable=self.water_amount_var, 
                                            command=lambda v: self.water_amount_var.set(round(float(v))))
        self.water_amount_slider.pack(side="left", padx=5, fill="x", expand=True)
        
        # Current water level indicator
        level_frame = ttk.Frame(control_card, style="Custom.TFrame")
        level_frame.pack(fill="x", pady=5)
        
        ttk.Label(level_frame, text="Current Water Level:", background=self.card_color).pack(side="left", padx=5)
        
        self.current_water_level = ttk.Label(level_frame, text="80%", font=("Segoe UI", 9, "bold"), 
                                           background=self.card_color)
        self.current_water_level.pack(side="left", padx=5)
        
        # Water button
        water_btn = ttk.Button(control_card, text="💦 Water Selected", command=self.water_selected_flower,
                             style="Accent.TButton")
        water_btn.pack(pady=10)
        
        # Watering history in a card
        history_card = ttk.Frame(self.watering_tab, style="Card.TFrame")
        history_card.pack(fill="both", expand=True, pady=10, padx=10)
        
        ttk.Label(history_card, text="⏳ Watering History", font=("Segoe UI", 12, "bold"), 
                 background=self.card_color).pack(pady=(5, 10), fill="x")
        
        columns = ("Flower", "Water Amount", "Time", "Result")
        self.watering_tree = ttk.Treeview(history_card, columns=columns, show="headings", height=10, style="Treeview")
        
        for col in columns:
            self.watering_tree.heading(col, text=col)
            self.watering_tree.column(col, width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(history_card, orient="vertical", command=self.watering_tree.yview)
        self.watering_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.watering_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Configure accent button style
        self.style.configure("Accent.TButton", background=self.accent_color, foreground="white")
        self.style.map("Accent.TButton", 
                      background=[('active', self.primary_color), ('!disabled', self.accent_color)])
    
    def water_selected_flower(self):
        flower = self.water_flower_var.get()
        if not flower:
            messagebox.showerror("Error", "Please select a flower")
            return
        
        water_amount = self.water_amount_var.get()
        
        # Update water level
        self.flowers[flower]["water_level"] = min(100, self.flowers[flower]["water_level"] + water_amount)
        
        # Update condition based on water level
        if self.flowers[flower]["water_level"] > 60:
            self.flowers[flower]["condition"] = "Fresh"
        elif self.flowers[flower]["water_level"] > 30:
            self.flowers[flower]["condition"] = "Normal"
        else:
            self.flowers[flower]["condition"] = "Wilting"
        
        # Update last watered time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.flowers[flower]["last_watered"] = current_time
        
        # Add to watering history
        result = "Watered" if water_amount > 20 else "Light watering"
        self.watering_history.append({
            "flower": flower,
            "amount": water_amount,
            "time": current_time,
            "result": result
        })
        
        # Update displays
        self.update_inventory_display()
        self.update_watering_history()
        self.update_analytics_plot()
        
        # Show notification
        self.show_notification(f"Watered {flower} with {water_amount}% water")
    
    def update_watering_history(self):
        # Clear existing data
        for item in self.watering_tree.get_children():
            self.watering_tree.delete(item)
        
        # Add history entries in reverse chronological order
        for entry in reversed(self.watering_history[-50:]):  # Show last 50 entries
            self.watering_tree.insert("", "end", values=(
                entry["flower"],
                f"{entry['amount']}%",
                entry["time"],
                entry["result"]
            ))
    
    def water_all_flowers(self):
        for flower in self.flowers:
            # Add 25% water to all flowers
            self.flowers[flower]["water_level"] = min(100, self.flowers[flower]["water_level"] + 25)
            
            # Update condition
            if self.flowers[flower]["water_level"] > 60:
                self.flowers[flower]["condition"] = "Fresh"
            elif self.flowers[flower]["water_level"] > 30:
                self.flowers[flower]["condition"] = "Normal"
            
            # Update last watered time
            self.flowers[flower]["last_watered"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Add to watering history
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.watering_history.append({
            "flower": "ALL",
            "amount": 25,
            "time": current_time,
            "result": "Batch watered"
        })
        
        self.update_inventory_display()
        self.update_watering_history()
        self.show_notification("All flowers have been watered")
    
    def update_inventory_display(self):
        # Clear existing data
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add current data with color coding for condition
        for flower, data in self.flowers.items():
            condition = data["condition"]
            water_level = data["water_level"]
            
            # Determine tag based on condition
            if condition == "Fresh":
                tag = "fresh"
            elif condition == "Wilting":
                tag = "wilting"
            else:
                tag = "normal"
            
            self.inventory_tree.insert("", "end", values=(
                flower, 
                data["quantity"], 
                f"${data['price']:.2f}",
                condition,
                f"{water_level}%",
                data["expiry"], 
                data["threshold"]
            ), tags=(tag,))
        
        # Update the current water level display if on watering tab
        if hasattr(self, 'water_flower_var'):
            selected_flower = self.water_flower_var.get()
            if selected_flower in self.flowers:
                self.current_water_level.config(
                    text=f"{self.flowers[selected_flower]['water_level']}%",
                    foreground=self.get_water_level_color(self.flowers[selected_flower]['water_level'])
                )
    
    def get_water_level_color(self, level):
        if level > 60:
            return "#4CAF50"  # Green
        elif level > 30:
            return "#FFC107"  # Amber
        else:
            return "#F44336"  # Red
    
    def add_flower(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Flower")
        add_window.geometry("400x450")
        
        # Use theme for the window
        for child in add_window.winfo_children():
            child.destroy()
        
        frame = ttk.Frame(add_window, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Add New Flower", font=("Segoe UI", 14, "bold"), 
                 background=self.card_color).pack(pady=10)
        
        # Form fields
        fields = [
            ("Flower Name:", "entry", ""),
            ("Initial Quantity:", "spinbox", (0, 1000, 50)),
            ("Price ($):", "spinbox_float", (0.01, 100, 2.99)),
            ("Expiry Date (YYYY-MM-DD):", "entry", datetime.now().strftime("%Y-%m-%d")),
            ("Restock Threshold:", "spinbox", (1, 100, 20))
        ]
        
        self.form_vars = []
        for i, (label, field_type, default) in enumerate(fields):
            ttk.Label(frame, text=label, background=self.card_color).pack(pady=(10, 0))
            
            if field_type == "entry":
                var = tk.StringVar(value=default)
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(fill="x", padx=20)
            elif field_type == "spinbox":
                var = tk.IntVar(value=default[2])
                spinbox = ttk.Spinbox(frame, from_=default[0], to=default[1], textvariable=var)
                spinbox.pack(fill="x", padx=20)
            elif field_type == "spinbox_float":
                var = tk.DoubleVar(value=default[2])
                spinbox = ttk.Spinbox(frame, from_=default[0], to=default[1], increment=0.5, textvariable=var)
                spinbox.pack(fill="x", padx=20)
            
            self.form_vars.append(var)
        
        def save_flower():
            name = self.form_vars[0].get()
            if name in self.flowers:
                messagebox.showerror("Error", "Flower already exists!")
                return
            
            try:
                quantity = int(self.form_vars[1].get())
                price = float(self.form_vars[2].get())
                expiry = self.form_vars[3].get()
                threshold = int(self.form_vars[4].get())
                
                # Validate date format
                datetime.strptime(expiry, "%Y-%m-%d")
                
                self.flowers[name] = {
                    "quantity": quantity,
                    "price": price,
                    "expiry": expiry,
                    "threshold": threshold,
                    "condition": "Fresh",
                    "water_level": 50,
                    "last_watered": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                # Initialize sales data
                self.sales_data[name] = [0] * 5
                
                self.update_inventory_display()
                self.update_analytics_plot()
                add_window.destroy()
                self.show_notification("Flower added successfully!")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        save_btn = ttk.Button(frame, text="Save Flower", command=save_flower, style="Accent.TButton")
        save_btn.pack(pady=20)
    
    def update_flower(self):
        selected = self.inventory_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a flower to update")
            return
        
        flower = self.inventory_tree.item(selected)["values"][0]
        data = self.flowers[flower]
        
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update {flower}")
        update_window.geometry("400x450")
        
        # Use theme for the window
        for child in update_window.winfo_children():
            child.destroy()
        
        frame = ttk.Frame(update_window, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text=f"Update {flower}", font=("Segoe UI", 14, "bold"), 
                 background=self.card_color).pack(pady=10)
        
        # Form fields
        fields = [
            ("Quantity:", "spinbox", (0, 1000, data["quantity"])),
            ("Price ($):", "spinbox_float", (0.01, 100, data["price"])),
            ("Expiry Date (YYYY-MM-DD):", "entry", data["expiry"]),
            ("Restock Threshold:", "spinbox", (1, 100, data["threshold"]))
        ]
        
        self.update_vars = []
        for i, (label, field_type, default) in enumerate(fields):
            ttk.Label(frame, text=label, background=self.card_color).pack(pady=(10, 0))
            
            if field_type == "entry":
                var = tk.StringVar(value=default)
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(fill="x", padx=20)
            elif field_type == "spinbox":
                var = tk.IntVar(value=default[2])
                spinbox = ttk.Spinbox(frame, from_=default[0], to=default[1], textvariable=var)
                spinbox.pack(fill="x", padx=20)
            elif field_type == "spinbox_float":
                var = tk.DoubleVar(value=default[2])
                spinbox = ttk.Spinbox(frame, from_=default[0], to=default[1], increment=0.5, textvariable=var)
                spinbox.pack(fill="x", padx=20)
            
            self.update_vars.append(var)
        
        def save_changes():
            try:
                quantity = int(self.update_vars[0].get())
                price = float(self.update_vars[1].get())
                expiry = self.update_vars[2].get()
                threshold = int(self.update_vars[3].get())
                
                # Validate date format
                datetime.strptime(expiry, "%Y-%m-%d")
                
                self.flowers[flower] = {
                    "quantity": quantity,
                    "price": price,
                    "expiry": expiry,
                    "threshold": threshold,
                    "condition": data["condition"],
                    "water_level": data["water_level"],
                    "last_watered": data["last_watered"]
                }
                
                self.update_inventory_display()
                self.check_alerts()
                update_window.destroy()
                self.show_notification("Flower updated successfully!")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        save_btn = ttk.Button(frame, text="Save Changes", command=save_changes, style="Accent.TButton")
        save_btn.pack(pady=20)
    
    def delete_flower(self):
        selected = self.inventory_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a flower to delete")
            return
        
        flower = self.inventory_tree.item(selected)["values"][0]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {flower}?", icon="warning"):
            del self.flowers[flower]
            del self.sales_data[flower]
            self.update_inventory_display()
            self.update_analytics_plot()
            self.show_notification(f"{flower} has been deleted")
    
    def restock_flowers(self):
        restock_window = tk.Toplevel(self.root)
        restock_window.title("Restock Flowers")
        restock_window.geometry("500x400")
        
        # Use theme for the window
        for child in restock_window.winfo_children():
            child.destroy()
        
        frame = ttk.Frame(restock_window, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Restock Flowers", font=("Segoe UI", 14, "bold"), 
                 background=self.card_color).pack(pady=10)
        
        # Listbox to show flowers needing restock
        list_frame = ttk.Frame(frame, style="Custom.TFrame")
        list_frame.pack(fill="both", expand=True, pady=10)
        
        self.restock_listbox = tk.Listbox(list_frame, bg=self.card_color, fg=self.text_color, 
                                        selectbackground=self.primary_color, selectforeground="white",
                                        font=("Segoe UI", 10))
        self.restock_listbox.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.restock_listbox.yview)
        self.restock_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Find flowers that need restocking (quantity <= threshold)
        self.need_restock = []
        for flower, data in self.flowers.items():
            if data["quantity"] <= data["threshold"]:
                self.need_restock.append(flower)
                self.restock_listbox.insert("end", 
                                          f"{flower} (Current: {data['quantity']}, Threshold: {data['threshold']})")
        
        if not self.need_restock:
            self.restock_listbox.insert("end", "No flowers currently need restocking!")
            self.restock_listbox.config(state="disabled")
            return
        
        # Restock quantity controls
        control_frame = ttk.Frame(frame, style="Custom.TFrame")
        control_frame.pack(fill="x", pady=10)
        
        ttk.Label(control_frame, text="Restock Quantity:", background=self.card_color).pack(side="left", padx=5)
        
        self.restock_qty_var = tk.IntVar(value=50)
        self.restock_qty = ttk.Spinbox(control_frame, from_=1, to=1000, textvariable=self.restock_qty_var)
        self.restock_qty.pack(side="left", padx=5, fill="x", expand=True)
        
        def perform_restock():
            selected = self.restock_listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "Please select a flower to restock")
                return
            
            flower = self.need_restock[selected[0]]
            quantity = self.restock_qty_var.get()
            
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
            
            self.flowers[flower]["quantity"] += quantity
            self.update_inventory_display()
            self.check_alerts()
            restock_window.destroy()
            self.show_notification(f"Restocked {flower} with {quantity} units")
        
        restock_btn = ttk.Button(frame, text="🔄 Restock Selected", command=perform_restock, style="Accent.TButton")
        restock_btn.pack(pady=10)
    
    def setup_sales_tab(self):
        # Sales Entry Card
        entry_card = ttk.Frame(self.sales_tab, style="Card.TFrame")
        entry_card.pack(fill="x", pady=10, padx=10)
        
        ttk.Label(entry_card, text="💵 Record Sale", font=("Segoe UI", 12, "bold"), 
                 background=self.card_color).pack(pady=(5, 15), fill="x")
        
        # Sales entry form
        form_frame = ttk.Frame(entry_card, style="Custom.TFrame")
        form_frame.pack(fill="x", pady=5)
        
        ttk.Label(form_frame, text="Flower:", background=self.card_color).grid(row=0, column=0, padx=5, sticky="w")
        self.flower_var = tk.StringVar()
        self.flower_dropdown = ttk.Combobox(form_frame, textvariable=self.flower_var, 
                                          values=list(self.flowers.keys()), state="readonly")
        self.flower_dropdown.grid(row=0, column=1, padx=5, sticky="ew")
        self.flower_dropdown.current(0)
        
        ttk.Label(form_frame, text="Quantity:", background=self.card_color).grid(row=0, column=2, padx=5, sticky="w")
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_entry = ttk.Spinbox(form_frame, from_=1, to=100, textvariable=self.quantity_var, width=8)
        self.quantity_entry.grid(row=0, column=3, padx=5, sticky="ew")
        
        record_btn = ttk.Button(form_frame, text="💾 Record Sale", command=self.record_sale, style="Accent.TButton")
        record_btn.grid(row=0, column=4, padx=5, sticky="ew")
        
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)
        
        # Sales History Card
        history_card = ttk.Frame(self.sales_tab, style="Card.TFrame")
        history_card.pack(fill="both", expand=True, pady=10, padx=10)
        
        ttk.Label(history_card, text="📜 Sales History", font=("Segoe UI", 12, "bold"), 
                 background=self.card_color).pack(pady=(5, 10), fill="x")
        
        columns = ("Date", "Flower", "Quantity", "Price", "Total", "Condition")
        self.sales_tree = ttk.Treeview(history_card, columns=columns, show="headings", height=15, style="Treeview")
        
        col_widths = [150, 120, 80, 80, 100, 100]
        for col, width in zip(columns, col_widths):
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=width, anchor="center")
        
        scrollbar = ttk.Scrollbar(history_card, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.sales_tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Update sales history display
        self.update_sales_history()
        
        # Demand Prediction Button
        predict_btn = ttk.Button(history_card, text="🔮 Predict Demand", command=self.show_demand_prediction,
                               style="Accent.TButton")
        predict_btn.pack(pady=10)
    
    def record_sale(self):
        flower = self.flower_var.get()
        if not flower:
            messagebox.showerror("Error", "Please select a flower")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
                
            if self.flowers[flower]["quantity"] < quantity:
                messagebox.showerror("Error", "Not enough stock available")
                return
                
            # Update inventory
            self.flowers[flower]["quantity"] -= quantity
            
            # Update sales data (keeping last 5 days)
            self.sales_data[flower].append(quantity)
            if len(self.sales_data[flower]) > 5:
                self.sales_data[flower] = self.sales_data[flower][-5:]
            
            # Record sale in history
            price = self.flowers[flower]["price"]
            total = price * quantity
            condition = self.flowers[flower]["condition"]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            self.sales_history.append({
                "date": current_time,
                "flower": flower,
                "quantity": quantity,
                "price": price,
                "total": total,
                "condition": condition
            })
            
            # Update displays
            self.update_inventory_display()
            self.update_sales_history()
            self.update_analytics_plot()
            self.check_alerts()
            
            # Show notification
            self.show_notification(f"Recorded sale: {quantity} {flower}(s) for ${total:.2f}")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity entered")
    
    def update_sales_history(self):
        # Clear existing data
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Add sales entries in reverse chronological order
        for entry in reversed(self.sales_history[-50:]):  # Show last 50 entries
            self.sales_tree.insert("", "end", values=(
                entry["date"],
                entry["flower"],
                entry["quantity"],
                f"${entry['price']:.2f}",
                f"${entry['total']:.2f}",
                entry["condition"]
            ))
    
    def show_demand_prediction(self):
        # Simple demand prediction based on recent sales
        predictions = {}
        for flower, sales in self.sales_data.items():
            avg_sales = sum(sales) / len(sales)
            predictions[flower] = round(avg_sales * 1.2)  # Predict 20% higher than average
        
        # Show prediction in a new window
        predict_window = tk.Toplevel(self.root)
        predict_window.title("Demand Prediction")
        predict_window.geometry("400x300")
        
        frame = ttk.Frame(predict_window, style="Card.TFrame")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="📈 Demand Prediction", font=("Segoe UI", 14, "bold"), 
                 background=self.card_color).pack(pady=10)
        
        text = tk.Text(frame, wrap="word", bg=self.card_color, fg=self.text_color,
                      font=("Segoe UI", 10), padx=10, pady=10)
        text.pack(fill="both", expand=True)
        
        text.insert("end", "Predicted demand for next period:\n\n")
        for flower, pred in predictions.items():
            text.insert("end", f"• {flower}: {pred} units\n")
        
        text.config(state="disabled")
        
        # Add button to auto-adjust inventory
        ttk.Button(frame, text="🔄 Auto-Adjust Inventory", 
                  command=lambda: self.auto_adjust_inventory(predictions),
                  style="Accent.TButton").pack(pady=10)
    
    def auto_adjust_inventory(self, predictions):
        adjustments = []
        
        for flower, pred in predictions.items():
            current = self.flowers[flower]["quantity"]
            threshold = self.flowers[flower]["threshold"]
            
            if current < pred:
                needed = pred - current
                self.flowers[flower]["quantity"] += needed
                adjustments.append(f"➕ Added {needed} {flower}(s) to meet predicted demand")
            elif current > pred * 1.5:  # If we have much more than needed
                excess = current - pred
                adjustments.append(f"⚠️ Consider reducing {flower} stock (current: {current}, predicted need: {pred})")
        
        if adjustments:
            # Show summary of adjustments
            summary_window = tk.Toplevel(self.root)
            summary_window.title("Inventory Adjustment Summary")
            summary_window.geometry("500x300")
            
            frame = ttk.Frame(summary_window, style="Card.TFrame")
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            ttk.Label(frame, text="Inventory Adjustments", font=("Segoe UI", 14, "bold"), 
                     background=self.card_color).pack(pady=10)
            
            text = tk.Text(frame, wrap="word", bg=self.card_color, fg=self.text_color,
                          font=("Segoe UI", 10), padx=10, pady=10)
            text.pack(fill="both", expand=True)
            
            for adj in adjustments:
                text.insert("end", f"• {adj}\n")
            
            text.config(state="disabled")
            
            ttk.Button(frame, text="Close", command=summary_window.destroy,
                      style="Accent.TButton").pack(pady=10)
        else:
            messagebox.showinfo("Info", "No inventory adjustments needed based on predictions")
        
        self.update_inventory_display()
        self.check_alerts()
        self.show_notification("Inventory adjusted based on demand predictions")

    def setup_analytics_tab(self):
        # Analytics Frame with tabs
        self.analytics_notebook = ttk.Notebook(self.analytics_tab)
        self.analytics_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Stock Analytics Tab
        stock_tab = ttk.Frame(self.analytics_notebook, style="Custom.TFrame")
        self.analytics_notebook.add(stock_tab, text="📦 Stock Levels")
        
        # Create figure for stock analytics
        self.stock_fig, self.stock_ax = plt.subplots(figsize=(10, 5))
        self.stock_fig.patch.set_facecolor(self.bg_color)
        
        self.stock_canvas = FigureCanvasTkAgg(self.stock_fig, master=stock_tab)
        self.stock_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Sales Analytics Tab
        sales_tab = ttk.Frame(self.analytics_notebook, style="Custom.TFrame")
        self.analytics_notebook.add(sales_tab, text="💰 Sales Trends")
        
        # Create figure for sales analytics
        self.sales_fig, self.sales_ax = plt.subplots(figsize=(10, 5))
        self.sales_fig.patch.set_facecolor(self.bg_color)
        
        self.sales_canvas = FigureCanvasTkAgg(self.sales_fig, master=sales_tab)
        self.sales_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Watering Analytics Tab
        water_tab = ttk.Frame(self.analytics_notebook, style="Custom.TFrame")
        self.analytics_notebook.add(water_tab, text="💧 Watering History")
        
        # Create figure for watering analytics
        self.water_fig, self.water_ax = plt.subplots(figsize=(10, 5))
        self.water_fig.patch.set_facecolor(self.bg_color)
        
        self.water_canvas = FigureCanvasTkAgg(self.water_fig, master=water_tab)
        self.water_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial plots
        self.update_analytics_plot()

    def update_analytics_plot(self):
        # Update stock levels plot
        self.stock_ax.clear()
        
        flowers = list(self.flowers.keys())
        quantities = [data["quantity"] for data in self.flowers.values()]
        thresholds = [data["threshold"] for data in self.flowers.values()]
        
        x = range(len(flowers))
        bar_width = 0.35
        
        # Stock levels bars
        bars = self.stock_ax.bar(x, quantities, bar_width, color=self.primary_color, label='Current Stock')
        threshold_bars = self.stock_ax.bar([i + bar_width for i in x], thresholds, bar_width, 
                                         color=self.secondary_color, label='Restock Threshold')
        
        self.stock_ax.set_title("Current Stock vs Restock Threshold", color=self.text_color)
        self.stock_ax.set_xticks([i + bar_width / 2 for i in x])
        self.stock_ax.set_xticklabels(flowers, rotation=45, ha="right")
        self.stock_ax.legend()
        
        # Add value labels on bars
        for bar in bars + threshold_bars:
            height = bar.get_height()
            self.stock_ax.text(bar.get_x() + bar.get_width()/2., height,
                              f'{int(height)}',
                              ha='center', va='bottom', color=self.text_color)
        
        # Style the plot
        self.stock_ax.set_facecolor(self.card_color)
        for spine in self.stock_ax.spines.values():
            spine.set_edgecolor(self.text_color)
        self.stock_ax.tick_params(colors=self.text_color)
        self.stock_ax.yaxis.label.set_color(self.text_color)
        self.stock_ax.xaxis.label.set_color(self.text_color)
        self.stock_ax.title.set_color(self.text_color)
        
        self.stock_fig.tight_layout()
        self.stock_canvas.draw()
        
        # Update sales trends plot
        self.sales_ax.clear()
        
        # Prepare sales data for the last 5 days
        days = [f"Day {i}" for i in range(1, 6)]
        
        for flower, sales in self.sales_data.items():
            self.sales_ax.plot(days, sales[-5:], marker='o', label=flower)
        
        self.sales_ax.set_title("Sales Trends (Last 5 Days)", color=self.text_color)
        self.sales_ax.legend()
        self.sales_ax.grid(True, linestyle='--', alpha=0.7)
        
        # Style the plot
        self.sales_ax.set_facecolor(self.card_color)
        for spine in self.sales_ax.spines.values():
            spine.set_edgecolor(self.text_color)
        self.sales_ax.tick_params(colors=self.text_color)
        self.sales_ax.yaxis.label.set_color(self.text_color)
        self.sales_ax.xaxis.label.set_color(self.text_color)
        self.sales_ax.title.set_color(self.text_color)
        
        self.sales_fig.tight_layout()
        self.sales_canvas.draw()
        
        # Update watering history plot
        self.water_ax.clear()
        
        if self.watering_history:
            # Prepare data for last 7 days
            today = datetime.now()
            dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
            flower_counts = {flower: [0]*7 for flower in self.flowers.keys()}
            
            for entry in self.watering_history[-50:]:  # Consider last 50 entries
                entry_date = datetime.strptime(entry["time"], "%Y-%m-%d %H:%M")
                for i, date in enumerate(dates):
                    if entry_date.date() == date.date():
                        flower_counts[entry["flower"]][i] += 1
                        break
            
            bottom = [0]*7
            for flower in self.flowers.keys():
                counts = flower_counts[flower]
                if sum(counts) > 0:  # Only show flowers with watering activity
                    self.water_ax.bar([d.strftime("%a") for d in dates], counts, 
                                     bottom=bottom, label=flower)
                    bottom = [bottom[j] + counts[j] for j in range(7)]
            
            self.water_ax.set_title("Watering Activity (Last 7 Days)", color=self.text_color)
            self.water_ax.legend()
        
        # Style the plot
        self.water_ax.set_facecolor(self.card_color)
        for spine in self.water_ax.spines.values():
            spine.set_edgecolor(self.text_color)
        self.water_ax.tick_params(colors=self.text_color)
        self.water_ax.yaxis.label.set_color(self.text_color)
        self.water_ax.xaxis.label.set_color(self.text_color)
        self.water_ax.title.set_color(self.text_color)
        
        self.water_fig.tight_layout()
        self.water_canvas.draw()

    def check_alerts(self):
        alerts = []
        today = datetime.now()
        
        # Check expiry alerts
        for flower, data in self.flowers.items():
            expiry_date = datetime.strptime(data["expiry"], "%Y-%m-%d")
            days_left = (expiry_date - today).days
            
            if days_left <= 0:
                alerts.append(f"⛔ {flower} has expired!")
            elif days_left <= 2:
                alerts.append(f"⚠️ {flower} expires in {days_left} day(s)")
        
        # Check low stock alerts
        for flower, data in self.flowers.items():
            if data["quantity"] <= data["threshold"]:
                alerts.append(f"📉 {flower} stock is low ({data['quantity']} left, threshold: {data['threshold']})")
        
        # Check water alerts
        for flower, data in self.flowers.items():
            if data["water_level"] < 20:
                alerts.append(f"💧 CRITICAL: {flower} needs immediate watering! (Level: {data['water_level']}%)")
            elif data["water_level"] < 40:
                alerts.append(f"💧 Warning: {flower} needs watering soon (Level: {data['water_level']}%)")
        
        if alerts:
            self.alerts_label.config(text="\n".join(alerts), foreground="white")
        else:
            self.alerts_label.config(text="✅ No alerts at this time", foreground="#4CAF50")

    def show_notification(self, message):
        self.status_label.config(text=message)
        self.root.after(5000, lambda: self.status_label.config(text="Ready"))

    def refresh_data(self):
        self.update_inventory_display()
        self.update_sales_history()
        self.update_analytics_plot()
        self.check_alerts()
        self.show_notification("Data refreshed")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFlowerInventory(root)
    root.mainloop()