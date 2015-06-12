# coding:utf-8
from flask import Flask
from flask import render_template, url_for, request, redirect, make_response, session
from database4mysql import *
from logHelper import *
import mysql4comment as db4comment
import pages
from sae.storage import Bucket, Connection
import os
import sys
reload(sys)

app = Flask(__name__)

sys.setdefaultencoding('utf-8')


app.secret_key = 'm\xf8>I\xa9\xbf\x05\x81\xf3\xf0\x9aA\xab%1s\xff5\xe6D\x99\xbc%\xa2'

@app.route('/')
@app.route('/index')
def index():
    title = 'Stay with me'
    img = url_for('static', filename='images/baby.jpg')
    # nav_list = [u'头条', u'娱乐', u'体育', u'科技']
    print img
    # username = request.cookies.get('username')
    username = session.get('username')
    if username:
        return render_template("index.html",
                               user=username,
                               title=title,
                               # nagtive=nav_list,
                               img=img)
    else:
        # return redirect("/login")
        return render_template("index.html",
                               title=title,
                               # nagtive=nav_list,
                               img=img)


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print username, password

        if username and password and username not in user_list:
            headimage = request.files['headimage']
            headimage.save(file_path + os.sep + headimage.filename)

            # 讲注册信息存放到sqlite3数据库中
            # conn = sqlite3.connect('tmp/my.db')
            # cursor = conn.cursor()
            # sql = "insert into user (username,password) values (?,?)"
            # cursor.execute(sql, (username, password))
            # conn.commit()
            # cursor.close()
            # conn.close()

            # 将注册信息存放到列表中

            user_list[username] = password
            session['username'] = username
            return redirect('/index')
        else:
            return redirect('/regist')
    else:
        # request.args['username']
        return render_template('regist.html')


# user_list = {'jiaju': '1234', 'admin': 'admin'}


@app.route('/login', methods=['POST', 'GET'])
def login():
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

@app.route('/about')
def about():
    return render_template("about.html", title="关于作者")
    
    
@app.route("/userzone")
def zone():
    username = request.args.get('name')
    if session.has_key('username'):
        themes = os.listdir("static/default")
        
        if username == session['username']:
            return render_template("userZone.html", user=username, themes=themes)
        else:
            return redirect('/userzone?name=%s' % session['username'])
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    # response = make_response(redirect('/index/'))
    # response.set_cookie('username', value='', max_age=0)
    # return response
    del session['username']
    return redirect('/index')


# 文件的存储路径
file_path = 'static/resources'
ADMIN_NAME = "cjj"
ADMIN_PASSWORD = "cjj"

@app.route('/upload', methods=['POST'])
def upload():
        username = request.form.get('username')
        password = request.form.get('password')
        #return username+password
        if username == ADMIN_NAME and password == ADMIN_PASSWORD:

            uploadType = request.form.get('upload_type')

            if uploadType == 'Resources':
                try:
                    resource = request.files['file']
                    filename = request.form.get('file_name')
                    c = Connection(account='bomd')
                    bucket = c.get_bucket('resources')
                    bucket.put_object(filename, resource.read())
                    #return bucket.generate_url(filename)
                    #print "User: %s has upload resource: %s"%(username, filename)
                    return u"资源上传成功: %s"%filename
                except:
                    return "cuowu"

            elif uploadType == 'Essays':
                essayBody = request.files['essay_body'].read()
                essayDate = request.form.get('essay_date')
                essayTitle = request.form.get('essay_title')
                essayLock = request.form.get('essay_lock')
                essayTag = request.form.get('essay_tag')
                #return essayTitle
                try:
                    isRepeat = SelectEssay(essayTitle)
                except Exception as e:
                    log('log/dataBase.txt', e.message)
                    return u"数据库异常，查重失败 %s"%e.message

                if isRepeat:
                    try:
                        UpdateEssay(essayTitle, essayDate, essayBody, essayLock, essayTag)
                        return "文章更新成功: %s"%essayTitle
                    except Exception as e:
                        log('log/dataBase.log', e.message)
                        return u"数据库异常，更新失败 %s"%e.message
                try:
                    InsertEssay(essayTitle, essayDate, essayBody, essayLock, essayTag)
                except Exception as e:
                    log('log/dataBase.log', e.message)
                    return u"数据库异常,发布失败 %s"%e.message

                else:
                    print "User: %s has upload essay: %s"%(username, essayTitle)
                    return "文章发布成功: %s"%essayTitle
        else:
            # return redirect('/regist/')
            return u"用户名或密码错误"



