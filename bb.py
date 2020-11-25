from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import config
import aa

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
spider = aa.Spider_Crawl()
url = "http://www.xbiquge.la"


class Aa(db.Model):
    __tablename__ = 'aa'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(64))


class Bb(db.Model):
    __tablename__ = 'bb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url_list = db.Column(db.String(64))
    txt = db.Column(db.Text)
    a_id = db.Column(db.Integer, db.ForeignKey(Aa.id))


@app.route("/")
def index():
    html = spider.get_url(url)
    detail_vote = spider.parse(html)
    for key in detail_vote:
        s = Aa(name=key, url=detail_vote[key])
        db.session.add(s)
        db.session.commit()

    aa = Aa.query.all()
    return render_template("index.html", aa=aa)


@app.route("/long/<id>")
def long(id):
    den = Aa.query.filter(Aa.id == id).first()
    html = spider.get_url(den.url)
    detail_d = spider.detail_parse(html)
    print(detail_d)
    for key in detail_d:
        g_url = "http://www.xbiquge.la" + detail_d[key]
        s = Bb(name=key, url_list=g_url, a_id=den.id)
        db.session.add(s)
        db.session.commit()

    bb = Bb.query.all()
    return render_template("long.html", bb=bb)

#
# @app.route("/xia/<id>")
# def xia(id):
#     aen = Bb.query.filter(Bb.id == id).first()
#     html = spider.get_url(aen.url)
#     denta_xia = spider.detail_a(html)
#     aabb = Bb(txt=denta_xia, a_id=aen.a_id)
#     db.session.add(aabb)
#     db.session.commit()
#     cc = Bb.query.all()
#     return render_template("xia.html", cc=cc)


# @app.route("/xia/<id>")
# def xia(id):
#     detail = Bb.query.filter(Bb.id == id).first()
#     title = detail.name
#     print("----------------------------", title)
#     html = spider.get_url(detail.url)
#     content = spider.read_parse(html)
#     return render_template("xia.html", content=content, title=detail.list_name)


@app.route("/xia/<id>")
def xia(id):
        detail = Bb.query.filter(Bb.id == id).first()
        title = detail.name
        html = spider.get_url(detail.url_list)
        # print(html)
        content = spider.read_parse(html)
        detail.list_content = content
        print(content)
        db.session.commit()
        return render_template("xia.html", content=content, title=title)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)