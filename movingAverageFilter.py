"""""
A Denoising filter thar reduce noise but inreaz fuzzyness
"""""
# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
#
# img = cv2.imread('WIN_20190627_12_40_00_Pro.jpg')
#
# dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,5,21)
# # cv2.imwrite('filtered1.jpg', dst)
#
# plt.subplot(121),plt.imshow(img)
# plt.subplot(122),plt.imshow(dst)
# plt.show()

# input: an image
import numpy as np
import cv2
from matplotlib import pyplot as plt

def moving_average_filter(img):
    avg1 = np.float32(img)
    # alpha regulates the update speed (how fast the accumulator “forgets” about earlier images)
    cv2.accumulateWeighted(img, avg1, 0.1)
    res = cv2.convertScaleAbs(avg1)

    return res

