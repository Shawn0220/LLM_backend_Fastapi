# -*- coding: utf-8 -*-
import re
"""正则匹配：非零，正数和正浮点数"""
str_ = '0'

print(re.match('(^[1-9]+$)|(^\d+.\d*$)', str_))
import requests
requests = requests.session()