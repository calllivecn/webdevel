#!/usr/bin/env python3
# coding=utf-8
# date 2020-01-18 14:30:00
# author calllivecn <calllivecn@outlook.com>

########
#
# 都能使用了，只差加密部分了。
#
#######

import os
import re
import sys
import pprint
from os import path
from pathlib import Path
from urllib import parse

from datetime import (
    datetime,
    timedelta,
    )

from flask import (
    Flask,
    request,
    Response,
    session,
    render_template_string,
    redirect,
    #escape,
    url_for,
    jsonify,
    )

from werkzeug.utils import secure_filename
from werkzeug.routing import BaseConverter


ROOT = Path(".")
PW="videopassword"

app = Flask(__name__)

LOING="""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>why</title>
</head>
<body>
<form action="{{ url_for('why') }}" method="post">
    <input type="password" name="pw" required />
    <input type="submit" value="ok" />
</form>
</body>
</html>
"""

VIDEOS="""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>why</title>
</head>
<body>
    <a href="{{ url_for('upload') }}">上传文件</a>

    {% for v, s in videos %}
    <li>
      <a href="{{ url_for('video', filename=v) }}">play</a>
      <label> or </label>
      <a href="{{url_for('download', filename=v)}}">download</a>
      <label>{{ v }} -- {{ s }} </label>
    </li>
    {% endfor %}
</body>
</html>
"""

VIDEO="""
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>why</title>
</head>

<body>
    <video id="video1" controls="controls" autoplay="autoplay" preload="metadata">
        <source src="{{ url_for('play', filename=video) }}"
    </video>
</body>
    <script>
        v = document.getElementById("video1");
        //console.log("video time start: ", v.buffered.start(0));
        //console.log("video time end: ", v.buffered.end(0));

        var c = 0;
        v.addEventListener("progress", function(){
            c += 1;
            console.log("----------------------------------------------");
            console.log("video currenttime: ", v.currentTime, "total length: ", v.duration, "count:", c);
            //console.log("video time start: ", v.buffered.start(0), "end: ", v.buffered.end(0));
            console.log("played time Range:", v.played);
        })
    </script>
</html>
"""

UPLOAD="""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>上传文件</title>
</head>
<body>
    <h1>上传文件</h1>
    <form action="{{ url_for('upload') }}" method="POST" enctype="multipart/form-data">
        <input type="file" name="filename" />
        <input type="submit" value="上传" />
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return "server error", 500


def getsize(filename: Path):

    size = filename.stat().st_size
    
    if 0 <= size < 1024: # B 
        return "{}B".format(size)
    elif 1024 <= size <= 1048576: # KB
        return "{}KB".format(round(size / 1024, 2)) 
    elif 1048576 <= size < 1073741824: # MB
        return "{}MB".format(round(size / 1048576, 2)) 
    elif 1048576 <= size: # < 1099511627776: # GB
        return "{}GB".format(round(size / 1073741824, 2))


@app.route("/why/", methods=["GET", "POST"])
def why():

    if request.method == "GET":

        return render_template_string(LOING)

    elif request.method == "POST":

        if request.form["pw"] != PW:
            return ""

        session["key"] = request.form["pw"]

        return redirect(url_for("videos"));


@app.route("/i/")
def videos():

    if session["key"] != PW:
        return ""

    print("key:", session["key"])

    videos = os.listdir(ROOT)

    vs = []
    for v in videos:
        if v.endswith(".mkv") or v.endswith(".MKV") or v.endswith(".mp4") or v.endswith(".MP4") or v.endswith(".webm") or v.endswith(".WEBM") or v.endswith(".ogg") or v.endswith(".OGG"):
            size = getsize(ROOT / v)
            vs.append((v, size))

    return render_template_string(VIDEOS, videos=vs)


@app.route("/v/<filename>/")
def video(filename):

    if session["key"] != PW:
        return ""

    Range = request.headers.get("Range")

    #print("Client headers :")
    #print(pprint.pformat(request.headers))

    filesize = getsize(ROOT / filename)

    return render_template_string(VIDEO, video=filename)

range_bytes = re.compile("bytes=(\d+)-\d*")
@app.route("/p/<filename>/")
def play(filename):

    print("key:", session["key"])

    if session["key"] != PW:
        return ""

    Range = request.headers.get("Range", None)

    if Range is None:
        seek = 0
    else:
        match = range_bytes.search(Range)
        seek = int(match.group(1))

    filepath = ROOT / filename

    block = 1<<20 # 64k 块
    total = filepath.stat().st_size
    with open(filepath, "rb") as f:
        f.seek(seek, os.SEEK_SET)
        videoblock = f.read(block)

    end = seek + len(videoblock) - 1

    headers = {}
    headers["Accept-Ranges"] = "bytes"
    headers["Content-Length"] = block
    headers["Content-Range"] = f"bytes {seek}-{end}/{total}"

    return Response(videoblock, 206, headers=headers)

@app.route("/u/", methods=["GET", "POST"])
def upload():

    #if session["key"] != PW:
    #    return ""

    if request.method == "GET":

        return render_template_string(UPLOAD)

    elif request.method == "POST":

        f = request.files["filename"]

        #print("""request.files["filename"]: """, dir(f))
        #print("f.stream: ", dir(f.stream))
        #print("request.stream: ", dir(request.stream))

        filename = secure_filename(f.filename)

        filefullpath = ROOT / filename

        #f.save(filefullpath)

        chunksize = 1<<16 # 64k
        #size = 0
        with open(filefullpath, "wb") as fp:
            #for data in iter(partial(f.stream.read, chunksize), b""):
            while (data := f.stream.read(chunksize)) != b"":
                #size += len(data)
                #print(f"当前：{size}")
                fp.write(data)

        return jsonify({"recode": 0, "filename": filename})

def __send_chunk(filename):
    path = ROOT / filename
    with open(path, "rb") as f:
        while (data := f.read(4096)) != b"":
            yield data


@app.route("/d/<filename>/", methods=["GET"])
def download(filename):
    filepath = ROOT / filename
    filesize = filepath.stat().st_size
    res = Response(__send_chunk(filepath), content_type="application/octet-stream")
    res.headers.set("content-length", filesize)
    res.headers.set("Content-Disposition", f"attachment;filename={parse.quote(filename)}")
    return res

@app.route("/favicon.ico")
def ico():
    expired = datetime.now() + timedelta(3)
    headers = {}
    headers['Expires'] = expired
    res = Response("", 404, headers=headers)
    return res

class Any(BaseConverter):
    def __init__(self, url_map, regex):

        super().__init__(url_map)
        self.regex = regex

app.url_map.converters["re"] = Any

@app.route("/<re('.*'):any>")
def error(drop):
    return "server error", 500

if __name__ == "__main__":

    try:
        ROOT = Path(sys.argv[1])
    except Exception:
        pass

    prog = Path(sys.argv[0])
    dirname, filename = prog.parent, prog.name

    os.putenv("FLASK_APP", filename)
    os.putenv("FLASK_ENV", "development")

    app.config["DEBUG"] = True
    #app.config["SECRET_KEY"] = os.urandom(24)
    app.config["SECRET_KEY"] = b"secretkey"
    app.run(host="0.0.0.0", port=6789, debug=True)
