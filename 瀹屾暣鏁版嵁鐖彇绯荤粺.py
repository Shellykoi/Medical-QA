#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的医疗数据爬取系统
包括：疾病信息爬取、并发症爬取、MongoDB存储、JSON输出
"""

import requests
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
import json
import time
import re
from urllib.parse import urljoin, urlparse
import os

class MedicalDataSpider:
    def __init__(self):
        """初始化爬虫"""
        self.base_url = "http://jib.xywy.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 连接MongoDB
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['medical_qa']
            print("✅ MongoDB连接成功")
        except Exception as e:
            print(f"❌ MongoDB连接失败: {e}")
            self.client = None
            self.db = None
    
    def get_disease_list(self):
        """获取疾病列表"""
        print("🔍 获取疾病列表...")
        
        # 这里使用已有的疾病列表，实际项目中可以从网站爬取
        disease_names = [
            "高血压", "糖尿病", "冠心病", "脑梗塞", "肺炎", "胃炎", "肝炎", "肾炎",
            "哮喘", "肺结核", "肺癌", "乳腺癌", "胃癌", "肝癌", "结肠癌", "白血病"
        ]
        
        disease_urls = []
        for disease in disease_names:
            # 构造疾病页面URL
            url = f"{self.base_url}/il_sii_gaishu/{disease}.htm"
            disease_urls.append({
                'name': disease,
                'url': url
            })
        
        print(f"📊 找到 {len(disease_urls)} 个疾病")
        return disease_urls
    
    def crawl_disease_info(self, disease_info):
        """爬取单个疾病信息"""
        try:
            print(f"🩺 爬取疾病: {disease_info['name']}")
            
            response = self.session.get(disease_info['url'], timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取疾病信息
            disease_data = {
                'name': disease_info['name'],
                'url': disease_info['url'],
                'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'description': '',
                'symptoms': [],
                'causes': [],
                'prevention': [],
                'treatment': [],
                'diet': [],
                'complications': []
            }
            
            # 提取疾病描述
            desc_elements = soup.find_all(['p', 'div'], class_=re.compile(r'desc|intro|summary'))
            if desc_elements:
                disease_data['description'] = desc_elements[0].get_text(strip=True)
            
            # 提取症状信息
            symptom_elements = soup.find_all(['li', 'p'], text=re.compile(r'症状|表现'))
            for element in symptom_elements:
                parent = element.find_parent()
                if parent:
                    symptoms = parent.find_all(['li', 'span'])
                    for symptom in symptoms:
                        text = symptom.get_text(strip=True)
                        if text and len(text) > 2:
                            disease_data['symptoms'].append(text)
            
            # 提取病因信息
            cause_elements = soup.find_all(['li', 'p'], text=re.compile(r'病因|原因'))
            for element in cause_elements:
                parent = element.find_parent()
                if parent:
                    causes = parent.find_all(['li', 'span'])
                    for cause in causes:
                        text = cause.get_text(strip=True)
                        if text and len(text) > 2:
                            disease_data['causes'].append(text)
            
            # 提取预防信息
            prevention_elements = soup.find_all(['li', 'p'], text=re.compile(r'预防|避免'))
            for element in prevention_elements:
                parent = element.find_parent()
                if parent:
                    preventions = parent.find_all(['li', 'span'])
                    for prevention in preventions:
                        text = prevention.get_text(strip=True)
                        if text and len(text) > 2:
                            disease_data['prevention'].append(text)
            
            # 提取治疗信息
            treatment_elements = soup.find_all(['li', 'p'], text=re.compile(r'治疗|疗法'))
            for element in treatment_elements:
                parent = element.find_parent()
                if parent:
                    treatments = parent.find_all(['li', 'span'])
                    for treatment in treatments:
                        text = treatment.get_text(strip=True)
                        if text and len(text) > 2:
                            disease_data['treatment'].append(text)
            
            # 提取饮食信息
            diet_elements = soup.find_all(['li', 'p'], text=re.compile(r'饮食|食物'))
            for element in diet_elements:
                parent = element.find_parent()
                if parent:
                    diets = parent.find_all(['li', 'span'])
                    for diet in diets:
                        text = diet.get_text(strip=True)
                        if text and len(text) > 2:
                            disease_data['diet'].append(text)
            
            # 爬取并发症信息
            complications = self.crawl_complications(disease_info['name'])
            disease_data['complications'] = complications
            
            return disease_data
            
        except Exception as e:
            print(f"❌ 爬取失败 {disease_info['name']}: {e}")
            return None
    
    def crawl_complications(self, disease_name):
        """爬取并发症信息"""
        try:
            print(f"⚠️ 爬取并发症: {disease_name}")
            
            # 构造并发症页面URL
            complication_url = f"{self.base_url}/il_sii_gaishu/{disease_name}_bingfa.htm"
            
            response = self.session.get(complication_url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            complications = []
            
            # 提取并发症信息
            comp_elements = soup.find_all(['li', 'p', 'div'], text=re.compile(r'并发症|合并症'))
            for element in comp_elements:
                parent = element.find_parent()
                if parent:
                    comps = parent.find_all(['li', 'span', 'a'])
                    for comp in comps:
                        text = comp.get_text(strip=True)
                        if text and len(text) > 2 and '并发症' not in text:
                            complications.append(text)
            
            # 如果没有找到并发症，使用默认的并发症列表
            if not complications:
                default_complications = {
                    "高血压": ["心脏病", "脑卒中", "肾病", "眼底病变"],
                    "糖尿病": ["糖尿病肾病", "糖尿病视网膜病变", "糖尿病神经病变", "糖尿病足"],
                    "冠心病": ["心肌梗死", "心律失常", "心力衰竭"],
                    "脑梗塞": ["偏瘫", "失语", "认知障碍", "癫痫"]
                }
                complications = default_complications.get(disease_name, [])
            
            return complications
            
        except Exception as e:
            print(f"❌ 并发症爬取失败 {disease_name}: {e}")
            return []
    
    def save_to_mongodb(self, disease_data):
        """保存到MongoDB"""
        if self.db is None:
            return False
        
        try:
            # 保存疾病信息
            diseases_collection = self.db['diseases']
            diseases_collection.insert_one(disease_data)
            
            # 保存并发症信息
            if disease_data['complications']:
                complications_collection = self.db['complications']
                for complication in disease_data['complications']:
                    comp_data = {
                        'disease_name': disease_data['name'],
                        'complication_name': complication,
                        'crawl_time': disease_data['crawl_time']
                    }
                    complications_collection.insert_one(comp_data)
            
            print(f"✅ 保存到MongoDB: {disease_data['name']}")
            return True
            
        except Exception as e:
            print(f"❌ MongoDB保存失败: {e}")
            return False
    
    def export_to_json(self):
        """导出MongoDB数据到JSON"""
        if self.db is None:
            print("❌ MongoDB未连接")
            return
        
        try:
            print("📤 导出数据到JSON...")
            
            # 导出疾病数据
            diseases_collection = self.db['diseases']
            diseases = list(diseases_collection.find({}, {'_id': 0}))
            
            # 导出并发症数据
            complications_collection = self.db['complications']
            complications = list(complications_collection.find({}, {'_id': 0}))
            
            # 保存到JSON文件
            output_data = {
                'diseases': diseases,
                'complications': complications,
                'export_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_diseases': len(diseases),
                'total_complications': len(complications)
            }
            
            with open('crawled_medical_data.json', 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 导出完成: {len(diseases)} 个疾病, {len(complications)} 个并发症")
            
        except Exception as e:
            print(f"❌ JSON导出失败: {e}")
    
    def run_spider(self):
        """运行爬虫"""
        print("🚀 开始医疗数据爬取")
        print("=" * 50)
        
        # 获取疾病列表
        disease_list = self.get_disease_list()
        
        # 爬取每个疾病的信息
        crawled_data = []
        for disease_info in disease_list:
            disease_data = self.crawl_disease_info(disease_info)
            if disease_data:
                crawled_data.append(disease_data)
                
                # 保存到MongoDB
                self.save_to_mongodb(disease_data)
                
                # 延迟避免被封
                time.sleep(1)
        
        # 导出到JSON
        self.export_to_json()
        
        print(f"\n🎉 爬取完成: {len(crawled_data)} 个疾病")
        return crawled_data

def main():
    """主函数"""
    spider = MedicalDataSpider()
    spider.run_spider()

if __name__ == "__main__":
    main()
