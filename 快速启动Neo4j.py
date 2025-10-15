#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动Neo4j数据库
使用Docker方式，无需复杂安装
"""

import subprocess
import time
import requests
import json

def check_docker():
    """检查Docker是否安装"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker已安装")
            return True
        else:
            print("❌ Docker未安装")
            return False
    except FileNotFoundError:
        print("❌ Docker未安装")
        return False

def install_docker():
    """安装Docker Desktop"""
    print("📥 请手动安装Docker Desktop：")
    print("1. 访问：https://www.docker.com/products/docker-desktop/")
    print("2. 下载Docker Desktop for Mac")
    print("3. 安装并启动Docker Desktop")
    print("4. 然后重新运行此脚本")
    return False

def start_neo4j():
    """启动Neo4j容器"""
    print("🚀 启动Neo4j容器...")
    
    # 检查是否已有Neo4j容器
    try:
        result = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=neo4j'], 
                             capture_output=True, text=True)
        if 'neo4j' in result.stdout:
            print("📋 发现已存在的Neo4j容器")
            # 启动现有容器
            subprocess.run(['docker', 'start', 'neo4j'])
            print("✅ Neo4j容器已启动")
        else:
            print("📦 创建新的Neo4j容器...")
            # 创建新容器
            cmd = [
                'docker', 'run', '-d',
                '--name', 'neo4j',
                '-p', '7474:7474',
                '-p', '7687:7687',
                '-e', 'NEO4J_AUTH=neo4j/password',
                'neo4j:5.15.0'
            ]
            subprocess.run(cmd)
            print("✅ Neo4j容器已创建并启动")
    except Exception as e:
        print(f"❌ 启动Neo4j失败: {e}")
        return False
    
    return True

def check_neo4j():
    """检查Neo4j是否运行"""
    print("🔍 检查Neo4j状态...")
    
    # 等待Neo4j启动
    for i in range(30):
        try:
            response = requests.get('http://localhost:7474', timeout=5)
            if response.status_code == 200:
                print("✅ Neo4j已启动并运行")
                print("🌐 访问地址：http://localhost:7474")
                print("👤 用户名：neo4j")
                print("🔑 密码：password")
                return True
        except:
            pass
        
        print(f"⏳ 等待Neo4j启动... ({i+1}/30)")
        time.sleep(2)
    
    print("❌ Neo4j启动超时")
    return False

def main():
    """主函数"""
    print("🚀 快速启动Neo4j数据库")
    print("=" * 50)
    
    # 检查Docker
    if not check_docker():
        if not install_docker():
            return
    
    # 启动Neo4j
    if start_neo4j():
        if check_neo4j():
            print("\n🎉 Neo4j启动成功！")
            print("📋 下一步：")
            print("1. 访问 http://localhost:7474")
            print("2. 用户名：neo4j，密码：password")
            print("3. 运行：python3 build_medicalgraph.py")
        else:
            print("\n❌ Neo4j启动失败")
    else:
        print("\n❌ 无法启动Neo4j")

if __name__ == "__main__":
    main()

