import tkinter as tk
from Gen3_Menu import Gen3_Menu

class VentanaPrincipal(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Pokebot")
        self.geometry("500x300+710+390")  # Ajusta según sea necesario

        # Create a canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind the frame's configure event to update the canvas scroll region
        self.scrollable_frame.bind("<Configure>", self.update_scrollregion)

        # Load the title image
        self.image = tk.PhotoImage(file="./Images/Title.png")
        self.title_label = tk.Label(self.scrollable_frame, image=self.image)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)  # Center title

        # Create specific buttons
        self.button1 = tk.Button(self.scrollable_frame, text="Pokemon Sapphire/Ruby/Emerald", command=self.sre_onclick, bg="#313131", fg="white")
        self.button2 = tk.Button(self.scrollable_frame, text="Pokemon Leaf Green/Fire Red", command=lambda: self.on_button_click("Leaf Green/Fire Red"), bg="#313131", fg="white")

        self.button1.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.button2.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # Configure row and column weights for expansion
        self.scrollable_frame.grid_rowconfigure(0, weight=0)  # Title row
        self.scrollable_frame.grid_rowconfigure(1, weight=1)  # First button row
        self.scrollable_frame.grid_rowconfigure(2, weight=1)  # Second button row
        self.scrollable_frame.grid_columnconfigure(0, weight=1)  # Single column

    def update_scrollregion(self, event):
        # Update the scrollregion of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def sre_onclick(self):
        Gen3_Menu()

    def on_button_click(self, button_name):
        # Perform the desired action
        print(f"¡Botón {button_name} clickeado!")

ventana = VentanaPrincipal()
ventana.mainloop()
