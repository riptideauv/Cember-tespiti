import cv2
import numpy as np

#Örnek bir koddur. Kenar tespiti algoritması kullanılmamıştır. Bu algoritmada sadece renk maskelemesi üzerinden bir tespit uygulanmıştır.

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

#cv2.namedWindow("Kirmizi Daire")
while(True):
    success, img1 = cap.read()
    img1 = cv2.flip(img1, 1)
    img2 = img1.copy()
    #img1 = cv2.imread("coins.jpg")

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    kirmizi_min = np.array([0, 157, 184], np.uint8)
    kirmizi_max = np.array([180, 255, 255], np.uint8)

    maske = cv2.inRange(hsv, kirmizi_min, kirmizi_max)

    img1_blur = cv2.medianBlur(maske, 5)#pozitif ve tek olmalı 2. parametre

    circles = cv2.HoughCircles(img1_blur, cv2.HOUGH_GRADIENT, 1, img1.shape[0]/0.1, param1=200, param2=10, minRadius=5, maxRadius=30)
    #(kaynak resim, yöntem, çözünürlük ölçeği,çemberler arası mesafe img1.shape[0]/64 ile oynayıp değiştirebilirsin...)

    cv2.rectangle(img2, (320 - 30, 240 - 30), (320 + 30, 240 + 30), (0, 0, 0),thickness=2)  # Kordinat Sistemi Merkezi Hedef Alanı
    cv2.line(img2, (320, 240 - 30), (320, 0), (0, 0, 0), thickness=2)  # Kordinat Sistemim Çizgileri
    cv2.line(img2, (320, 240 + 30), (320, 480), (0, 0, 0), thickness=2)
    cv2.line(img2, (320 - 30, 240), (0, 240), (0, 0, 0), thickness=2)
    cv2.line(img2, (320 + 30, 240), (640, 240), (0, 0, 0), thickness=2)

    if circles is not None:
        circles = np.uint16(np.around(circles))#around ile değerleri yuvarladık
        for i in circles[0,:]: #circles içerisinde 50 tane değer varsa mesela i ye 0 ıncıdan 50. ye kadar olan değerleri sırayla atar. i o değerleri alır.
            #buradaki 0. ve  1. değerler {(a,b), koordinat sistemindeki merkez noktasının konumu} merkez noktasının koordinatı. 2. değer ise yarıçaptır.(r)
            cv2.circle(img2,(i[0], i[1]), i[2],(0,255,0),2)

            if i[0] > 290 and i[0] < 350 and i[1] > 210 and i[1] < 270:

                cv2.putText(img2, "KILITLENDI!:", (i[0], i[1] + i[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)
                cv2.putText(img2, "X:" + str(i[0]) + "  Y:" + str(i[1]), (i[0], i[1] + i[2] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

                cv2.rectangle(img2, (320 - 30, 240 - 30), (320 + 30, 240 + 30), (0, 0, 255),thickness=2)  # Kordinat Sistemi Merkezi Hedef Alanı
                cv2.line(img2, (320, 240 - 30), (320, 0), (0, 0, 255), thickness=2)  # Kordinat Sistemim Çizgileri
                cv2.line(img2, (320, 240 + 30), (320, 480), (0, 0, 255), thickness=2)
                cv2.line(img2, (320 - 30, 240), (0, 240), (0, 0, 255), thickness=2)
                cv2.line(img2, (320 + 30, 240), (640, 240), (0, 0, 255), thickness=2)
            else:

                cv2.putText(img2, "KORDINAT:", (i[0], i[1]+i[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(img2, "X:" + str(i[0]) + "  Y:" + str(i[1]), (i[0], i[1]+i[2]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    #cv2.namedWindow("Kirmizi Daire", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("Kirmizi Daire", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)



    cv2.imshow("Kirmizi Daire Maske", maske)
    cv2.imshow("Kirmizi Daire", img2)
    #cv2.resizeWindow("Cirmizu Dayire", 1366, 768)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break