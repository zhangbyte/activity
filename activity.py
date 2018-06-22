#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
import json
from db.db import User, Activity, Star, Registration
import os
from util import utils
from util import const

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def success_response(data=None):
    return json.dumps({
        'error': False,
        'msg': None,
        'data': data
    })


def error_response(msg=None):
    return json.dumps({
        'error': True,
        'msg': msg,
        'data': None
    })


# 身份校验
def auth(func):
    def wrapper(*args, **kw):
        if not request.values.get('user_id', None):
            return error_response('Access denied!')
        return func(*args, **kw)

    return wrapper


# 组织者身份校验
def auth2(func):
    def wrapper(*args, **kw):
        # if not request.values.get('user_id', None) and int(request.values.get('type', 1)) != 2:
        #     return error_response('Access denied!')
        return func(*args, **kw)

    return wrapper


# 注册
@app.route('/sign-up', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    phone = request.form['phone']

    try:
        User(
            email=email,
            password=password,
            name=name,
            phone=phone
        ).save()
    except:
        return error_response()

    return success_response()


# 登录
@app.route('/sign-in', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']

    try:
        user = User.get(email=email, password=password)
    except Exception, e:
        # print e
        return error_response()

    if user:
        return success_response({
            "user_id": user.user_id,
            "type": user.type,
        })
    else:
        return error_response()


# 上传图片
@app.route('/upload', methods=['POST'], endpoint='upload')
@auth
def upload():
    try:
        pic = request.files['pic']
        filename = utils.random_str() + '.' + pic.filename.rsplit('.', 1)[1]
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception, e:
        print e
        return error_response()

    return success_response({
        'pic_url': 'https://activity.duohuo.org/static/' + filename
    })


# 获取用户信息
@app.route('/user', methods=['GET'], endpoint='user')
@auth
def user():
    user_id = request.values['user_id']
    try:
        user = User.get(user_id=user_id)
    except:
        return error_response()

    return success_response({
        'name': user.name,
        'avatar_url': user.avatar_url,
        'gender': user.gender,
        'phone': user.phone,
        'email': user.email
    })


# 更新用户信息
@app.route('/user', methods=['POST'], endpoint='user_update')
@auth
def user_update():
    user_id = request.values['user_id']

    avatar_url = request.form.get('avatar_url', None)
    name = request.form.get('name', None)
    gender = request.form.get('gender', None)
    phone = request.form.get('phone', None)

    try:
        user = User.get(user_id=user_id)
        user.avatar_url = avatar_url if avatar_url else user.avatar_url
        user.name = name if name else user.name
        user.gender = gender if gender else user.gender
        user.phone = phone if phone else user.phone
        user.save()
    except Exception, e:
        # print e
        return error_response()

    return success_response()


# 发布活动
@app.route('/activity', methods=['POST'], endpoint='activity_post')
@auth2
def activity_post():
    user_id = request.values['user_id']

    title = request.form['title']
    tags = request.form['tags']
    sort = request.form['sort']
    place = request.form['place']
    description = request.form['description']
    guests = request.form['guests']
    activity_img = request.form['activity_img']
    date = request.form['date']

    try:
        Activity(
            user_id=user_id,
            title=title,
            tags=tags,
            sort=sort,
            place=place,
            description=description,
            guests=guests,
            activity_img=activity_img,
            date=utils.timestamp2datetime(date)
        ).save()
    except Exception, e:
        print e
        return error_response()

    return success_response()


# 获取活动详情
@app.route('/activity', methods=['GET'], endpoint='activity')
@auth
def activity():
    activity_id = request.args['activity_id']

    try:
        activity = Activity.get(activity_id=activity_id)
        user = User.get(user_id=activity.user_id)
    except Exception, e:
        print e
        return error_response()

    return success_response({
        'title': activity.title,
        'date': utils.datetime2timestamp(activity.date),
        'place': activity.place,
        'stars': activity.stars,
        'tags': activity.tags,
        'sort': activity.sort,
        'activity_img': activity.activity_img,
        'description': activity.description,
        'guests': activity.guests,
        'organizer_name': user.name,
        'organizer_id': user.user_id,
        'organizer_avatar': user.avatar_url
    })


# 修改活动
@app.route('/activity/update', methods=['POST'], endpoint='activity_update')
@auth2
def activity_update():
    user_id = request.values['user_id']

    activity_id = request.form['activity_id']
    title = request.form.get('title', None)
    tags = request.form.get('tags', None)
    sort = request.form.get('sort', None)
    place = request.form.get('place', None)
    description = request.form.get('description', None)
    guests = request.form.get('guests', None)
    activity_img = request.form.get('activity_img', None)
    date = request.form.get('date', None)

    try:
        activity = Activity.get(activity_id=activity_id, user_id=user_id)

        activity.title = title if title else activity.title
        activity.tags = tags if tags else activity.tags
        activity.sort = sort if sort else activity.sort
        activity.place = place if place else activity.place
        activity.description = description if description else activity.description
        activity.guests = guests if guests else activity.guests
        activity.activity_img = activity_img if activity_img else activity.activity_img
        activity.date = date if date else activity.date

        activity.save()
    except Exception, e:
        print e
        return error_response()

    return success_response()


# 删除活动
@app.route('/activity/delete', methods=['POST'], endpoint='activity_delete')
@auth2
def activity_delete():
    user_id = request.values['user_id']
    activity_id = request.form['activity_id']

    try:
        Activity.delete().where(
            Activity.activity_id == activity_id,
            Activity.user_id == user_id
        ).execute()
    except Exception, e:
        print e
        return error_response()

    return success_response()


# 点赞
@app.route('/star', methods=['POST'], endpoint='star')
@auth
def star():
    user_id = request.values['user_id']
    activity_id = request.form['activity_id']

    try:
        Star(
            activity_id=activity_id,
            user_id=user_id
        ).save()
    except:
        return error_response()

    return success_response()


# 取消点赞
@app.route('/star/delete', methods=['POST'], endpoint='star_delete')
@auth
def star_delete():
    user_id = request.values['user_id']
    activity_id = request.form['activity_id']

    try:
        Star.delete().where(
            Star.activity_id == activity_id,
            Star.user_id == user_id
        ).execute()
    except:
        return error_response()

    return success_response()


# 判断点赞关系
@app.route('/star', methods=['GET'], endpoint='is_star')
@auth
def is_star():
    user_id = request.values['user_id']
    activity_ids = request.args['activity_ids']
    activity_ids = json.loads(activity_ids)

    try:
        stars = Star.select().where(
            Star.user_id == user_id
        )
    except Exception, e:
        print e
        return error_response()

    result = {}
    for activity_id in activity_ids:
        result[activity_id] = 0
    for star in stars:
        if result.get(star.activity_id, None) == 0:
            result[star.activity_id] = 1

    return success_response(result)


# 报名
@app.route('/join', methods=['POST'], endpoint='join')
@auth
def join():
    user_id = request.values['user_id']
    activity_id = request.form['activity_id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    gender = request.form['gender']

    try:
        Registration(
            activity_id=activity_id,
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            gender=gender
        ).save()
    except:
        return error_response()

    return success_response()


# 报名情况
@app.route('/join/result', methods=['GET'], endpoint='join_result')
@auth2
def join_result():
    user_id = request.values['user_id']
    activity_id = request.args['activity_id']

    try:
        activity = Activity.get(activity_id=activity_id, user_id=user_id)
        registrations = Registration.select().where(
            Registration.activity_id == activity_id
        )
    except Exception, e:
        print e
        return error_response()

    result = []
    for registration in registrations:
        result.append({
            'name': registration.name,
            'gender': registration.gender,
            'phone': registration.phone,
            'email': registration.email,
            'create_time': utils.datetime2timestamp(registration.create_time)
        })

    return success_response({
        'stars': activity.stars,
        'registration': result
    })


# 活动title搜索
@app.route('/search', methods=['GET'])
def search():
    text = request.args['text']
    search_text = '%'+text+'%'

    try:
        activitys = Activity.select().where(Activity.title % search_text)
    except:
        return error_response()

    result = []
    for activity in activitys:
        result.append({
            'activity_id': activity.activity_id,
            'title': activity.title,
            'date': utils.datetime2timestamp(activity.date),
            'place': activity.place,
            'activity_img': activity.activity_img
        })

    return success_response(result)


# activity Model -> dict
def mk_activity_result(activitys):
    result = []
    for activity in activitys:
        result.append({
            'activity_id': activity.activity_id,
            'title': activity.title,
            'date': utils.datetime2timestamp(activity.date),
            'place': activity.place,
            'activity_img': activity.activity_img
        })

    return result


# 发布活动列表
@app.route('/activity/list/post', methods=['GET'], endpoint='activity_list_post')
@auth2
def activity_list_post():
    user_id = request.values['user_id']

    try:
        activitys = Activity.select().where(
            Activity.user_id == user_id
        )
    except:
        return error_response()

    return success_response(mk_activity_result(activitys))


# 加入活动列表
@app.route('/activity/list/join', methods=['GET'], endpoint='activity_list_join')
@auth
def activity_list_join():
    user_id = request.values['user_id']

    try:
        activity_ids = Registration.select(Registration.activity_id).where(
            Registration.user_id == user_id
        )
        activitys = Activity.select().where(
            Activity.activity_id.in_(activity_ids)
        )
    except:
        return error_response()

    return success_response(mk_activity_result(activitys))


# 点赞活动列表
@app.route('/activity/list/star', methods=['GET'], endpoint='activity_list_star')
@auth
def activity_list_star():
    user_id = request.values['user_id']

    try:
        activity_ids = Star.select(Star.activity_id).where(
            Star.user_id == user_id
        )
        activitys = Activity.select().where(
            Activity.activity_id.in_(activity_ids)
        )
    except:
        return error_response()

    return success_response(mk_activity_result(activitys))


# 分类活动列表
@app.route('/activity/list/sort', methods=['GET'], endpoint='activity_list_sort')
@auth
def activity_list_sort():
    sort = request.args['sort']

    try:
        activitys = Activity.select().where(
            Activity.sort == sort
        )
    except:
        return error_response()

    return success_response(mk_activity_result(activitys))


# 活动列表
@app.route('/activity/list', methods=['GET'], endpoint='activity_list')
def activity_list():
    time_type = request.args.get('time_type', None)
    limit_time = const.LIMIT_TIME[time_type] if time_type else None

    try:
        if not limit_time:
            activitys = Activity.select()
        elif time_type == const.TIME_TYPE_TOMORROW:
            activitys = Activity.select().where(
                Activity.date > utils.get_tomorrow(),
                Activity.date < limit_time
            )
        else:
            activitys = Activity.select().where(
                Activity.date > utils.get_today_start(),
                Activity.date < limit_time
            )
    except:
        return error_response()

    return success_response(mk_activity_result(activitys))


if __name__ == '__main__':
    app.run(port=6000)
