import tkinter as tk
from typing import Text


class App(tk.Tk) :

    def __init__(self):

        super().__init__()

        self.title("Multi-Fenster App")
        self.geometry("300x250")
        #--- Positionierung des Hauptfensters in der Mitte des Bildschirms ---#
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_frame(StartPage)

    def show_frame(self, page):

        frame = self.frames[page]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

       super().__init__(parent)

       label = tk.Label(self, 
                        text="Start Page", 
                        font=('Helvetica', 18, "bold"))
       label.pack(pady=20)

       btn1 = tk.Button(self,
                        text="Gehe zu Fenster 1", 
                        command = lambda: controller.show_frame(PageOne))
       btn1.pack(pady=10, padx=100)


       btn2 = tk.Button(self, 
                        text="Gehe zu Fenster 2", 
                        command = lambda: controller.show_frame(PageTwo))
       btn2.pack(pady=10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        label = tk.Label(self,
                         text="Fenster 1",                               
                         font=('Helvetica',18,"bold"))
        label.pack(pady=20)

        btn_back = tk.Button(self,
                             text= "Zurück zum Menü",
                             command= lambda: controller.show_frame(StartPage))

        btn_back.pack(pady=10)

class PageTwo(tk.Frame) : 

    def __init__(self, parent, controller):

        super().__init__(parent)

        label = tk.Label(self,
                         text="Fenster 2",
                         font=('Helvetica',18,"bold"))
        label.pack(pady=20)
        btn_back = tk.Button(self,
                             text="Zurück zum Menü",
                             command = lambda: controller.show_frame(StartPage))
        btn_back.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
