#coding:utf-8
# render_template("index.html", user=username, title=title, img=img)
# render_template("index.html", title=title, img=img)
# render_template('regist.html')
# render_template('login.html')
# render_template("about.html", title="关于作者")
# render_template("userZone.html", user=username, themes=themes)
# render_template('Articles.html', num='all', articles=sub_meeted_articles, title="所有博文", tips=tips, maxPage=maxPage, pageID=pageID, searchfor=searchfor)
# render_template('Articles.html', num='all', articles = articles, title="所有博文", maxPage=maxPage, pageID=pageID, searchfor=searchfor)
# render_template('Articles.html', num='one', article = Essay, lock = essayLock, title=essayTitle, comments=comments, nickname=nickname, email=email)
# render_template('Resources.html', resources = resources)
import Maxims


class TemplateSettingDict(dict):
	_theme = 'highlight.css'

	def __init__(self, **kwargs):
		# print kwargs.update(theme=self.theme, maxim=self.maxim)
		self._maxim = Maxims.maxim()
		super(TemplateSettingDict, self).__init__(kwargs, theme=self._theme, maxim=self._maxim)

	def setTheme(self, new_theme):
		self._theme = new_theme

	def args(self):
		print self.items()


if __name__ == '__main__':
	dt = TemplateSettingDict(title='关于bomd')
	# for key, item in dt.items():
	# 	print ': '.join((key, item))
	dt.args()