# -*- coding: utf-8 -*-

from 臺灣言語工具.基本元素.集 import 集
from 臺灣言語工具.基本元素.句 import 句
from 臺灣言語工具.基本元素.章 import 章


class 揀集內組:
	def 揀(self,章物件,集選擇):
		揀出來的章物件=章()
		所在 = 0
		for 句物件 in 章物件.內底句:
			集陣列 = []
			for 集物件 in 句物件.內底集:
				if 所在 < len(集選擇):
					選擇 = 集選擇[所在]
				else:
					選擇 = 0
				所在 += 1
				if 選擇 < len(集物件.內底組):
					組陣列 = 集物件.內底組[選擇:選擇 + 1]
				else:
					組陣列 = 集物件.內底組[:1]
				集物件 = 集()
				集物件.內底組 = 組陣列
				集陣列.append(集物件)
			句物件 = 句()
			句物件.內底集 = 集陣列
			揀出來的章物件.內底句.append(句物件)
		return 揀出來的章物件
