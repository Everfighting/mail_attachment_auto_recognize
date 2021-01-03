#-*- codeing = utf-8 -*-
#@Time : 2020/12/30 下午2:13
#@Author : 江啸栋19262010049
#@File : run.py
#@Software : PyCharm

from cnocr import CnOcr
ocr = CnOcr()
res = ocr.ocr('examples/00010991.jpg')
print("Predicted Chars:", res)

