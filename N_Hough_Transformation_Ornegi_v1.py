import cv2
import numpy as np

#Örnek bir koddur. Kenar tespiti algoritması kullanılmamıştır. Bu algoritmada sadece renk maskelemesi üzerinden bir tespit uygulanmıştır.

frameWidth = 500
frameHeight = 350
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

#cv2.namedWindow("Kirmizi Daire")
while(True):
    success, img1 = cap.read()
    img1 = cv2.flip(img1, 1)
    img2 = img1.copy()

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

    sari_min = np.array([20, 100, 100])
    sari_max = np.array([158, 255, 255])

    maske = cv2.inRange(hsv, sari_min, sari_max)

    img1_blur = cv2.medianBlur(maske, 5)#pozitif ve tek olmalı 2. parametre

    circles = cv2.HoughCircles(img1_blur, cv2.HOUGH_GRADIENT, 1, img1.shape[0]/0.1, param1=200, param2=10, minRadius=5, maxRadius=30)
    #(kaynak resim, yöntem, çözünürlük ölçeği,çemberler arası mesafe img1.shape[0]/64 ile oynayıp değiştirebilirsin...)

    cv2.circle(img2,(320,200),30,(0,0,0),thickness=2)  # Kordinat Sistemi Merkezi Hedef Alanı
    cv2.line(img2, (320, 240 - 70), (320, 0), (0, 0, 0), thickness=2)  # Kordinat Sistemim Çizgileri
    cv2.line(img2, (320, 240 - 10), (320, 480), (0, 0, 0), thickness=2)
    cv2.line(img2, (240 + 50, 200), (0, 200), (0, 0, 0), thickness=2)
    cv2.line(img2, (320 + 30, 200), (640, 200), (0, 0, 0), thickness=2)

    if circles is not None:
        circles = np.uint16(np.around(circles))#around ile değerleri yuvarladık
        for i in circles[0,:]: #circles içerisinde 50 tane değer varsa mesela i ye 0 ıncıdan 50. ye kadar olan değerleri sırayla atar. i o değerleri alır.
            #buradaki 0. ve  1. değerler {(a,b), koordinat sistemindeki merkez noktasının konumu} merkez noktasının koordinatı. 2. değer ise yarıçaptır.(r)
            cv2.circle(img2,(i[0], i[1]), i[2],(0,255,0),2)

            if i[0] > 300 and i[0] < 340 and i[1] > 180 and i[1] < 240:

                cv2.putText(img2, "KILITLENDI!:", (i[0], i[1] + i[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0,0), 1)
                cv2.putText(img2, "X:" + str(i[0]) + "  Y:" + str(i[1]), (i[0], i[1] + i[2] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

                cv2.circle(img2,(320,200),30,(0,0,0),thickness=2)  # Kordinat Sistemi Merkezi Hedef Alanı
                cv2.line(img2, (320, 240 - 70), (320, 0), (0, 0, 0), thickness=2)  # Kordinat Sistemim Çizgileri
                cv2.line(img2, (320, 240 - 10), (320, 480), (0, 0, 0), thickness=2)
                cv2.line(img2, (240 + 50, 200), (0, 200), (0, 0, 0), thickness=2)
                cv2.line(img2, (320 + 30, 200), (640, 200), (0, 0, 0), thickness=2)
            else:

                cv2.putText(img2, "KORDINAT:", (i[0], i[1]+i[2]), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                cv2.putText(img2, "X:" + str(i[0]) + "  Y:" + str(i[1]), (i[0], i[1]+i[2]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

 
    cv2.imshow("Cember Maske", maske)
    cv2.imshow("Sari Cember", img2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
