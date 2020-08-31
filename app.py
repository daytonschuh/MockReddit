from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from pytz import timezone
import pytz
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'posts.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


def get_pst_time():
    # date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    # pstDateTime=date.strftime(date_format)
    pstDateTime = date
    return pstDateTime

# Landing
@app.route('/', methods=['GET', 'POST'])
def home():
    global user_name
    global auth
    if request.method == 'POST':
        user_name = request.form.get('')
        auth = request.form.get('authToken')
    return render_template("index.html", user_name=user_name, auth=auth)

# Register a user
@app.route('/api/v1/register', methods=['POST'])
def register():
    form = request.form
    email = form['email']
    user_name = form['user_name']
    test = User.query.filter_by(email=email).first() and User.query.filter_by(user_name=user_name).first()
    if test:
        return jsonify(message='That email or username already exists.'), 409
    else:
        user_name = form['user_name']
        first_name = form['first_name']
        last_name = form['last_name']
        password = form['password']
        karma = form['karma']
        create_time = get_pst_time()
        modify_time = get_pst_time()
        user = User(user_name=user_name, first_name=first_name, last_name=last_name, email=email, password=password,
                    karma=karma, create_time=create_time, modify_time=modify_time)
        db.session.add(user)

        db.session.commit()
        return jsonify(message='User created successfully!'), 201


# Update user email
@app.route('/api/v1/update_email', methods=['PUT'])
def update_email():
    form = request.form
    user_name = form['user_name']
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        user.email = form['email']
        user.modify_time = get_pst_time()
        db.session.commit()
        return jsonify(message='Email updated successfully!'), 202
    else:
        return jsonify(message='Failed to update email!'), 404


# Increment karma for user
@app.route('/api/v1/increment_karma', methods=['PUT'])
def increment_karma():
    form = request.form
    user_name = form['user_name']
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        user.karma += 1
        user.modify_time = get_pst_time()
        db.session.commit()
        return jsonify(message='Karma incremented successfully!'), 202
    else:
        return jsonify(message='Failed to increment karma!'), 404


# Decrement karma for user
@app.route('/api/v1/decrement_karma', methods=['PUT'])
def decrement_karma():
    form = request.form
    user_name = form['user_name']
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        user.karma -= 1
        user.modify_time = get_pst_time()
        db.session.commit()
        return jsonify(message='Karma decremented successfully!'), 202
    else:
        return jsonify(message='Failed to decrement karma!'), 404


# Delete a user
@app.route('/api/v1/deactivate_account/<int:user_id>', methods=['DELETE'])
def remove_account(user_id):
    user_name = User.query.filter_by(user_id=user_id).first()
    if user_name:
        db.session.delete(user_name)
        db.session.commit()
        return jsonify(message="User deleted successfully!"), 202
    else:
        return jsonify(message="Failed to delete user!"), 404


# Create a post
@app.route('/api/v1/create_post', methods=['POST'])
def create_post():
    form = request.form
    user_name = form['user_name']
    test = User.query.filter_by(user_name=user_name).first()
    if test:
        post_id = form['post_id']
        user_name = form['user_name']
        title = form['title']
        text = form['text']
        community = form['community']
        resource_url = form['resource_url']
        create_time = get_pst_time()
        modify_time = get_pst_time()
        post = Post(post_id=post_id, user_name=user_name, title=title, text=text, community=community, resource_url=resource_url,
                    create_time=create_time, modify_time=modify_time)
        vote = Vote(post_id=post_id, votes=0, up_votes=0, down_votes=0,
                    create_time=create_time, modify_time=modify_time)
        db.session.add(post)
        db.session.add(vote)
        db.session.commit()
        return jsonify(message='Post created successfully!'), 201
    else:
        return jsonify(message='Failed to create post!'), 409

# Delete a post
@app.route('/api/v1/delete_post/<int:post_id>', methods=['DELETE'])
def remove_post(post_id: int):
    post = Post.query.filter_by(post_id=post_id).first()
    vote = Vote.query.filter_by(post_id=post_id).first()
    if post:
        db.session.delete(post)
        db.session.delete(vote)
        db.session.commit()
        return jsonify(message="Post deleted successfully!"), 202
    else:
        return jsonify(message="Failed to delete post!"), 404


# Retrieve a post
@app.route('/api/v1/retrieve_post/<int:id>', methods=['GET'])
def retrieve_post(id: int):
    post = Post.query.filter_by(post_id=id).first()
    if post:
        result = {'post':post_schema.dump(post), 'message':'Post retrieved successfully!'}
        return jsonify(result), 202
    else:
        return jsonify(message="Failed to retrieve post!"), 404


# Retrieve a list of posts from a community
@app.route('/api/v1/list_posts_comm/<string:community>/<int:number>', methods=['GET'])
def list_post_comm(community: str, number: int):
    post = Post.query.filter_by(community=community).order_by(Post.create_time.desc()).limit(number)
    if post:
        result = {'posts':posts_schema.dump(post), 'message':'Posts retrieved successfully!'}
        return jsonify(result), 202
    else:
        return jsonify('Failed to retrieve posts!'), 404


