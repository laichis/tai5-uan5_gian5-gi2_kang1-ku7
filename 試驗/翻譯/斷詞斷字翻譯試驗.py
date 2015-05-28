# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國103年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from unittest.case import TestCase
from unittest.mock import patch, call


from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.基本元素.章 import 章
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.基本元素.句 import 句
from 臺灣言語工具.基本元素.組 import 組
from 臺灣言語工具.基本元素.集 import 集
from 臺灣言語工具.翻譯.斷詞斷字翻譯 import 斷詞斷字翻譯

class 斷詞斷字翻譯試驗(TestCase):
	def setUp(self):
		self.分析器 = 拆文分析器()
		self.譀鏡 = 物件譀鏡()
		
		self.xmlrpcPatcher = patch('xmlrpc.client.ServerProxy')
		self.xmlrpcMock = self.xmlrpcPatcher.start()
		
		斷詞用戶端 = 摩西用戶端()
		斷字用戶端 = 摩西用戶端()
		self.翻譯工具 = 斷詞斷字翻譯(
				斷詞用戶端=斷詞用戶端,
				斷字用戶端=斷字用戶端,
				)
		華語組物件 = 組()
		華語組物件.內底詞 = [
				self.分析器.建立詞物件('我們'),
				self.分析器.建立詞物件('要'),
				self.分析器.建立詞物件('去'),
				self.分析器.建立詞物件('吃飯'),
				self.分析器.建立詞物件('。'),
			]
		華語集物件 = 集()
		華語集物件.內底組 = [華語組物件]
		self.華語句物件 = 句()
		self.華語句物件.內底集 = [華語集物件]
		
		閩南語組陣列 = [
			self.分析器.轉做組物件('阮｜gun2'),
			self.分析器.轉做組物件('欲｜beh4'),
			self.分析器.轉做組物件('去｜khi3'),
			self.分析器.轉做組物件('食-飯｜tsiah8-png7'),
			self.分析器.轉做組物件('。｜.'),
			]
		self.閩南語句物件 = self._組陣列分開包做句物件(閩南語組陣列)
		
		self.華語句物件二 = self.分析器.建立句物件('好喲！')
		self.華語章物件 = 章([self.華語句物件, self.華語句物件二])
		
		翻譯對應關係 = [
				{'tgt-start': 0, 'src-start': 0, 'src-end': 0},
				{'tgt-start': 1, 'src-start': 1, 'src-end': 1},
				{'tgt-start': 2, 'src-start': 2, 'src-end': 2},
				{'tgt-start': 3, 'src-start': 3, 'src-end': 3},
				{'tgt-start': 4, 'src-start': 4, 'src-end': 4},
			]
		
		self.斷詞全翻譯結果 = {'nbest':[{
			'text':'阮｜gun2  欲｜beh4  去｜khi3  食-飯｜tsiah8-png7  。｜.  ',
			'align':翻譯對應關係,
			'totalScore':-21.66,
			}]}
		self.斷詞孤字未知詞譯孤字 = {'nbest':[{
			'text':'阮｜gun2  要|UNK|UNK|UNK  去｜khi3  食-飯｜tsiah8-png7  。｜.  ',
			'align':翻譯對應關係,
			'totalScore':-21.66,
			}]}
		self.斷字孤字未知詞譯孤字 = {'nbest':[{
			'text':'欲｜beh4  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 0}],
			'totalScore':-3.33,
			}]}
		self.斷字孤字未知詞譯袂出來 = {'nbest':[{
			'text':'要|UNK|UNK|UNK  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 0}],
			'totalScore':-3.33,
			}]}
		self.斷詞雙字未知詞譯孤字 = {'nbest':[{
			'text':'我們|UNK|UNK|UNK  欲｜beh4  去｜khi3  食-飯｜tsiah8-png7  。｜.  ',
			'align':翻譯對應關係,
			'totalScore':-21.66,
			}]}
		self.斷字雙字未知詞譯孤字 = {'nbest':[{
			'text':'阮｜gun2  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 1}],
			'totalScore':-3.33,
			}]}
		self.斷詞雙字未知詞譯雙字 = {'nbest':[{
			'text':'阮｜gun2  欲｜beh4  去｜khi3  吃飯|UNK|UNK|UNK  。｜.  ',
			'align':翻譯對應關係,
			'totalScore':-21.66,
			}]}
		
		self.斷字雙字未知詞譯雙詞 = {'nbest':[{
			'text':'食｜tsiah8  飯｜png7  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 1}],
			'totalScore':-3.33,
			}]}
		
		self.斷詞雙未知詞 = {'nbest':[{
			'text':'阮｜gun2  欲｜beh4  去|UNK|UNK|UNK  吃飯|UNK|UNK|UNK  。｜.  ',
			'align':翻譯對應關係,
			'totalScore':-21.66,
			}]}
		self.斷字雙未知詞譯一詞 = {'nbest':[{
			'text':'去｜khi3  食｜tsiah8  飯｜png7  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 2}],
			'totalScore':-3.33,
			}]}
		self.斷字雙未知詞譯兩詞 = {'nbest':[{
			'text':'去｜khi3  食｜tsiah8  飯｜png7  ',
			'align':[{'tgt-start': 0, 'src-start': 0, 'src-end': 0},
					{'tgt-start': 1, 'src-start': 1, 'src-end': 2}],
			'totalScore':-3.33,
			}]}
	def tearDown(self):
		self.xmlrpcPatcher.stop()
	def test_干焦用著斷詞用戶端的翻譯(self):
		self.xmlrpcMock.return_value.translate.return_value = self.斷詞全翻譯結果
		翻譯工具 = 斷詞斷字翻譯(
				斷詞用戶端=摩西用戶端(),
				斷字用戶端=None,
				)
		翻譯工具.翻譯(self.華語句物件)
		self.xmlrpcMock.return_value.translate.assert_has_calls([
				call({
						"text":'我-們 要 去 吃-飯 。',
						"align":"true",
						"report-all-factors":"true",
						'nbest':1,
					})
			])
	def test_翻譯結果是句物件(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertIsInstance(結果句物件, 句)
	def test_翻譯結果結構(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(結果句物件, self.閩南語句物件)
	def test_來源新結構檢查(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		_, 華語新結構句物件, _ = self.翻譯工具.翻譯(self.華語句物件)
		華語組陣列 = [
			self.分析器.轉做組物件('我們'),
			self.分析器.轉做組物件('要'),
			self.分析器.轉做組物件('去'),
			self.分析器.轉做組物件('吃飯'),
			self.分析器.轉做組物件('。'),
			]
		華語句物件 = self._組陣列分開包做句物件(華語組陣列)
		self.assertEqual(華語新結構句物件, 華語句物件)
	def test_翻譯結果佮來源長度相仝(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		結果句物件, 華語新結構句物件, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(len(結果句物件.內底集[0].內底組),
			len(華語新結構句物件.內底集[0].內底組))
	def test_翻譯結果對齊檢查(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		for 組物件 in 結果句物件.內底集[0].內底組:
			self.assertEqual(組物件, 組物件.翻譯來源組物件.翻譯目標組物件)
	def test_來源新結構對齊檢查(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		_, 華語新結構句物件, _ = self.翻譯工具.翻譯(self.華語句物件)
		for 組物件 in 華語新結構句物件.內底集[0].內底組:
			self.assertEqual(組物件, 組物件.翻譯目標組物件.翻譯來源組物件)
	def test_翻譯分數(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯孤字
			]
		_, _, 分數 = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(分數, -21.66 - 3.33)
	def test_斷字未知詞的詞愛記錄(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯袂出來
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(self.譀鏡.看型(結果句物件.內底集[1].內底組[0]), '要')
		self.assertEqual(結果句物件.內底集[1].內底組[0].屬性['未知詞'], '是')
	def test_斷字毋是未知詞的詞袂使記錄(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞孤字未知詞譯孤字, self.斷字孤字未知詞譯袂出來
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(self.譀鏡.看型(結果句物件.內底集[0].內底組[0]), '阮')
		self.assertFalse(hasattr(結果句物件.內底集[0].內底組[0], '屬性'))
		
	def test_斷詞雙字未知詞譯孤字(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙字未知詞譯孤字, self.斷字雙字未知詞譯孤字
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(結果句物件, self.閩南語句物件)
	def test_斷詞雙字未知詞譯雙字(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙字未知詞譯雙字, self.斷字雙字未知詞譯雙詞
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(結果句物件, self.閩南語句物件)
	def test_雙未知詞譯做伙翻譯(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙未知詞, self.斷字雙未知詞譯兩詞
			]
		self.翻譯工具.翻譯(self.華語句物件)		
		self.xmlrpcMock.return_value.translate.assert_has_calls([
				call({
						"text":'去 吃 飯',
						"align":"true",
						"report-all-factors":"true",
						'nbest':1,
					})
			])
	def test_雙未知詞譯兩詞(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙未知詞, self.斷字雙未知詞譯兩詞
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(結果句物件, self.閩南語句物件)
	def test_雙未知詞譯一詞閩南語(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙未知詞, self.斷字雙未知詞譯一詞
			]
		結果句物件, _, _ = self.翻譯工具.翻譯(self.華語句物件)
		閩南語組陣列 = [
			self.分析器.轉做組物件('阮｜gun2'),
			self.分析器.轉做組物件('欲｜beh4'),
			self.分析器.轉做組物件('去-食-飯｜khi3-tsiah8-png7'),
			self.分析器.轉做組物件('。｜.'),
			]
		閩南語句物件 = self._組陣列分開包做句物件(閩南語組陣列)
		self.assertEqual(結果句物件, 閩南語句物件)
	def test_雙未知詞譯一詞華語(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙未知詞, self.斷字雙未知詞譯一詞
			]
		_, 華語新結構句物件, _ = self.翻譯工具.翻譯(self.華語句物件)
		華語組陣列 = [
			self.分析器.轉做組物件('我們'),
			self.分析器.轉做組物件('要'),
			self.分析器.轉做組物件('去吃飯'),
			self.分析器.轉做組物件('。'),
			]
		華語句物件 = self._組陣列分開包做句物件(華語組陣列)
		self.assertEqual(華語新結構句物件, 華語句物件)
	def test_雙未知詞譯一詞華語語句(self):
		self.xmlrpcMock.return_value.translate.side_effect = [
			self.斷詞雙未知詞, self.斷字雙未知詞譯一詞
			]
		_, 華語新結構句物件, _ = self.翻譯工具.翻譯(self.華語句物件)
		self.assertEqual(
				self.譀鏡.看型(華語新結構句物件, 物件分詞符號=' '),
				'我們 要 去吃飯 。'
			)
		
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_章物件的結果是章物件(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		結果章物件, _, _ = self.翻譯工具.翻譯(self.華語章物件)
		self.assertIsInstance(結果章物件, 章)
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_章物件的來源新結構章物件(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		_, 華語新結構章物件, _ = self.翻譯工具.翻譯(self.華語章物件)
		self.assertIsInstance(華語新結構章物件, 章)
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_結果章物件長度佮原本一樣(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		結果章物件, _, _ = self.翻譯工具.翻譯(self.華語章物件)
		self.assertEqual(len(結果章物件.內底句), len(self.華語章物件.內底句))
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_新結構章物件長度佮原本一樣(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		_, 華語新結構章物件, _ = self.翻譯工具.翻譯(self.華語章物件)
		self.assertEqual(len(華語新結構章物件.內底句), len(self.華語章物件.內底句))
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_翻譯章物件的分數(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		_, _, 分數 = self.翻譯工具.翻譯(self.華語章物件)
		self.assertEqual(分數, -21.66 - 21.66)
	@patch('臺灣言語工具.翻譯.斷詞斷字翻譯.斷詞斷字翻譯._翻譯句物件')
	def test_章物件是一句一句翻譯(self, 翻譯句物件mock):
		翻譯句物件mock.return_value = None, None, -21.66
		self.翻譯工具.翻譯(self.華語章物件)
		翻譯句物件mock.assert_has_calls(
			[call(self.華語句物件), call(self.華語句物件二)],
			any_order=True
		)
	def _組陣列分開包做句物件(self, 組陣列):
		句物件 = 句()
		for 組物件 in 組陣列:
			集物件 = 集()
			集物件.內底組 = [組物件]
			句物件.內底集.append(集物件)
		return 句物件
