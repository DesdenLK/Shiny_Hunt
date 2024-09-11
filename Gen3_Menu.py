import tkinter as tk
from PIL import Image, ImageTk
from modules.Games.RZ import RZ

class Gen3_Menu(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grab_set()
        self.title("Pokebot")
        self.geometry("500x300+710+390")

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
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

        # Create labels and buttons
        self.ruby_label = tk.Label(self.scrollable_frame, text="Ruby", font=("Helvetica", 16), fg="red")
        self.button1 = tk.Button(self.scrollable_frame, text="Treecko Hunt", command=lambda: self.starter_RZ(Zafiro=0, starter=1), bg="lightgreen", fg="white")
        self.button2 = tk.Button(self.scrollable_frame, text="Torchic Hunt", command=lambda: self.starter_RZ(Zafiro=0, starter=2), bg="red", fg="white")
        self.button3 = tk.Button(self.scrollable_frame, text="Mudkip Hunt", command=lambda: self.starter_RZ(Zafiro=0, starter=3), bg="lightblue", fg="white")
        self.back_button = tk.Button(self.scrollable_frame, text="Back", command=self.destroy, bg="#313131", fg="white")

        self.sapphire_label = tk.Label(self.scrollable_frame, text="Sapphire", font=("Helvetica", 16), fg="blue")
        self.button4 = tk.Button(self.scrollable_frame, text="Treecko Hunt", command=self.dummy_command, bg="lightgreen", fg="white")
        self.button5 = tk.Button(self.scrollable_frame, text="Torchic Hunt", command=self.dummy_command, bg="red", fg="white")
        self.button6 = tk.Button(self.scrollable_frame, text="Mudkip Hunt", command=self.dummy_command, bg="lightblue", fg="white")
        

        self.emerald_label = tk.Label(self.scrollable_frame, text="Emerald", font=("Helvetica", 16), fg="green")
        self.button7 = tk.Button(self.scrollable_frame, text="Treecko Hunt", command=self.dummy_command, bg="lightgreen", fg="white")
        self.button8 = tk.Button(self.scrollable_frame, text="Torchic Hunt", command=self.dummy_command, bg="red", fg="white")
        self.button9 = tk.Button(self.scrollable_frame, text="Mudkip Hunt", command=self.dummy_command, bg="lightblue", fg="white")


        # Add widgets to the grid
        self.ruby_label.grid(row=1, column=0, padx=10, pady=10)
        self.button1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.button2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.button3.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.back_button.grid(row=5, column=1, padx=10, pady=10)

        # Add widgets to the grid
        self.sapphire_label.grid(row=1, column=1, padx=10, pady=10)
        self.button4.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.button5.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.button6.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

         # Add widgets to the grid
        self.emerald_label.grid(row=1, column=2, padx=10, pady=10)
        self.button7.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        self.button8.grid(row=3, column=2, padx=10, pady=10, sticky="ew")
        self.button9.grid(row=4, column=2, padx=10, pady=10, sticky="ew")
        

        # Configure row and column weights for expansion
        self.scrollable_frame.grid_rowconfigure(0, weight=0)  # Title row
        self.scrollable_frame.grid_rowconfigure(1, weight=0)  # Buttons row
        self.scrollable_frame.grid_rowconfigure(2, weight=1)  # Buttons row
        self.scrollable_frame.grid_rowconfigure(3, weight=0)  # Back button row

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

    def update_scrollregion(self, event):
        # Update the scrollregion of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def dummy_command(self):
        # Placeholder command for buttons
        print("Button clicked!")

    def starter_RZ(self, Zafiro, starter):
        try:
            game = None
            if Zafiro: game = RZ(1)
            else: game = RZ(0)

            game.starter_hunt(starter)
        except Exception as e:
            self.destroy()




#ventana = VentanaSecundaria()
#ventana.mainloop()
