
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import datetime

# 1. 定义数据模型
class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # 自动验证邮箱格式
    signup_ts: datetime | None = None # 允许为空，若传入字符串会自动转为 datetime

# 2. 模拟原始数据 (通常来自 JSON)
raw_data = {
    "id": "123",          # 字符串，但模型需要 int，Pydantic 会尝试转换
    "name": "Alice",
    "email": "alice@example.com",
    "signup_ts": "2023-10-01T12:00:00" # 字符串，会自动转为 datetime 对象
}

try:
    # 3. 验证并创建实例
    user = User(**raw_data)
    
    print(user)
    # 输出: id=123 name='Alice' email='alice@example.com' signup_ts=datetime.datetime(2023, 10, 1, 12, 0)
    
    print(user.email) # 访问属性
    # 输出: alice@example.com
    
    # 转换为字典 (序列化)
    print(user.model_dump()) 

except ValidationError as e:
    # 4. 处理验证错误
    print(e.errors())

