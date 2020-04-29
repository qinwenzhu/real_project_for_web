

class ToolData:

    """ 参数化数据- 上传不同人脸属性的图片 - 期望输出对应的人脸属性内容 """
    face_data_negative = [
        { "img_path": "woman_no_mustache_no_glasse_no_mask.jpg", "sex": "女", "age": "成人", "phiz": "悲伤",
            "mustache": "无", "glasse": "无", "mask": "无", "helmet": "无", "hat": "无"},
        {"img_path": "have_glasse.jpg", "sex": "男", "age": "成人", "phiz": "平静",
            "mustache": "无", "glasse": "透明眼镜", "mask": "无", "helmet": "无", "hat": "无"},
        {"img_path": "have_hat_and_have_glasse.jpg", "sex": "女", "age": "儿童", "phiz": "平静",
                "mustache": "无", "glasse": "太阳眼镜", "mask": "无", "helmet": "无", "hat": "有"},
        {"img_path": "man_have_mustache.jpg", "sex": "男", "age": "成人", "phiz": "平静",
            "mustache": "有", "glasse": "无", "mask": "无", "helmet": "无", "hat": "无"},
        {"img_path": "have_helmet.jpg", "sex": "女", "age": "成人", "phiz": "平静",
            "mustache": "无", "glasse": "无", "mask": "无", "helmet": "有", "hat": "有"},
        {"img_path": "have_mask.jpg", "sex": "女", "age": "成人", "phiz": "平静",
            "mustache": "无", "glasse": "无", "mask": "有", "helmet": "无", "hat": "无"}
    ]

    """ 参数化数据- 上传不同尺寸大小的人脸图片 - 检测支持系统是否支持上限小于等于16M大小的图片 """
    score_detection_data_negative = [
        {"img_path": "size_normal.jpg"},
        {"img_path": "size_17K.jpg"},
        {"img_path": "size_140K.jpg"},
        {"img_path": "size_5M.jpg"},
        {"img_path": "size_10M.jpg"}
    ]
