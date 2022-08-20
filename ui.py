import tkinter as tk
from detekcija import Detekcija
from dicomhandler import DicomHandler
import os
from tkinter import messagebox

class UIClass:

    def __init__(self):
        self.napraviUI()
        self.napraviBindove()
        self.__window.mainloop()

    def napraviUI(self):
        self.__window = tk.Tk()
        self.__window.geometry('800x600')
        self.__window.resizable(False, False)
        self.__window.columnconfigure(0, weight=1)
        self.__window.columnconfigure(1, weight=2)
        self.__window.columnconfigure(2, weight=1)
        self.__window.title(
            'Препознавање тумора мозга на DICOM формату - Алекса Лазаревић ')

        self.__pacijenti = ()
        if os.path.exists("./slike"):
            self.__pacijenti = os.listdir("./slike")

        self.__kolona1 = tk.Frame(self.__window)
        self.__kolona1.grid(column=0, row=0)

        self.__labelPacijent = tk.Label(self.__kolona1, text="Изабери пацијента: ")
        self.__labelPacijent.grid(column=0, row=1)
        self.__labelPacijent.configure(anchor='n')

        self.__listboxPacijent = tk.Listbox(self.__kolona1, listvariable=tk.StringVar(
            value=self.__pacijenti), width=30, height=6, selectmode='single')
        self.__listboxPacijent.grid(
            column=0, row=2)

        self.__labelSlike = tk.Label(self.__kolona1, text="Изабери слику: ")
        self.__labelSlike.grid(column=0, row=3)
        self.__labelSlike.configure(anchor='n')

        self.__listboxSlike = tk.Listbox(
            self.__kolona1, width=30, height=6, selectmode='single', exportselection=False)
        self.__listboxSlike.grid(
            column=0, row=4)

        self.__canvasSlike = tk.Canvas(self.__window, width=300, height=400)
        self.__canvasSlike.grid(column=1, row=0)

        self.__kolona3 = tk.Frame(self.__window)
        self.__kolona3.grid(column=3, row=0)

        self.__dugmeNapraviSlike = tk.Button(self.__kolona1, text="Направи слике",
                                      command=self.napraviSlikeHandler)
        self.__dugmeNapraviSlike.grid(column=0, row=0)

        self.__labelDonjiThreshold = tk.Label(self.__kolona3, text="Доњи праг: ")
        self.__labelDonjiThreshold.grid(column=0, row=0)
        self.__labelDonjiThreshold.configure(anchor='n')

        self.__donjiThresholdRange = tk.Scale(self.__kolona3, from_=0, to=255, orient='horizontal')
        self.__donjiThresholdRange.set(80)
        self.__donjiThresholdRange.grid(column=0, row=1)

        self.__labelGornjiThreshold = tk.Label(self.__kolona3, text="Горњи праг: ")
        self.__labelGornjiThreshold.grid(column=0, row=2)
        self.__labelGornjiThreshold.configure(anchor='n')

        self.__gornjiThresholdRange = tk.Scale(self.__kolona3, from_=0, to=255, orient='horizontal')
        self.__gornjiThresholdRange.set(87)
        self.__gornjiThresholdRange.grid(column=0, row=3)

        self.__labelminimalnaPovrsina = tk.Label(self.__kolona3, text="Минимална површина тумора: ")
        self.__labelminimalnaPovrsina.grid(column=0, row=4)
        self.__labelminimalnaPovrsina.configure(anchor='n')

        self.__minimalnaPovrsinaTumora = tk.Scale(self.__kolona3, from_=0, to=200, orient='horizontal')
        self.__minimalnaPovrsinaTumora.set(100)
        self.__minimalnaPovrsinaTumora.grid(column=0, row=5)

        self.__labelmaksimalnaPovrsina = tk.Label(self.__kolona3, text="Максимална површина тумора: ")
        self.__labelmaksimalnaPovrsina.grid(column=0, row=6)
        self.__labelmaksimalnaPovrsina.configure(anchor='n')

        self.__maksimalnaPovrsinaTumora = tk.Scale(self.__kolona3, from_=200, to=5000, orient='horizontal')
        self.__maksimalnaPovrsinaTumora.set(2300)
        self.__maksimalnaPovrsinaTumora.grid(column=0, row=7)

        self.__dugmeIzvrsiSlike = tk.Button(self.__kolona3, text="Изврши препознавање тумора",
                                 command=self.izvrsiPrepoznavanjeHandler)
        self.__dugmeIzvrsiSlike.grid(column=0, row=8)

    def napraviBindove(self):
        self.__listboxPacijent.bind('<ButtonRelease>', self.proveraSlika)
        self.__listboxSlike.bind('<ButtonRelease>', self.proveraSlika)
        self.__listboxPacijent.bind('<<ListboxSelect>>', self.pacijentSelected)
        self.__listboxSlike.bind('<<ListboxSelect>>', self.slikaSelected)

    def napraviSlikeHandler(self):
        DicomHandler.napraviSlike(self.__listboxPacijent)

    def izvrsiPrepoznavanjeHandler(self):
        if not (self.__listboxSlike.curselection() and self.__listboxPacijent.curselection()):
            messagebox.showerror("Грешка!", "Нисте изабрали сва поља!")
            return
        selectedSlika = self.__listboxSlike.get(self.__listboxSlike.curselection())
        selectedPacijent = self.__listboxPacijent.get(self.__listboxPacijent.curselection())
        fullPutanja = f"./slike/{selectedPacijent}/{selectedSlika}"
        detekcija = Detekcija(fullPutanja)

        detekcija.detektujTumor(self.__donjiThresholdRange.get(),
                                self.__gornjiThresholdRange.get(), 
                                self.__minimalnaPovrsinaTumora.get(), 
                                self.__maksimalnaPovrsinaTumora.get())

        detekcija.prikaziRezultate()

    def pacijentSelected(self, event):
        selected = self.__listboxPacijent.get(self.__listboxPacijent.curselection())
        print(f"Изабран пацијент: {selected}")
        slike = os.listdir(f"./slike/{selected}")
        self.__listboxSlike.delete(0, tk.END)
        for slika in slike:
            self.__listboxSlike.insert(tk.END, slika)

    def slikaSelected(self, event):
        selectedSlika = self.__listboxSlike.get(self.__listboxSlike.curselection())
        selectedPacijent = self.__listboxPacijent.get(self.__listboxPacijent.curselection())
        fullPutanja = f"./slike/{selectedPacijent}/{selectedSlika}"
        print(
            f"Изабрана слика: {fullPutanja}")

        img = tk.PhotoImage(file=fullPutanja)
        self.__window.img = img
        self.__canvasSlike.delete("all")
        self.__canvasSlike.create_image(img.width() / 2, img.height() / 2, anchor="center", image=img)

    def proveraSlika(self, event):
        if os.path.exists('./slike') and len(os.listdir("./slike")) > 0:
            return
        messagebox.showerror("Грешка!", "Слике нису учитане!")