@app.route('/manage', methods=['POST'])
def manage():
    command = request.form.get('command')
    if command == "ls":
        articles = listEssays()[::-1]
        #articles.reserve()
        num = len(articles)
        return "\n".join(["%d. "%ID + articles[ID-1][0] for ID in xrange(num, 0, -1)])
    
    if command.startswith("del"):
        try:
            
            EssayID = int(command.split(' ')[1])

        except Exception as e:
            return "删除命令有误 %s"%e.message
        try:
            ll = DeleteEssay(EssayID-1)
        except Exception as e:
            return "序号不正确，删除失败 %s"%e.message

        return "删除成功"

    return "不支持该命令"


tags = ['python', 'Git', 'GitHub', 'Java', 'MongoDB', '普通', 'flask', 'MacOS', 'Linux',
        'Unix', 'MarkDown', 'Objective-C', 'Swift', 'Ios开发', '生活', '疑问']


@app.route('/articles', methods=['POST', 'GET'])
def listArticles():
    searchfor = request.args.get('search')
    if searchfor:
        
        pageID = request.args.get('page')
        try:
            articles = list(listEssays())
            #articles.reverse()
            articles = [article for article in articles if searchfor in article[0] or searchfor in article[-1] ]
            tips = ""
            if not articles:
                tips = "抱歉！什么都没找到.."
            maxPage, pageID, articles = pages.pageHandle(articles, 4, pageID)
            return render_template('Articles.html', num='all', articles=articles, title="所有博文", tags=tags, tips=tips, maxPage=maxPage, pageID=pageID, searchfor=searchfor)
        except Exception as e:
            return e.message
        return render_template('Articles.html', num='all', articles =[], title="所有博文", tags=tags, tips=tips)

    essayTitle = request.args.get('title')

    if not essayTitle:
        pageID = request.args.get('page')
        try:
            articles = list(listEssays())
            #articles.reverse()
            maxPage, pageID, articles = pages.pageHandle(articles, 4, pageID)
            return render_template('Articles.html', num='all', articles = articles, title="所有博文", maxPage=maxPage, pageID=pageID, searchfor=searchfor)
        except Exception as e:
            return e.message
            return render_template('Articles.html', num='all', articles =[], title="所有博文")
    else:
        nickname = ""
        email = ""
        if session.has_key('nickname') and session.has_key('email'):
            nickname = session['nickname']
            email = session['email']
        try:
            Essay = SelectEssay(essayTitle)
            Essay = Essay[-5:]  #标题， 时间， 访问密码， 正文， 标签
            
            comments = db4comment.getByTitle(essayTitle)
            #return "".join(comments)
        except Exception as e:
            log('log/dataBase.log', e.message)
            return e.message
            

        if request.method == 'GET':
            essayLock = ""
            if session.has_key(essayTitle):
                essayLock = session[essayTitle]
            return render_template('Articles.html', num='one', article = Essay, lock = essayLock, title=essayTitle, comments=comments, nickname=nickname, email=email)
            
        else:   #POST method
            essayLock = request.form.get('lock')
                
            if essayLock == Essay[2]:
                    
                session[essayTitle] = essayLock
                    
            return render_template('Articles.html', num='one', article = Essay, lock = essayLock, title=essayTitle, comments=comments, nickname=nickname, email=email)
   

@app.route('/resources')
def listResources():
    c = Connection(account='bomd')
    bucket = c.get_bucket('resources')
    #一个obj就是一个资源文件
    resources = {obj.name:[bucket.generate_url(obj.name), obj.last_modified, obj.bytes] for obj in bucket.list()}
    #print resources
    return render_template('Resources.html', resources = resources)


#评论的处理逻辑
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
    