# Retrieve a specific number of posts
@app.route('/api/v1/list_posts/<int:number>', methods=['GET'])
def list_posts(number: int):
    posts_list = Post.query.order_by(Post.create_time.desc()).limit(number)
    if posts_list:
        result = {'posts':posts_schema.dump(posts_list), 'message':'Posts retrieved successfully!'}
        return jsonify(result), 202
    else:
        return jsonify('Failed to retrieve posts!'), 404

    
# Upvote a post
@app.route('/api/v1/up_vote_post/<int:post_id>', methods=['PUT'])
def up_vote_post(post_id: int):
    vote = Vote.query.filter_by(post_id=post_id).first()
    if vote:
        vote.votes += 1
        vote.up_votes += 1
        vote.modify_time = get_pst_time()
        db.session.commit()
        return jsonify(message='Post upvoted successfully!'), 202
    else:
        return jsonify('Failed to upvote post!'), 404


# Downvote a post
@app.route('/api/v1/down_vote_post/<int:post_id>', methods=['PUT'])
def down_vote_post(post_id: int):
    vote = Vote.query.filter_by(post_id=post_id).first()
    if vote:
        vote.votes -= 1
        vote.down_votes += 1
        vote.modify_time = get_pst_time()
        db.session.commit()
        return jsonify(message='Post downvoted successfully!'), 202
    else:
        return jsonify(vote), 404


# Retrieve post votes
@app.route('/api/v1/list_post_votes/<int:post_id>', methods=['GET'])
def list_post_votes(post_id: int):
    vote = Vote.query.filter_by(post_id=post_id).order_by().first()
    if vote:
        result = {'vote':vote_schema.dump(vote), 'message':'Votes retrieved successfully!'}
        return jsonify(result), 202
    else:
        return jsonify(message="That post does not exist"), 404


# Send a message
@app.route('/api/v1/send_message', methods=['POST'])
def send_message():
    form = request.form
    user_to = form['user_to']
    user_from = form['user_from']
    test = User.query.filter_by(user_name=user_to).first()
    test2 = User.query.filter_by(user_name=user_from).first()
    if test and test2:
        contents = form['contents']
        flag = form['flag']
        message_id = form['message_id']
        create_time = get_pst_time()

        message = Message(message_id=message_id, user_from=user_from, user_to=user_to, contents=contents, flag=flag, create_time=create_time)
        db.session.add(message)
        db.session.commit()
        return jsonify(message='Message sent successfully!'), 201
    else:
        return jsonify(message='Failed to send message!'), 409


# Delete a message
@app.route('/api/v1/delete_message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id: int):
    message = Message.query.filter_by(message_id=message_id).first()
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify(message="Message deleted successfully!"), 202
    else:
        return jsonify(message="Failed to delete message!"), 404


# Favorite a message
@app.route('/api/v1/favorite_message/<int:message_id>', methods=['PUT'])
def list_favorite_messages(message_id: int):
    message = Message.query.filter_by(message_id=message_id)
    if message:
        message.flag = 'Favorite'
        result = message_schema.dump(message)
        return jsonify(result)
    else:
        return jsonify(message="Failed to favorite a message!"), 404
    
    
# database models
class User(db.Model):
    __tablename__ = 'tb_users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    karma = Column(Integer, default=0)
    create_time = Column(DateTime, default=get_pst_time())
    modify_time = Column(DateTime, default=get_pst_time())


class Post(db.Model):
    __tablename__ = 'tb_posts'
    post_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    title = Column(String)
    text = Column(String)
    community = Column(String)
    resource_url = Column(String)
    create_time = Column(DateTime, default=get_pst_time())
    modify_time = Column(DateTime, default=get_pst_time())


class Vote(db.Model):
    __tablename__ = 'tb_votes'
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    votes = Column(Integer, default=0)
    up_votes = Column(Integer, default=0)
    down_votes = Column(Integer, default=0)
    create_time = Column(DateTime, default=get_pst_time())
    modify_time = Column(DateTime, default=get_pst_time())


class Message(db.Model):
    __tablename__ = 'tb_messages'
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_from = Column(String)
    user_to = Column(String)
    contents = Column(String)
    flag = Column(String)
    create_time = Column(DateTime, default=get_pst_time())


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'user_name', 'first_name', 'last_name', 'email', 'password', 'karma', 'create_time', 'modify_time')


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name', 'title', 'text', 'community', 'resource_url', 'create_time', 'modify_time')


class VoteSchema(ma.Schema):
    class Meta:
        fields = ('post_id', 'votes', 'up_votes', 'down_votes', 'create_time', 'modify_time')


class MessageSchema(ma.Schema):
    class Meta:
        fields = ('message_id', 'user_from', 'user_to', 'contents', 'flag', 'create_time')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

vote_schema = VoteSchema()
votes_schema = VoteSchema(many=True)

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

if __name__ == '__main__':
    app.run()
