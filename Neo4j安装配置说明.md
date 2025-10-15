# Neo4j 安装和配置说明

## 📋 前置要求

### 1. 安装Java环境
```bash
# 检查Java版本
java -version

# 如果没有Java，安装OpenJDK 11
brew install openjdk@11

# 或者从Oracle官网下载JDK 8
# https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
```

### 2. 安装Neo4j

#### 方法一：使用Homebrew（推荐）
```bash
# 安装Neo4j
brew install neo4j

# 启动Neo4j服务
brew services start neo4j
```

#### 方法二：手动安装
1. 访问 [Neo4j官网](https://neo4j.com/download/)
2. 下载Neo4j Community Edition
3. 解压到本地目录
4. 启动Neo4j：
   ```bash
   cd neo4j-community-5.x.x
   ./bin/neo4j start
   ```

## 🔧 配置Neo4j

### 1. 启动Neo4j
```bash
# 使用Homebrew启动
brew services start neo4j

# 或手动启动
neo4j start
```

### 2. 访问Neo4j浏览器
- 打开浏览器访问：http://localhost:7474
- 默认用户名：`neo4j`
- 默认密码：`neo4j`（首次登录需要修改）

### 3. 修改默认密码
1. 首次登录时会要求修改密码
2. 建议设置密码为：`password`（与代码中一致）
3. 或者修改代码中的密码设置

## 🚀 运行知识图谱构建

### 1. 确保Neo4j正在运行
```bash
# 检查Neo4j状态
brew services list | grep neo4j

# 或检查端口
lsof -i :7687
```

### 2. 运行构建脚本
```bash
cd /Users/shellykoi/Downloads/QASystemOnMedicalKG-master
python3 build_medicalgraph.py
```

### 3. 构建过程
- **预计时间**：1-2小时
- **数据量**：8807个疾病，5998个症状，300K+个关系
- **进度显示**：脚本会显示构建进度

## 🔍 验证构建结果

### 1. 在Neo4j浏览器中查看
1. 访问 http://localhost:7474
2. 在查询框中输入：
   ```cypher
   MATCH (n) RETURN count(n) as total_nodes
   ```
3. 查看节点数量

### 2. 查看疾病节点
```cypher
MATCH (d:Disease) RETURN d.name LIMIT 10
```

### 3. 查看关系
```cypher
MATCH ()-[r]->() RETURN count(r) as total_relationships
```

## ⚠️ 常见问题

### 1. 连接失败
```
❌ Neo4j数据库连接失败: ServiceUnavailable
```
**解决方案**：
- 确保Neo4j正在运行
- 检查端口7687是否被占用
- 验证用户名和密码

### 2. 内存不足
```
OutOfMemoryError
```
**解决方案**：
- 增加Neo4j堆内存设置
- 编辑 `conf/neo4j.conf`
- 添加：`dbms.memory.heap.initial_size=2G`

### 3. 构建时间过长
**优化建议**：
- 分批处理数据
- 增加Neo4j内存配置
- 使用SSD硬盘

## 📊 构建完成后的数据统计

构建完成后，您将拥有：
- **疾病节点**：8,807个
- **症状节点**：5,998个
- **药品节点**：约2,000个
- **关系总数**：300,000+个

## 🎯 下一步

构建完成后，您可以：
1. 使用Web界面进行问答：http://localhost:8080
2. 在Neo4j浏览器中探索知识图谱
3. 运行基于Neo4j的问答系统

## 📞 技术支持

如果遇到问题，请检查：
1. Java版本（推荐JDK 8或11）
2. Neo4j版本（推荐5.x）
3. 系统内存（建议8GB+）
4. 磁盘空间（建议10GB+）
