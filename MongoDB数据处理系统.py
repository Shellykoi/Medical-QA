#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MongoDB数据处理系统
实现MongoDB数据处理，输出JSON数据
"""

import pymongo
from pymongo import MongoClient
import json
import os
from datetime import datetime

class MongoDBDataProcessor:
    def __init__(self):
        """初始化MongoDB连接"""
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['medical']
            print("✅ MongoDB连接成功")
        except Exception as e:
            print(f"❌ MongoDB连接失败: {e}")
            self.client = None
            self.db = None
    
    def check_mongodb_data(self):
        """检查MongoDB中的数据"""
        if self.db is None:
            print("❌ MongoDB未连接")
            return None
        
        try:
            # 获取所有集合
            collections = self.db.list_collection_names()
            print(f"📊 MongoDB集合: {collections}")
            
            data_summary = {}
            
            for collection_name in collections:
                collection = self.db[collection_name]
                count = collection.count_documents({})
                print(f"📋 {collection_name}: {count} 条记录")
                
                # 获取示例数据
                sample = collection.find_one()
                if sample:
                    data_summary[collection_name] = {
                        'count': count,
                        'sample_keys': list(sample.keys())[:5]  # 前5个字段
                    }
            
            return data_summary
            
        except Exception as e:
            print(f"❌ 检查数据失败: {e}")
            return None
    
    def export_to_json(self, output_dir="json_output"):
        """导出MongoDB数据到JSON文件"""
        if self.db is None:
            print("❌ MongoDB未连接")
            return False
        
        try:
            # 创建输出目录
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            print("📤 开始导出MongoDB数据到JSON...")
            
            # 获取所有集合
            collections = self.db.list_collection_names()
            export_results = {}
            
            for collection_name in collections:
                print(f"📋 处理集合: {collection_name}")
                collection = self.db[collection_name]
                
                # 获取所有数据
                data = list(collection.find({}, {'_id': 0}))
                
                # 保存到JSON文件
                output_file = os.path.join(output_dir, f"{collection_name}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                export_results[collection_name] = {
                    'file_path': output_file,
                    'record_count': len(data),
                    'file_size': os.path.getsize(output_file)
                }
                
                print(f"✅ {collection_name}: {len(data)} 条记录 -> {output_file}")
            
            # 创建汇总文件
            summary = {
                'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'collections': export_results,
                'total_collections': len(collections),
                'total_records': sum(r['record_count'] for r in export_results.values())
            }
            
            summary_file = os.path.join(output_dir, "export_summary.json")
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            print(f"📊 导出汇总: {summary_file}")
            print(f"🎉 导出完成: {len(collections)} 个集合, {summary['total_records']} 条记录")
            
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
    
    def create_web_viewer(self, output_dir="json_output"):
        """创建Web查看器"""
        html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MongoDB数据查看器</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .content {
            padding: 30px;
        }
        .collection-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #667eea;
        }
        .collection-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 10px;
        }
        .collection-info {
            color: #666;
            margin-bottom: 15px;
        }
        .view-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s;
        }
        .view-button:hover {
            background: #5a6fd8;
        }
        .data-viewer {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            max-height: 400px;
            overflow-y: auto;
        }
        .json-data {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗄️ MongoDB数据查看器</h1>
            <p>医疗知识图谱数据展示</p>
        </div>
        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="totalCollections">-</div>
                    <div class="stat-label">数据集合</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalRecords">-</div>
                    <div class="stat-label">总记录数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="exportTime">-</div>
                    <div class="stat-label">导出时间</div>
                </div>
            </div>
            
            <div id="collectionsList">
                <!-- 集合列表将在这里动态生成 -->
            </div>
        </div>
    </div>

    <script>
        // 加载数据
        async function loadData() {
            try {
                // 加载汇总信息
                const summaryResponse = await fetch('export_summary.json');
                const summary = await summaryResponse.json();
                
                // 更新统计信息
                document.getElementById('totalCollections').textContent = summary.total_collections;
                document.getElementById('totalRecords').textContent = summary.total_records;
                document.getElementById('exportTime').textContent = new Date(summary.export_time).toLocaleString();
                
                // 生成集合列表
                const collectionsList = document.getElementById('collectionsList');
                for (const [collectionName, info] of Object.entries(summary.collections)) {
                    const collectionCard = document.createElement('div');
                    collectionCard.className = 'collection-card';
                    collectionCard.innerHTML = `
                        <div class="collection-title">📊 ${collectionName}</div>
                        <div class="collection-info">
                            记录数: ${info.record_count} | 
                            文件大小: ${(info.file_size / 1024).toFixed(2)} KB
                        </div>
                        <button class="view-button" onclick="viewCollection('${collectionName}')">
                            查看数据
                        </button>
                    `;
                    collectionsList.appendChild(collectionCard);
                }
                
            } catch (error) {
                console.error('加载数据失败:', error);
                document.getElementById('collectionsList').innerHTML = 
                    '<div class="collection-card">❌ 无法加载数据，请确保JSON文件存在</div>';
            }
        }
        
        // 查看集合数据
        async function viewCollection(collectionName) {
            try {
                const response = await fetch(`${collectionName}.json`);
                const data = await response.json();
                
                // 创建数据查看器
                const viewer = document.createElement('div');
                viewer.className = 'data-viewer';
                viewer.innerHTML = `
                    <h3>📋 ${collectionName} 数据 (前10条)</h3>
                    <div class="json-data">${JSON.stringify(data.slice(0, 10), null, 2)}</div>
                    <button class="view-button" onclick="this.parentElement.remove()">关闭</button>
                `;
                
                document.getElementById('collectionsList').appendChild(viewer);
                
            } catch (error) {
                console.error('查看数据失败:', error);
                alert('无法加载数据文件');
            }
        }
        
        // 页面加载完成后执行
        document.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>
        """
        
        html_file = os.path.join(output_dir, "index.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Web查看器已创建: {html_file}")
        return html_file
    
    def run_processing(self):
        """运行数据处理"""
        print("🚀 开始MongoDB数据处理")
        print("=" * 50)
        
        # 1. 检查MongoDB数据
        print("📊 检查MongoDB数据...")
        data_summary = self.check_mongodb_data()
        
        if not data_summary:
            print("❌ 无法访问MongoDB数据")
            return False
        
        # 2. 导出到JSON
        print("\n📤 导出数据到JSON...")
        success = self.export_to_json()
        
        if not success:
            print("❌ 导出失败")
            return False
        
        # 3. 创建Web查看器
        print("\n🌐 创建Web查看器...")
        html_file = self.create_web_viewer()
        
        print(f"\n🎉 处理完成！")
        print(f"📁 JSON文件位置: json_output/")
        print(f"🌐 Web查看器: {html_file}")
        print(f"💡 在浏览器中打开: file://{os.path.abspath(html_file)}")
        
        return True

def main():
    """主函数"""
    processor = MongoDBDataProcessor()
    processor.run_processing()

if __name__ == "__main__":
    main()
