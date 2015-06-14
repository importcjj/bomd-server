# coding:utf-8
import os
import sys
import pages
from config import *
# import sqlite4comment as db4comment
# import sqlite4essay as db4essay
import mysql4comment as db4comment
import mysql4essay as db4essay
from sae.storage import Bucket, Connection

from flask import Flask
from flask import render_template, url_for, request, redirect, make_response, session
reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)
app.secret_key = 'm\xf8>I\xa9\xbf\x05\x81\xf3\xf0\x9aA\xab%1s\xff5\xe6D\x99\xbc%\xa2'


#首页的处理逻辑
@app.route('/')
@app.route('/index')
def index():
    title = 'Stay with me'
    img = url_for('static', filename='images/baby.jpg')
    # username = request.cookies.get('username')
    username = session.get('username')
    if username:
        return render_template("index.html", user=username, title=title, img=img)
    else:
        # return redirect("/login")
        return render_template("index.html", title=title, img=img)

#注册的处理逻辑
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    #暂时不开放注册功能
    return redirect('/index')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password and username not in user_list:
            headimage = request.files['headimage']
            headimage.save(file_path + os.sep + headimage.filename)
            user_list[username] = password
            session['username'] = username
            return redirect('/index')
        else:
            return redirect('/regist')
    else:
        return render_template('regist.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    #暂时不开放登陆
    return redirect('/index')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_list.has_key(username) and user_list[username] == password:
            # response = make_response(redirect('/index/'))
            # response.set_cookie('username', value=username, max_age=300)
            # return response
            session['username'] = username
            return redirect('/index')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')

#关于页面
@app.route('/about')
def about():

    return render_template("about.html", title="关于作者")
    
    
@app.route("/userzone")
def zone():
    #暂时不开放用户中心
    return redirect('/index')
    username = request.args.get('name')
    if session.has_key('username'):
        
        if username == session['username']:
            return render_template("userZone.html", user=username, themes=themes)
        else:
            return redirect('/userzone?name=%s' % session['username'])
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    #暂时不开放用户功能
    return redirect('/index')
    # response = make_response(redirect('/index/'))
    # response.set_cookie('username', value='', max_age=0)
    # return response
    del session['username']
    return redirect('/index')


#本地库上传文章或资源的处理逻辑
@app.route('/upload', methods=['POST'])
def upload():
        username = request.form.get('username')
        password = request.form.get('password')
        uploadType = request.form.get('upload_type')
        #验证合法的用户名和口令
        if username == ADMIN_NAME and password == ADMIN_PASSWORD:
            #如果上传是资源文件
            if uploadType == 'Resources':
                try:
                    resource = request.files['file']
                    filename = request.form.get('file_name')
                    conn = Connection(account=PROJECT_NAME)
                    bucket = conn.get_bucket('resources')
                    bucket.put_object(filename, resource.read())
                    #return bucket.generate_url(filename)
                    #print "User: %s has upload resource: %s"%(username, filename)
                    return u"(remote)资源上传成功: %s"%filename
                except:
                    return "(remote)资源上传失败: %s"%filename

            elif uploadType == 'Essays':
                essayBody = request.files['essay_body'].read()
                essayDate = request.form.get('essay_date')
                essayTitle = request.form.get('essay_title')
                essayLock = request.form.get('essay_lock')
                essayTag = request.form.get('essay_tag')
                try:
                    isRepeat = db4essay.SelectEssay(essayTitle)
                except Exception as e:
                    return u"(remote)抱歉!文章数据库异常，查重失败\nError:%s"%e.message

                if isRepeat:
                    try:
                        db4essay.UpdateEssay(essayTitle, essayDate, essayBody, essayLock, essayTag)
                        return "(remote)文章更新成功: %s"%essayTitle
                    except Exception as e:
                        return u"(remote)抱歉!文章数据库异常，更新失败\nError:%s"%e.message
                else:
                    try:
                        db4essay.InsertEssay(essayTitle, essayDate, essayBody, essayLock, essayTag)
                    except Exception as e:
                        return u"(remote)抱歉!文章数据库异常,发布失败\nError:%s"%e.message
                    else:
                        return "(remote)文章发布成功: %s"%essayTitle
        else:
            return u"(remote)抱歉!用户名或密码错误"


#本地库管理文章的处理逻辑
@app.route('/manage', methods=['POST'])
def manage():
    command = request.form.get('command')
    if command == "ls":
        articles = db4essay.listEssays()[::-1]
        return "\n".join(["%d. "%ID + title for ID, title in enumerate(artiles)])
    
    if command.startswith("del"):
        try:
            EssayID = int(command.split(' ')[1])
        except Exception as e:
            return "(remote)抱歉!删除命令有误\nError%s"%e.message
        try:
            ll = db4essay.DeleteEssay(EssayID)
        except Exception as e:
            return "(remote)抱歉!文章序号不正确，删除失败\nError%s"%e.message
        return "删除成功"

    return "不支持该命令"


# tags = ['python', 'Git', 'GitHub', 'Java', 'MongoDB', '普通', 'flask', 'MacOS', 'Linux',
#         'Unix', 'MarkDown', 'Objective-C', 'Swift', 'Ios开发', '生活', '疑问']


#有关文章的处理逻辑
@app.route('/articles', methods=['POST', 'GET'])
def Articles():
    searchfor = request.args.get('search')
    essayTitle = request.args.get('title')
    pageID = request.args.get('page')
    
    #如果有搜索参数
    if searchfor:
        
        try:
            articles = list(db4essay.listEssays()) # [title, uptime, pwd, tag] 时间 上传时间 访问密码 标签
            meeted_articles = [article for article in articles if searchfor in article[0] or searchfor in article[-1] ]
            tips = "" if meeted_articles else "抱歉！什么都没找到.."
            maxPage, pageID, sub_meeted_articles = pages.pageHandle(meeted_articles, 4, pageID)
        except Exception as e:
            return "出错啦!\n%s"%e.message
        else:
            return render_template('Articles.html', num='all', articles=sub_meeted_articles, title="所有博文", tips=tips, maxPage=maxPage, pageID=pageID, searchfor=searchfor)
    #如果没有标题,说明是显示文章列表
    if not essayTitle:
        try:
            articles = list(db4essay.listEssays())
            maxPage, pageID, articles = pages.pageHandle(articles, 4, pageID)
        except Exception as e:
            return "出错啦!\n%s"%e.message
        else:
            return render_template('Articles.html', num='all', articles = articles, title="所有博文", maxPage=maxPage, pageID=pageID, searchfor=searchfor)
    #如果有标题，说明就是某一文章的内容页
    else:
        nickname = session['nickname'] if session.has_key('nickname') else  ""
        email = session['email'] if session.has_key('email') else "" 
        try:
            Essay = db4essay.SelectEssay(essayTitle)        #从数据库取出相应标题的文章
            Essay = Essay[-5:]                              #标题， 时间， 访问密码， 正文， 标签
            comments = db4comment.getByTitle(essayTitle)    #取出该文章相应的评论
            # return "%d"%len(comments)
        except Exception as e:
            return "出错啦!\n%s"%e.message

        if request.method == 'GET':
            essayLock = session[essayTitle]if session.has_key(essayTitle) else ""
        #从某一文章的内容页post过来，则是验证加密文章的密码
        else: #POST method
            essayLock = request.form.get('lock')    
            if essayLock == Essay[2]: session[essayTitle] = essayLock
        return render_template('Articles.html', num='one', article = Essay, lock = essayLock, title=essayTitle, comments=comments, nickname=nickname, email=email)

   
#资源页面的处理逻辑
@app.route('/resources')
def Resources():
    conn = Connection(account=PROJECT_NAME)
    bucket = conn.get_bucket('resources')
    #一个obj就是一个资源文件
    #资源文件的url
    #资源文件上一次修改的时间
    #资源文件的大小
    resources = {obj.name:[bucket.generate_url(obj.name), obj.last_modified, obj.bytes] for obj in bucket.list()}
    return render_template('Resources.html', resources = resources)


#评论板块的处理逻辑
@app.route('/comment', methods=['POST','GET'])
def comment():
    essayTitle = request.args.get('article') #文章标题
    parentID = request.args.get('parentID')  #父评论的ID
    replyto = request.args.get('replyto')    #回复的对象的昵称
    username = request.form.get('username')  #回复人的昵称
    email = request.form.get('email')        #回复人的Email地址
    content = request.form.get('content')    #回复的内容
    
    #如果没有填写昵称或者Email地址，则提示错误
    if not username or not email or not comment:
        return "不要空哦"

    #没有回复对象，则说明回复的是文章
    if not replyto or not parentID:
        replyto = ""
        parentID = 0
    else:
        parentID = int(parentID)
    #保留评论人的信息
    session['nickname'] = username
    session['email'] = email
    res = db4comment.new_comment(essayTitle, username, email, parentID, replyto, content)
    return redirect('/articles?title=%s'%essayTitle)
    
