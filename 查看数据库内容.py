#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看Neo4j数据库和MongoDB数据库的具体内容
"""

from py2neo import Graph
import json
import pymongo
from pymongo import MongoClient

def view_neo4j_data():
    """查看Neo4j数据库内容"""
    print("🔍 查看Neo4j数据库内容")
    print("=" * 50)
    
    try:
        # 连接Neo4j
        g = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password"))
        
        # 1. 查看节点统计
        print("📊 节点统计：")
        node_types = ['Disease', 'Symptom', 'Drug', 'Food', 'Check', 'Department', 'Producer']
        for node_type in node_types:
            result = g.run(f"MATCH (n:{node_type}) RETURN count(n) as count")
            count = result.data()[0]['count']
            print(f"  {node_type}: {count} 个")
        
        # 2. 查看关系统计
        print("\n📊 关系统计：")
        result = g.run("MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count ORDER BY count DESC LIMIT 10")
        for record in result:
            print(f"  {record['rel_type']}: {record['count']} 个")
        
        # 3. 查看具体疾病数据
        print("\n🏥 疾病数据示例：")
        result = g.run("MATCH (d:Disease) RETURN d.name, d.desc LIMIT 5")
        for record in result:
            name = record['d.name']
            desc = record['d.desc'][:100] + "..." if len(record['d.desc']) > 100 else record['d.desc']
            print(f"  {name}: {desc}")
        
        # 4. 查看疾病-症状关系
        print("\n🔗 疾病-症状关系示例：")
        result = g.run("MATCH (d:Disease)-[r:has_symptom]->(s:Symptom) RETURN d.name, s.name LIMIT 5")
        for record in result:
            print(f"  {record['d.name']} -> {record['s.name']}")
        
        # 5. 查看疾病-药品关系
        print("\n💊 疾病-药品关系示例：")
        result = g.run("MATCH (d:Disease)-[r:common_drug]->(drug:Drug) RETURN d.name, drug.name LIMIT 5")
        for record in result:
            print(f"  {record['d.name']} -> {record['drug.name']}")
            
    except Exception as e:
        print(f"❌ Neo4j连接失败: {e}")

def view_mongodb_data():
    """查看MongoDB数据库内容"""
    print("\n🔍 查看MongoDB数据库内容")
    print("=" * 50)
    
    try:
        # 连接MongoDB
        client = MongoClient('localhost', 27017)
        db = client['medical_qa']
        
        # 查看所有集合
        collections = db.list_collection_names()
        print(f"📊 MongoDB集合: {collections}")
        
        # 查看疾病数据
        if 'diseases' in collections:
            diseases_collection = db['diseases']
            count = diseases_collection.count_documents({})
            print(f"\n🏥 疾病数据: {count} 条")
            
            # 查看示例数据
            sample = diseases_collection.find_one()
            if sample:
                print("📋 示例数据:")
                for key, value in sample.items():
                    if key != '_id':
                        print(f"  {key}: {str(value)[:100]}...")
        
        # 查看症状数据
        if 'symptoms' in collections:
            symptoms_collection = db['symptoms']
            count = symptoms_collection.count_documents({})
            print(f"\n🩺 症状数据: {count} 条")
        
        # 查看并发症数据
        if 'complications' in collections:
            complications_collection = db['complications']
            count = complications_collection.count_documents({})
            print(f"\n⚠️ 并发症数据: {count} 条")
            
            # 查看示例并发症数据
            sample = complications_collection.find_one()
            if sample:
                print("📋 并发症示例:")
                for key, value in sample.items():
                    if key != '_id':
                        print(f"  {key}: {str(value)[:100]}...")
        
    except Exception as e:
        print(f"❌ MongoDB连接失败: {e}")
        print("请确保MongoDB已启动")

def view_json_data():
    """查看JSON数据文件"""
    print("\n🔍 查看JSON数据文件")
    print("=" * 50)
    
    try:
        with open('data/medical.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 JSON数据统计:")
        print(f"  总疾病数: {len(data)}")
        
        # 查看第一个疾病的数据结构
        if data:
            first_disease = data[0]
            print(f"\n📋 疾病数据结构示例:")
            for key, value in first_disease.items():
                if isinstance(value, list):
                    print(f"  {key}: {len(value)} 项")
                else:
                    print(f"  {key}: {str(value)[:100]}...")
        
    except Exception as e:
        print(f"❌ JSON文件读取失败: {e}")

def main():
    """主函数"""
    print("🚀 医疗知识图谱数据库内容查看")
    print("=" * 60)
    
    # 查看Neo4j数据
    view_neo4j_data()
    
    # 查看MongoDB数据
    view_mongodb_data()
    
    # 查看JSON数据
    view_json_data()
    
    print("\n✅ 数据库内容查看完成！")

if __name__ == "__main__":
    main()
