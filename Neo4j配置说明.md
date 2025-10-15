# 🔧 Neo4j数据库配置说明

## 📋 当前配置

**已修改的配置：**
- **连接地址**：`bolt://127.0.0.1:7687`
- **用户名**：`neo4j`
- **密码**：`password`

## 🚀 启动Neo4j数据库

### 方法一：使用Docker（推荐）
```bash
# 1. 安装Docker Desktop
# 访问：https://www.docker.com/products/docker-desktop/

# 2. 运行Neo4j容器
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.15.0
```

### 方法二：手动安装
1. **完成JDK安装**（已下载安装包）
2. **下载Neo4j**：https://neo4j.com/download/
3. **解压并启动**：
   ```bash
   cd neo4j-community-5.15.0
   ./bin/neo4j start
   ```

## 🔧 修改数据库密码

### 1. 访问Neo4j浏览器
- 打开浏览器：http://localhost:7474
- 首次登录：用户名 `neo4j`，密码 `neo4j`

### 2. 修改密码
1. 登录后，系统会要求修改默认密码
2. 设置新密码为：`password`
3. 或者修改代码中的密码

### 3. 修改代码中的密码
如果您的Neo4j密码不是 `password`，请修改以下文件：

**文件：`answer_search.py`**
```python
self.g = Graph(
    "bolt://127.0.0.1:7687",
    auth=("neo4j", "您的密码"))  # 修改这里
```

**文件：`build_medicalgraph.py`**
```python
self.g = Graph(
    "bolt://127.0.0.1:7687",
    auth=("neo4j", "您的密码"))  # 修改这里
```

## 🔍 验证连接

### 1. 检查Neo4j是否运行
```bash
# 检查端口
lsof -i :7687
lsof -i :7474
```

### 2. 测试连接
```bash
python3 -c "
from py2neo import Graph
g = Graph('bolt://127.0.0.1:7687', auth=('neo4j', 'password'))
print('✅ Neo4j连接成功！')
"
```

### 3. 运行知识图谱构建
```bash
python3 build_medicalgraph.py
```

## ⚠️ 常见问题

### 1. 连接失败
```
❌ Neo4j数据库连接失败: Connection refused
```
**解决方案**：
- 确保Neo4j已启动
- 检查端口7687是否被占用
- 验证用户名和密码

### 2. 认证失败
```
❌ Neo4j数据库连接失败: Authentication failed
```
**解决方案**：
- 检查用户名和密码
- 确认Neo4j已正确配置认证

### 3. 端口冲突
```
❌ Port 7687 is already in use
```
**解决方案**：
- 停止其他Neo4j实例
- 或修改Neo4j配置使用其他端口

## 📊 构建完成后

构建完成后，您将拥有：
- **疾病节点**：8,807个
- **症状节点**：5,998个
- **关系总数**：300,000+个

## 🎯 下一步

1. **启动Neo4j数据库**
2. **运行知识图谱构建**：`python3 build_medicalgraph.py`
3. **使用Web界面**：http://localhost:8080
4. **在Neo4j浏览器中查看**：http://localhost:7474
