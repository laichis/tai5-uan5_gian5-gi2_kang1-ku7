# -*- coding: utf-8 -*-
from 臺灣言語工具.基本元素.章 import 章
from 臺灣言語工具.解析整理.參數錯誤 import 參數錯誤
from math import log10
from math import pow


from 臺灣言語工具.語言模型.語言模型 import 語言模型


class 實際語言模型(語言模型):
	基本 = 0.02
	權重 = [0.08, 0.2, 0.7]

	def __init__(self, 上濟詞數):
		if 上濟詞數 <= 0:
			raise 參數錯誤('詞數愛是正整數，傳入來的是{0}'.format(上濟詞數))
		self._上濟詞數 = 上濟詞數
		self.總數表 = [0] * self.上濟詞數()
		self.連詞表 = {}

	def 上濟詞數(self):
		return self._上濟詞數

	def 評詞陣列分(self, 詞陣列, 開始的所在=0):
		for 所在 in range(開始的所在, len(詞陣列)):
			分數 = self.感覺(詞陣列[max(0, 所在 + 1 - self.上濟詞數()):所在 + 1])
			try:
				分數 += 詞陣列[所在].屬性['機率']
			except:
				pass
			yield 分數

	def 感覺(self, 語句):
		條件 = self.條件(語句)
		分數 = self.基本
		for 分, 權 in zip(條件, self.權重):
			分數 += self.指數(分) * 權
		return self.對數(分數)

	def 總數(self):
		return self.總數表

	def 數量(self, 連詞):
		數量表 = []
		for 長度 in range(min(self.上濟詞數(), len(連詞))):
			組合 = tuple(連詞[-1 - 長度:])
			if 組合 in self.連詞表:
				數量表.append(self.連詞表[組合])
			else:
				數量表.append(0)
		return 數量表

	def 機率(self, 連詞):
		數量表 = self.數量(連詞)
		機率表 = []
		for 數, 總 in zip(數量表, self.總數表):
			if 數 == 0:
				機率表.append(self.無看過)
			else:
				機率表.append(self.對數(數 / 總))
		return 機率表

	def 條件(self, 連詞):
		'''條件機率'''
		if 連詞 == [self.開始()]:
			return [self.對數(1.0)]
		數量表 = self.數量(連詞)
		前數量表 = self.數量(連詞[:-1])
		條件表 = []
# 		print('數量表', 數量表)
# 		print('前數量表', 前數量表, self.總數表[:1],)
		for 數, 前 in zip(數量表, self.總數表[:1] + 前數量表):
			if 數 == 0:
				條件表.append(self.無看過)
			else:
				條件表.append(self.對數(數 / 前))
# 		print('條件表',條件表)
		return 條件表

	def 看(self, 物件):
		if isinstance(物件, 章):
			self.看章物件(物件)
			return
		詞陣列 = [self.開始()] + self._網仔.網出詞物件(物件) + [self.結束()]
		for 長度 in range(1, self.上濟詞數() + 1):
			for 所在 in range(len(詞陣列) - 長度 + 1):
				self.總數表[長度 - 1] += 1
				組合 = tuple(詞陣列[所在:所在 + 長度])
				if 組合 not in self.連詞表:
					self.連詞表[組合] = 1
				else:
					self.連詞表[組合] += 1
		return

	def 看章物件(self, 章物件):
		for 句物件 in 章物件.內底句:
			self.看(句物件)
		return

	def 對數(self, 數字):
		return log10(數字)

	def 指數(self, 數字):
		return pow(10.0, 數字)
