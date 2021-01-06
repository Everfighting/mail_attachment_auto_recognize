#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/1 4:21 下午
# @File    : extract_content.py
import os
import glob
import xlwt
from cnstd import CnStd
from cnocr import CnOcr
from loguru import logger


# 调用接口处理图片
def extract_content(save_dir_path):
    std = CnStd()
    cn_ocr = CnOcr()

    base_path = os.path.abspath(os.path.dirname(__file__))
    pic_base_dir = os.path.join(base_path, "received")
    pic_path_list = (glob.glob(os.path.join(pic_base_dir, "*.png")) +
                     glob.glob(os.path.join(pic_base_dir, "*.jpg")) +
                     glob.glob(os.path.join(pic_base_dir, "*.jpeg"))
                     )

    workbook = xlwt.Workbook()
    for index, pic_path in enumerate(pic_path_list):
        sheet = workbook.add_sheet('sheet{}'.format(index), cell_overwrite_ok=True)
        box_info_list = std.detect(pic_path)
        for box_info in box_info_list:
            x_list, y_list = [], []
            for (x, y) in box_info['box']:
                x_list.append(x)
                y_list.append(y)
            top, bottom, left, right = min(y_list), max(y_list), min(x_list), max(x_list)
            top_row, bottom_row, left_column, right_column = int(top // 80), int(bottom // 80), int(left // 60), int(
                right // 60)
            cropped_img = box_info['cropped_img']  # 检测出的文本框
            ocr_res = ''.join(cn_ocr.ocr_for_single_line(cropped_img))
            try:
                logger.info(
                    "top_row:{}, bottom_row:{}, left_column:{}, right_column:{}, ocr_res:{}",
                    top_row, bottom_row, left_column, right_column, ocr_res, feature="f-strings")
                sheet.write_merge(top_row, bottom_row, left_column, right_column, ocr_res)
            except Exception as e:
                print(e)

    xls_base_dir = os.path.join(base_path, save_dir_path)
    xls_path = os.path.join(xls_base_dir, "res.xls")
    workbook.save(xls_path)


if __name__ == '__main__':
    extract_content("./to_send")