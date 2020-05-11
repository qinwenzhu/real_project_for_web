# -*- coding: utf-8 -*-
# @time: 2020/4/25 15:03 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: main.py
# @software: PyCharm

import pytest

if __name__ == '__main__':
    # pytest.main()
    pytest.main(["-s", "-v", "-m test", "--html=outputs/reports/report.html"])
