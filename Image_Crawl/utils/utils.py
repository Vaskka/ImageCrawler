# -*- coding: utf-8 -*-
import base64


# 从图片路径得到编码图片
def _from_path_to_base64(path):
    with open(path, "rb") as f:
        raw_text = f.read()

    return base64.b64encode(raw_text)