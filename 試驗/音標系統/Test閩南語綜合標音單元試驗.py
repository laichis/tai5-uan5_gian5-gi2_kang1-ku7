# -*- coding: utf-8 -*-
from unittest.case import TestCase
from 臺灣言語工具.基本物件.字 import 字
from 臺灣言語工具.音標系統.閩南語綜合標音 import 閩南語綜合標音
from 臺灣言語工具.基本物件.公用變數 import 無音
from 臺灣言語工具.解析整理.型態錯誤 import 型態錯誤
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class 閩南語綜合標音單元試驗(TestCase):

    def setUp(self):
        self.我型, self.我音 = '我', 'gua2'

    def test_一般綜合標音(self):
        self.assertEqual(字('我', 'gua2').綜合標音(閩南語綜合標音), [{
            "漢字": "我",
            "臺羅數字調": "gua2",
            "臺羅閏號調": "guá",
            "通用數字調": "ghua4",
            "吳守禮方音": "ㆣㄨㄚˋ"
        }])

    def test_干焦漢字綜合標音(self):
        self.assertEqual(字('我', 無音).綜合標音(閩南語綜合標音), [{
            "漢字": "我",
            "臺羅數字調": "我",
            "臺羅閏號調": "我",
            "通用數字調": "我",
            "吳守禮方音": "我"
        }])

    def test_干焦臺羅綜合標音(self):
        self.assertEqual(字('gua2', 無音).綜合標音(閩南語綜合標音), [{
            "漢字": "gua2",
            "臺羅數字調": "gua2",
            "臺羅閏號調": "guá",
            "通用數字調": "ghua4",
            "吳守禮方音": "ㆣㄨㄚˋ"
        }])

    def test_標點綜合標音(self):
        self.assertEqual(字('，', 無音).綜合標音(閩南語綜合標音), [{
            "漢字": "，",
            "臺羅數字調": "，",
            "臺羅閏號調": "，",
            "通用數字調": "，",
            "吳守禮方音": "，"
        }])

    def test_對齊標點綜合標音(self):
        self.assertEqual(字('，', ',').綜合標音(閩南語綜合標音), [{
            "漢字": "，",
            "臺羅數字調": ",",
            "臺羅閏號調": ",",
            "通用數字調": ",",
            "吳守禮方音": ","
        }])

    def test_無合法音綜合標音(self):
        self.assertEqual(字('我', 'uo3').綜合標音(閩南語綜合標音), [{
            "漢字": "我",
            "臺羅數字調": "uo3",
            "臺羅閏號調": "uo3",
            "通用數字調": "uo3",
            "吳守禮方音": "uo3"
        }])

    def test_有分詞(self):
        綜合標音 = 拆文分析器.對齊句物件('我', 'uo3').綜合標音(閩南語綜合標音)
        self.assertIn('分詞', 綜合標音[0])

    def test_烏白傳(self):
        self.assertRaises(型態錯誤, 閩南語綜合標音, '我')
        self.assertRaises(型態錯誤, 閩南語綜合標音, '我', False)
        self.assertRaises(型態錯誤, 閩南語綜合標音, '我', True)
