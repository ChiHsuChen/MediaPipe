import cv2
import numpy as np

#image呼叫端使用cv2.imread的回傳值再帶入此function call
def gamma_correction(image, gamma):
    if image is None:
        raise ValueError("The provided image is invalid.")
    # Apply gamma correction
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
    gamma_corrected = cv2.LUT(image, table)
    return gamma_corrected

def open_image(image, kernel_size=(5, 5)):
    kernel = np.ones(kernel_size, np.uint8)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opened_image

def close_image(image, kernel_size=(5, 5)):
    kernel = np.ones(kernel_size, np.uint8)
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closed_image