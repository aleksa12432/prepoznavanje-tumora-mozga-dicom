import os
import pydicom
from tkinter import END
import matplotlib.pyplot as plt

class DicomHandler():

    def napraviSlike(listboxPacijent):
        print("Правим директоријум ./slike ако не постоји...")
        if not os.path.exists("slike"):
            os.makedirs("slike")

        print("Проналазим све DICOM фајлове у ./dicom директоријуму...")
        for f in os.listdir("./dicom"):
            fajl = os.path.join('dicom', f)
            print(f'Пронађен фајл: {str(fajl)}')

            dataset = pydicom.dcmread(fajl)
            putanja = f'slike/{str(dataset.PatientName).replace("^", "_")}'

            if not os.path.exists(putanja):
                os.makedirs(putanja)

            print(f'Чувам слику: {putanja}/{f}.png...')
            plt.imsave(f'{putanja}/{f}.png', dataset.pixel_array, cmap=plt.cm.gray)

        listboxPacijent.delete(0, END)
        for pacijent in os.listdir("./slike"):
            listboxPacijent.insert(END, pacijent)
