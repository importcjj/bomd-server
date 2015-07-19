#coding:utf-8

# bomd首页的名言模块
# time 2015-7-15
# author cjj

import random

_maxim_list = [
'作为一个真正的程序员，首先应该尊重编程，热爱你所写下的程序，他是你的伙伴，而不是工具。',
'程序员可以让步，却不可以退缩，可以羞涩，却不可以软弱，总之，程序员必须是勇敢的。',
'编程是一种单调的生活，因此程序员比普通人需要更多的关怀，更多的友情。',
'程序不是年轻的专利，但是，他属于年轻。',
'没有情调，不懂浪漫，也许这是程序员的一面，但拥有朴实无华的爱是他们的另一面。',
'一个好汉三个帮，程序员同样如此。',
'一个100行的代码调试都可能会让程序员遇到很多挫折，所以，面对挫折，我们永远不能低头。',
'调试完一个动态连接函数，固然值得兴奋，但真正的成功远还在无数个函数之后。',
'程序是我的生命，但我相信爱她甚过爱我的生命。',
'信念和目标，必须永远洋溢在程序员内心。',
'就算我们站在群山之颠，也别忘记雄鹰依旧能从我们头顶飞过。骄傲是比用JAVA进行底层开发更可笑的东西。',
'这句话不是很文雅，彻底鄙视那些害怕别人超越自己而拒绝回答别人问题的程序员。',
'如果调试一个程序让你很苦恼，千万不要放弃，成功永远在拐角之后，除非你走到拐角，否则你永远不知道你离他多远，所以，请记住，坚持不懈，直到成功。',
'最累的时候，家人是你最好的归宿。',
'退一步海阔天空，这是一种应有的心境。',
'如果你喜欢底层开发，千万不要勉强自己去搞VC，找到你最真实的想法，程序员最不能忍受的就是万精油。',
'IF（BOOL 学习= =FALSE）BOOL 落后=TRUE；不断的学习，我们才能不断的前进。',
'你的一个程序有时正常有时不正常，而你已经完全遵循编程的规则，为什么？事实上我认为相信只要遵循别人所说就能得到想当然的结果的人其实是个傻瓜。',
'编程中我们会遇到多少挫折？表放弃，沙漠尽头必是绿洲。',
'非优秀的程序员常常把空间和时间消耗殆尽，优秀的程序员则总是有足够的空间和时间去完成编程任务，而且配合近乎完美。',
'我们应该重视团队的精神，一个人作用再大，也不过是一碗水中比较大的一粒水珠而已。',
'无私奉献不是天方夜谭，有时候，我们也可以做到。'
]


def maxim():
	try:
		_maxim = random.choice(_maxim_list)
	except:
		_maxim = '--程序员名言'
	return _maxim


