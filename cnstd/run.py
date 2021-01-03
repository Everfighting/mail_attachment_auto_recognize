#-*- codeing = utf-8 -*-
#@Time : 2020/12/30 下午10:19
#@Author : 江啸栋19262010049
#@File : run.py
#@Software : PyCharm


# from cnstd import CnStd
# std = CnStd()
# box_info_list = std.detect('examples/taobao.jpg')

from cnstd import CnStd
from cnocr import CnOcr

std = CnStd()
cn_ocr = CnOcr()

box_info_list = std.detect('examples/taobao.jpg')

for box_info in box_info_list:
    cropped_img = box_info['cropped_img']
    ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
    print('ocr result: %s' % ''.join(ocr_res))