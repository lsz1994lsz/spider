# -*- coding: utf-8 -*-
import re





class Util():
	




    #截取字符串,以startStr开始,以endStr结束的中间一段
    @classmethod
    def getMidContent(self,startStr , endStr , text):
	patternStr = '.*%s(.*)%s.*' % (startStr,endStr)

	p = re.compile(patternStr,re.DOTALL)
	m = p.match(text)

	if m:
	    return m.group(1)
	else:
	    return None
