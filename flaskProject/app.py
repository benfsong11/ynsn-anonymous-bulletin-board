from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


# 게시물 업로드하기 API
@app.route('/post/upload', methods=['POST'])
def upload_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
        'like': 0
    }

    db.posts.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '업로드 완료!'})


# 게시물 공감 누르기 API
@app.route('/post/like', methods=['POST'])
def like_post():
    title_receive = request.form['title_give']

    target_post = db.posts.find_one({'title': title_receive})
    current_like = target_post['like']
    new_like = current_like + 1

    db.posts.update_one({'title': title_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success', 'msg': '공감 완료!'})


# 게시물 삭제하기 API
@app.route('/post/delete', methods=['POST'])
def delete_post():
    title_receive = request.form['title_give']
    db.posts.delete_one({'title': title_receive})

    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# 게시물 보여주기 API
@app.route('/post/list', methods=['GET'])
def view_post():
    posts = list(db.posts.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'all_posts': posts})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
