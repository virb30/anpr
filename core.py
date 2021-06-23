import numpy as np
import cv2
import imutils


main_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 13))


class Extractor:
    erode_iter = 2
    dilate_iter = 1

    def __init__(self, image):
        self.original_image = image
        self.converted_image = np.array(image)

    def __call__(self, erode_iter=2, dilate_iter=1):
        self.erode_iter = erode_iter
        self.dilate_iter = dilate_iter
        image = self.to_grayscale()
        area = self.get_plate_area()
        contours = cv2.findContours(area.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = w / h
            # dimensões da placa: 40x13cm
            if ratio >= 2.5 and ratio <= 4:
                identified_plate_area = image[y: y + h, x: x + w]
                cropped_plate = cv2.threshold(identified_plate_area, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
                return cropped_plate

    def to_grayscale(self):
        gray_image = cv2.cvtColor(self.converted_image, cv2.COLOR_RGB2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 13, 15, 15)
        return gray_image

    def get_plate_area(self):
        black_hat_image = self._black_hat_morph()
        # light_image = self.close(gray_image)
        gradient_image = self._magnitude_gradient(black_hat_image)
        smoothed_image = self._smooth(gradient_image)
        area_image = self._fine_tunning(smoothed_image)
        return area_image

    def _black_hat_morph(self):
        gray = self.to_grayscale()
        black_hat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, main_kernel)
        return black_hat

    def _close(self, image):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        light = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        light = cv2.threshold(light, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
        return light

    def _magnitude_gradient(self, image):
        gradient_x = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradient_x = np.absolute(gradient_x)

        # extrair valores mínimo e máximo
        minimo, maximo = np.min(gradient_x), np.max(gradient_x)

        # normalizar  = (valor-min) / (max-min)
        gradient_x = 255 * (gradient_x - minimo) / (maximo - minimo)

        # converter para UINT8
        gradient_x = gradient_x.astype("uint8")

        return gradient_x

    def _smooth(self, image):
        gradient_x = cv2.GaussianBlur(image, (5, 5), 0)
        gradient_x = cv2.morphologyEx(gradient_x, cv2.MORPH_CLOSE, main_kernel)
        thresh = cv2.threshold(gradient_x, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[-1]
        return thresh

    def _fine_tunning(self, image):
        thresh = cv2.erode(image, None, iterations=self.erode_iter)
        thresh = cv2.dilate(thresh, None, iterations=self.dilate_iter)
        return thresh

