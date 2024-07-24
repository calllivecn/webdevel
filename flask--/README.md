# uvicorn + flask 

- 需要安装 asgiref

- 在代码中使用

```python
from asgiref.wsgi import WsgiToAsgi

app = Flask("appname")
...

asgi_app = WsgiToAsgi(app)
```

