#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Neo4j连接和知识图谱状态
"""

from py2neo import Graph

def test_connection():
    """测试Neo4j连接"""
    print("🔍 测试Neo4j连接...")
    
    # 尝试不同的用户名和密码组合
    credentials = [
        ("neo4j", "neo4j"),
        ("neo4j", "password"),
        ("Shellykoi", "12345678"),
        ("neo4j", "12345678")
    ]
    
    for username, password in credentials:
        try:
            print(f"尝试连接: {username}/{password}")
            g = Graph("bolt://127.0.0.1:7687", auth=(username, password))
            
            # 测试查询
            result = g.run("MATCH (n) RETURN count(n) as total_nodes LIMIT 1")
            total_nodes = result.data()[0]['total_nodes']
            
            print(f"✅ 连接成功！用户名: {username}, 密码: {password}")
            print(f"📊 数据库中的节点数量: {total_nodes}")
            
            if total_nodes > 0:
                print("🎉 知识图谱已构建完成！")
                return True, username, password, total_nodes
            else:
                print("⚠️ 数据库为空，需要构建知识图谱")
                return True, username, password, 0
                
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            continue
    
    print("❌ 所有连接尝试都失败了")
    return False, None, None, 0

def main():
    """主函数"""
    print("🚀 Neo4j连接测试")
    print("=" * 50)
    
    success, username, password, total_nodes = test_connection()
    
    if success:
        print(f"\n✅ 连接成功！")
        print(f"用户名: {username}")
        print(f"密码: {password}")
        print(f"节点数量: {total_nodes}")
        
        if total_nodes > 0:
            print("\n🎉 知识图谱已构建完成！")
            print("现在可以正常使用Web界面了。")
        else:
            print("\n⚠️ 需要构建知识图谱：")
            print("python3 build_medicalgraph.py")
    else:
        print("\n❌ 无法连接到Neo4j")
        print("请检查：")
        print("1. Neo4j是否正在运行")
        print("2. 用户名和密码是否正确")
        print("3. 端口7687是否可访问")

if __name__ == "__main__":
    main()

