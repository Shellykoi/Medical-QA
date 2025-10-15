#!/bin/bash

echo "🚀 开始安装Neo4j数据库..."

# 检查Java环境
echo "📋 检查Java环境..."
if ! command -v java &> /dev/null; then
    echo "❌ 未找到Java环境，请先安装Java"
    echo "请访问：https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html"
    echo "或安装OpenJDK："
    echo "brew install openjdk@11"
    exit 1
else
    echo "✅ Java环境已安装"
    java -version
fi

# 检查Java运行时
echo "🔍 检查Java运行时..."
if ! java -version 2>&1 | grep -q "version"; then
    echo "❌ Java运行时不可用，请检查Java安装"
    echo "尝试设置JAVA_HOME环境变量"
    export JAVA_HOME=$(/usr/libexec/java_home 2>/dev/null || echo "")
    if [ -z "$JAVA_HOME" ]; then
        echo "请手动安装Java："
        echo "1. 访问 https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html"
        echo "2. 下载并安装JDK 8或11"
        exit 1
    fi
fi

# 创建Neo4j目录
NEO4J_DIR="$HOME/neo4j"
mkdir -p "$NEO4J_DIR"
cd "$NEO4J_DIR"

echo "📥 下载Neo4j Community Edition..."
# 下载Neo4j（使用更稳定的下载链接）
NEO4J_VERSION="5.15.0"
NEO4J_URL="https://dist.neo4j.org/neo4j-community-${NEO4J_VERSION}-unix.tar.gz"

if [ ! -f "neo4j-community-${NEO4J_VERSION}.tar.gz" ]; then
    echo "正在下载Neo4j ${NEO4J_VERSION}..."
    echo "下载地址：$NEO4J_URL"
    
    # 尝试多种下载方式
    if curl -L -o "neo4j-community-${NEO4J_VERSION}.tar.gz" "$NEO4J_URL"; then
        echo "✅ 下载成功"
    else
        echo "❌ 自动下载失败，请手动下载："
        echo "1. 访问：https://neo4j.com/download/"
        echo "2. 下载Neo4j Community Edition"
        echo "3. 将文件保存到：$NEO4J_DIR/neo4j-community-${NEO4J_VERSION}.tar.gz"
        echo "4. 然后重新运行此脚本"
        exit 1
    fi
else
    echo "✅ Neo4j安装包已存在"
fi

# 解压
if [ ! -d "neo4j-community-${NEO4J_VERSION}" ]; then
    echo "📦 解压Neo4j..."
    tar -xzf "neo4j-community-${NEO4J_VERSION}.tar.gz"
else
    echo "✅ Neo4j已解压"
fi

# 设置环境变量
echo "🔧 配置Neo4j..."
export NEO4J_HOME="$NEO4J_DIR/neo4j-community-${NEO4J_VERSION}"
export PATH="$NEO4J_HOME/bin:$PATH"

# 创建启动脚本
cat > "$NEO4J_DIR/start_neo4j.sh" << 'EOF'
#!/bin/bash
export NEO4J_HOME="$HOME/neo4j/neo4j-community-5.15.0"
export PATH="$NEO4J_HOME/bin:$PATH"
echo "🚀 启动Neo4j数据库..."
$NEO4J_HOME/bin/neo4j start
echo "✅ Neo4j已启动！"
echo "🌐 访问地址：http://localhost:7474"
echo "👤 默认用户名：neo4j"
echo "🔑 默认密码：neo4j（首次登录需要修改）"
EOF

chmod +x "$NEO4J_DIR/start_neo4j.sh"

# 创建停止脚本
cat > "$NEO4J_DIR/stop_neo4j.sh" << 'EOF'
#!/bin/bash
export NEO4J_HOME="$HOME/neo4j/neo4j-community-5.15.0"
export PATH="$NEO4J_HOME/bin:$PATH"
echo "🛑 停止Neo4j数据库..."
$NEO4J_HOME/bin/neo4j stop
echo "✅ Neo4j已停止！"
EOF

chmod +x "$NEO4J_DIR/stop_neo4j.sh"

echo ""
echo "🎉 Neo4j安装完成！"
echo ""
echo "📋 使用方法："
echo "1. 启动Neo4j：$NEO4J_DIR/start_neo4j.sh"
echo "2. 停止Neo4j：$NEO4J_DIR/stop_neo4j.sh"
echo "3. 访问地址：http://localhost:7474"
echo ""
echo "🔧 首次使用："
echo "1. 运行启动脚本"
echo "2. 打开浏览器访问 http://localhost:7474"
echo "3. 用户名：neo4j，密码：neo4j"
echo "4. 修改默认密码为：password"
echo ""
echo "⚠️  注意：请确保Java环境已正确安装！"
