# 🚀 简化Neo4j安装方案

## 📋 当前状态
- ✅ Web服务器已运行：http://localhost:8080
- ❌ Neo4j数据库未安装
- ❌ 知识图谱构建需要Neo4j

## 🎯 立即可用的功能

**您现在就可以使用：**
1. **Web界面**：http://localhost:8080
2. **智能问答**：基于JSON数据的问答系统
3. **数据统计**：显示数据规模

## 🔧 Neo4j安装选项

### 选项一：使用Docker（推荐）
```bash
# 安装Docker Desktop
# 访问：https://www.docker.com/products/docker-desktop/

# 运行Neo4j容器
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.15.0
```

### 选项二：手动安装
1. **安装Java**：
   - 访问：https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
   - 下载并安装JDK 8或11

2. **下载Neo4j**：
   - 访问：https://neo4j.com/download/
   - 下载Neo4j Community Edition
   - 解压到本地目录

3. **启动Neo4j**：
   ```bash
   cd neo4j-community-5.15.0
   ./bin/neo4j start
   ```

### 选项三：使用Homebrew
```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Neo4j
brew install neo4j

# 启动Neo4j
brew services start neo4j
```

## 🎯 当前项目功能

### ✅ 已完成
1. **Web界面**：美观的问答界面
2. **数据爬取**：MongoDB存储
3. **JSON数据处理**：智能问答
4. **并发症爬取**：完整实现

### ⚠️ 需要Neo4j的功能
1. **知识图谱构建**：需要1-2小时
2. **基于Neo4j的问答**：需要Neo4j运行

## 💡 建议

**立即可用：**
- 访问 http://localhost:8080 使用Web界面
- 基于JSON数据的智能问答
- 美观的界面和功能

**如需完整知识图谱：**
- 选择上述任一Neo4j安装方案
- 运行知识图谱构建（需要1-2小时）

## 🔍 验证安装

安装Neo4j后，访问：
- **Neo4j浏览器**：http://localhost:7474
- **用户名**：neo4j
- **密码**：password

然后运行：
```bash
python3 build_medicalgraph.py
```
