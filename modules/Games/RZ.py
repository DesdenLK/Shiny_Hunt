import time
import pyfiglet
from colorama import Fore, Back, Style
from modules.Games.baseGame import baseGame
from ..image_handler import *
from PIL import Image

class RZ(baseGame):
    def __init__(self, Zafiro):
        super().__init__()
        self.display.display("./roms/Rubi/Pokemon-Rubi.gba")
        time.sleep(1)
        self.display.focus()
        self.controller.fast_forward_on()
        self.display.move(560,240)
        time.sleep(1)


        if Zafiro: self.name = "Pokemon Zafiro"
        else: self.name = "Pokemon Rubi"

        self.isZafiro = Zafiro
        self.started = True
        self.in_battle = False

    if os.path.exists("./roms/Rubi/Images/reference.png"):
        os.remove("./roms/Rubi/Images/reference.png")
    if os.path.exists("./roms/Rubi/Pokemon-Rubi-0.png"):
        os.remove("./roms/Rubi/Pokemon-Rubi-0.png")


    def start_game(self):
        
        self.display.focus()
        


        self.controller.press_start()
        time.sleep(0.5)
        self.controller.press_start()
        time.sleep(0.5)
        self.controller.press_start()
        time.sleep(0.5)
        self.controller.press_a()
        time.sleep(0.5)

    def reset_game(self):
        self.resets += 1
        self.display.focus()
        self.controller.press_reset()

    def select_starter(self, starter):
        self.display.focus()
        self.controller.press_a()
        time.sleep(0.5)
        if starter == 1:
            self.controller.press_left()
        elif starter == 3:
            self.controller.press_right()
        
        time.sleep(0.5)
        self.controller.press_a()
        time.sleep(0.5)
        self.controller.press_a()
        time.sleep(0.5)
        self.controller.press_a()
        time.sleep(0.5)

    def menu_mode(self):
        print(Fore.RED + pyfiglet.figlet_format("Rubi/", font="slant") + Fore.BLUE + pyfiglet.figlet_format("/Zafiro", font="slant") + Fore.RESET)
        print("1. Starter Hunting")
        print("2. Spin Mode")
        print("3. Legendary Hunting")
        print("Seleccione un modo:")
        option = int(input())

        if option == 1:
            self.starter_menu()
        elif option == 2:
            self.spin_mode()
        elif option == 3:
            self.legendary_menu()


    def starter_menu(self):
        print("1. Treecko")
        print("2. Torchic")
        print("3. Mudkip")
        print("Seleccione un starter:")
        option = int(input())
        self.starter_hunt(option)

    def starter_hunt(self, option):
        self.start_game()
        self.select_starter(option)
        self.get_referenceImage()
        x = None
        y = None
        if option == 1:
            x = 69
            y = 80
        elif option == 2:
            x = 66
            y = 88
        else:
            x = 72
            y = 91
        
        self.referenceColorPixelStarter = self.get_colorPixel_reference("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", x,y)
        self.reset_game()
        while True:
            print(f"Resets: {self.resets}")
            self.start_game()
            self.select_starter(option)

            #self.controller.fast_forward_off()

            self.controller.make_screenshot()
            
            #self.controller.fast_forward_on()
            color = self.get_colorPixel_reference("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png", x,y)
            
            
            print(f"Color: {color}")

            if color != self.referenceColorPixelStarter:
                print("Shiny Found!")
                self.controller.pause()
                self.controller.fast_forward_off()
                input("Press Enter to continue...")
                break

            delete_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png")
            self.reset_game()
            time.sleep(0.5)

    def battle_started(self):
        self.controller.make_screenshot()
        if self.isZafiro:
            color = self.get_colorPixel_reference("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Zafiro-0.png", 0,159)
            delete_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Zafiro-0.png")
            if color == (74,66,82):
                return True
            return False
        else:
            color = self.get_colorPixel_reference("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png", 0,159)
            delete_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png")
            if color == (74,66,82):
                return True
            return False

    def search_encounter(self) -> bool:
        self.controller.fast_forward_off()
        for i in range(10):
            self.controller.spin_mode()
        self.controller.fast_forward_on()
        time.sleep(2)
        if self.battle_started():
            self.in_battle = True
            return True
        return False
    def spin_mode(self):
        self.start_game()
        while True:
            while not self.in_battle:
                self.search_encounter()

            print("Battle Started! Number: ", self.resets+1)
            self.reset_game()
            self.in_battle = False
            self.start_game()
    
    def legendary_menu(self):
        self.clean_terminal()
        print("1. Static Encounter")
        print("2. Groudon / Kyogre")
        print("Seleccione un modo:")
        option = int(input())

        self.static_encounter(option)

    def static_encounter(self, option):
        self.start_game()
        if option == 2:
            self.Groudon_Kyogre()
        time.sleep(0.5)
        self.get_referenceImage()
        self.crop_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", 110, 5, 220, 74)
        self.reset_game()

        while True:
            print(f"Resets: {self.resets}")
            self.start_game()
            
            if (option == 2):
                self.Groudon_Kyogre()
            time.sleep(0.5)
            self.controller.make_screenshot()
            self.crop_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png", 110, 5, 220, 74)
            a = compare_images("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png")
            if a != 0:
                print("Shiny Found!")
                self.controller.pause()
                self.controller.fast_forward_off()
                input("Press Enter to continue...")
                break
            print("NOT SHINY: ", a)
            delete_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png")
            self.reset_game()
    
    def Groudon_Kyogre(self):
        self.controller.press_left()
        time.sleep(1)
        self.controller.press_a()
        time.sleep(1)
        self.controller.press_a()
        time.sleep(1)
    def get_referenceImage(self):
        #self.controller.pause()
        #self.controller.fast_forward_off()
        #self.controller.avanza_frames(100)
        self.controller.make_screenshot()
        #self.controller.resume()
        #self.controller.fast_forward_on()
    
        if self.isZafiro:
            change_image_name("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Zafiro/Pokemon-Zafiro-0.png", "reference")
            move_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Huntroms/Zafiro/Images")
        else:
            change_image_name("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Pokemon-Rubi-0.png", "reference")
            move_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images")
        
        #self.crop_image("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png",60,80,80,90)
        #self.remove_background("/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png")


    def crop_image(self,image_path, output_path, left, top, right, bottom):
            image = Image.open(image_path)
            #print(image.size)
            cropped_image = image.crop((left, top, right, bottom))
            cropped_image.save(output_path)

    def remove_background(self, image_path, output_path):
        image = Image.open(image_path)
        image = image.convert("RGBA")

        # Create a mask of pixels that are close to white
        white_threshold = 200
        mask = image.convert("L").point(lambda x: 255 if x > white_threshold else 0, mode="1")

        # Apply the mask to the image
        image.putalpha(mask)

        # Save the image with transparent background
        image.save(output_path)
    
    #crop_image(None,"/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png", "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/referecropnce.png", 60,80,80,90)
    #remove_background(None, "/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/reference.png","/home/luca-acosta-iglesias/Documents/Shiny_Hunt/roms/Rubi/Images/2.png")