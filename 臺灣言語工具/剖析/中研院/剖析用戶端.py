# -*- coding: utf-8 -*-
from 臺灣言語工具.斷詞.中研院.用戶端連線 import 用戶端連線
from 臺灣言語工具.剖析.中研院.剖析結構化工具 import 剖析結構化工具


class 剖析用戶端(用戶端連線):
	def __init__(self, 主機='140.109.19.112', 連接埠=8000, 編碼='Big5',
			帳號='ihcaoe', 密碼='aip1614'):
		super(剖析用戶端, self).__init__(主機, 連接埠, 編碼, 帳號, 密碼)
		
		self.結構化工具 = 剖析結構化工具()

	def 語句剖析後結構化(self, 語句, 等待=10, 一定愛成功=False):
		語句結果 = self.語句剖析做語句(語句, 等待, 一定愛成功)
		結構化結果 = []
		for 一逝字 in 語句結果:
			一逝結構化 = []
			for 一句 in 一逝字:
				一逝結構化.append(self.結構化工具.結構化剖析結果(一句))
			結構化結果.append(一逝結構化)
		return 結構化結果

	def 語句剖析做語句(self, 語句, 等待=10, 一定愛成功=False):
		return self._語句做了嘛是語句(語句, 等待, 一定愛成功)
