from flask import Flask, render_template, request, jsonify
import os
import re
import datetime
import db
from models import iTunes


app = Flask(__name__)

# create the database and table. Insert 10 records
# Do this only once to avoid inserting the test books into
# the db multiple times
# if not os.path.isfile('iTunes.db'):
#     db.connect()

# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files


@app.route("/")
def index():
    return render_template("index.html")


def isValid(email):
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    title = req_data['title']
    artist = req_data['artist']
    album = req_data['album']
    mus = [m.serialize() for m in db.view()]
    for m in mus:
        if m['title'] == title:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Song with title {title} is already in iTunes!',
                'status': '404'
            })

    m = iTunes(db.getNewId(), title, artist, album, datetime.datetime.now())
    print('new song: ', m.serialize())
    db.insert(m)
    new_mus = [m.serialize() for m in db.view()]
    print('songs in lib: ', new_mus)

    return jsonify({
        # 'error': '',
        'res': m.serialize(),
        'status': '200',
        'msg': 'Success creating a new song!👍😀'
    })


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    mus = [m.serialize() for m in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for m in mus:
            if m['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': m,
                    'status': '200',
                    'msg': 'Success getting all songs in iTunes!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': mus,
            'status': '200',
            'msg': 'Success getting all songs in iTunes!👍😀',
            'no_of_songs': len(mus)
        })


@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    mus = [m.serialize() for m in db.view()]
    if req_args:
        for m in mus:
            if m['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': m,
                    'status': '200',
                    'msg': 'Success getting song by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Song with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            # 'error': '',
            'res': mus,
            'status': '200',
            'msg': 'Success getting song by ID!👍😀',
            'no_of_songs': len(mus)
        })


@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    title = req_data['title']
    artist = req_data['artist']
    album = req_data['album']
    the_id = req_data['id']
    mus = [m.serialize() for m in db.view()]
    for m in mus:
        if m['id'] == the_id:
            m = iTunes(
                the_id, title, artist, album, datetime.datetime.now()
            )
            print('new song: ', m.serialize())
            db.update(m)
            new_mus = [m.serialize() for m in db.view()]
            print('songs in lib: ', new_mus)
            return jsonify({
                # 'error': '',
                'res': m.serialize(),
                'status': '200',
                'msg': f'Success updating the song titled {title}!👍😀'
            })
    return jsonify({
        # 'error': '',
        'res': f'Error ⛔❌! Failed to update Song with title: {title}!',
        'status': '404'
    })


@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    mus = [m.serialize() for m in db.view()]
    if req_args:
        for m in mus:
            if m['id'] == int(req_args['id']):
                db.delete(m['id'])
                updated_mus = [m.serialize() for m in db.view()]
                print('updated_bks: ', updated_mus)
                return jsonify({
                    'res': updated_mus,
                    'status': '200',
                    'msg': 'Success deleting book by ID!👍😀',
                    'no_of_books': len(updated_mus)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No Book ID sent!",
            'res': '',
            'status': '404'
        })


if __name__ == '__main__':
    app.run()
