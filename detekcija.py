import matplotlib.pyplot as plt
import cv2

class Detekcija:

    def __init__(self, putanjaDoSlike):
        print(f"Изабран фајл: {putanjaDoSlike}, читам...")
        self.__origImg = cv2.imread(putanjaDoSlike, 0)

    def detektujTumor(self, donjiThreshold, gornjiThreshold, minPovrsina, maxPovrsina):

        self.__blurredImg = self.__origImg.copy()

        print(f"Копирам слику и претварам у RGB за контуру касније...")
        self.__output = cv2.cvtColor(self.__blurredImg.copy(), cv2.COLOR_GRAY2RGB)

        print(f"Замућујем слику...")
        self.__blurredImg = cv2.medianBlur(self.__blurredImg, 5)

        print(f"Извршавам бинарни праг на слику...")
        ret, self.__thresholdedImg = cv2.threshold(self.__blurredImg, donjiThreshold,
                                gornjiThreshold, cv2.THRESH_BINARY)

        print(f"Проналазим највећу контуру на слици...")
        contours, hierarchy = cv2.findContours(
            self.__thresholdedImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        c = max(contours, key=cv2.contourArea)

        if minPovrsina < cv2.contourArea(c) < maxPovrsina:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(self.__output, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    def prikaziRezultate(self):

        print(f"Приказујем слике...")
        titles = ["Оригинална слика", "Замућена слика",
                  "Слика бинарног прага", "Слика контуре"]

        images = [self.__origImg, self.__blurredImg, self.__thresholdedImg, self.__output]

        for i in range(len(images)):
            plt.subplot(2, 2, i + 1)
            plt.imshow(images[i], 'gray')
            plt.title(titles[i])
            plt.xticks([])
            plt.yticks([])

        plt.show()