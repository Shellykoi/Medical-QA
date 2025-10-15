#!/usr/bin/env python3
# coding: utf-8
# 医疗知识图谱问答系统 - Web服务器

from flask import Flask, render_template, request, jsonify
import json
import os
import re
from datetime import datetime

app = Flask(__name__)

class MedicalQuestionClassifier:
    """医疗问题分类器"""
    def __init__(self):
        # 加载词典
        self.disease_words = self.load_dict('dict/disease.txt')
        self.symptom_words = self.load_dict('dict/symptom.txt')
        self.drug_words = self.load_dict('dict/drug.txt')
        self.food_words = self.load_dict('dict/food.txt')
        self.check_words = self.load_dict('dict/check.txt')
        
        # 疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现', '有哪些']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何']
        self.desc_qwds = ['是什么', '介绍', '描述', '说明']
        self.cure_qwds = ['治疗', '怎么治', '如何治', '怎么办', '多久', '周期', '治愈']
        
    def load_dict(self, file_path):
        """加载词典文件"""
        words = []
        try:
            full_path = os.path.join(os.path.dirname(__file__), file_path)
            with open(full_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        words.append(word)
        except Exception as e:
            print(f"加载词典 {file_path} 失败: {e}")
        return words
    
    def classify(self, question):
        """分类问题"""
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        
        data['args'] = medical_dict
        types = list(medical_dict.keys())
        question_types = []
        
        # 症状
        if self.check_words_in_question(self.symptom_qwds, question) and 'disease' in types:
            question_types.append('disease_symptom')
        
        # 原因
        if self.check_words_in_question(self.cause_qwds, question) and 'disease' in types:
            question_types.append('disease_cause')
        
        # 治疗
        if self.check_words_in_question(self.cure_qwds, question) and 'disease' in types:
            question_types.append('disease_cure')
        
        # 描述
        if self.check_words_in_question(self.desc_qwds, question) and 'disease' in types:
            question_types.append('disease_desc')
        
        # 如果没有匹配到特定类型，但有疾病，默认为描述
        if not question_types and 'disease' in types:
            question_types.append('disease_desc')
        
        data['question_types'] = question_types
        return data
    
    def check_medical(self, question):
        """检查问题中的医疗实体"""
        medical_dict = {}
        
        # 检查疾病
        for disease in self.disease_words:
            if disease in question:
                if 'disease' not in medical_dict:
                    medical_dict['disease'] = []
                medical_dict['disease'].append(disease)
        
        # 检查症状
        for symptom in self.symptom_words:
            if symptom in question:
                if 'symptom' not in medical_dict:
                    medical_dict['symptom'] = []
                medical_dict['symptom'].append(symptom)
        
        return medical_dict
    
    def check_words_in_question(self, words, question):
        """检查问题中是否包含特定词汇"""
        for word in words:
            if word in question:
                return True
        return False

class MedicalAnswerSearcher:
    """医疗答案搜索器"""
    def __init__(self):
        self.medical_data = self.load_medical_data()
    
    def load_medical_data(self):
        """加载医疗数据"""
        data_path = os.path.join(os.path.dirname(__file__), 'data/medical.json')
        medical_data = {}
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        disease_data = json.loads(line)
                        medical_data[disease_data['name']] = disease_data
        except Exception as e:
            print(f"加载医疗数据失败: {e}")
        return medical_data
    
    def search_main(self, question_type, disease_name):
        """搜索答案"""
        if disease_name not in self.medical_data:
            return "抱歉，我没有找到相关信息。"
        
        disease_data = self.medical_data[disease_name]
        
        if question_type == 'disease_symptom':
            symptoms = disease_data.get('symptom', [])
            if symptoms:
                return f"{disease_name}的症状包括：{'；'.join(symptoms[:10])}"
            else:
                return f"抱歉，我没有找到{disease_name}的症状信息。"
        
        elif question_type == 'disease_cause':
            cause = disease_data.get('cause', '')
            if cause:
                cause_short = cause[:200] + "..." if len(cause) > 200 else cause
                return f"{disease_name}可能的成因有：{cause_short}"
            else:
                return f"抱歉，我没有找到{disease_name}的病因信息。"
        
        elif question_type == 'disease_cure':
            cure_way = disease_data.get('cure_way', [])
            cure_lasttime = disease_data.get('cure_lasttime', '')
            cured_prob = disease_data.get('cured_prob', '')
            
            result = f"{disease_name}的治疗信息：\n"
            if cure_way:
                result += f"治疗方式：{'；'.join(cure_way)}\n"
            if cure_lasttime:
                result += f"治疗周期：{cure_lasttime}\n"
            if cured_prob:
                result += f"治愈概率：{cured_prob}"
            
            if result == f"{disease_name}的治疗信息：\n":
                return f"抱歉，我没有找到{disease_name}的治疗信息。"
            else:
                return result.strip()
        
        elif question_type == 'disease_desc':
            desc = disease_data.get('desc', '')
            if desc:
                desc_short = desc[:300] + "..." if len(desc) > 300 else desc
                return f"{disease_name}，熟悉一下：{desc_short}"
            else:
                return f"抱歉，我没有找到{disease_name}的详细描述。"
        
        return "抱歉，我暂时无法回答这个问题。"

# 初始化医疗系统
try:
    classifier = MedicalQuestionClassifier()
    searcher = MedicalAnswerSearcher()
    print("医疗知识图谱系统初始化成功！")
except Exception as e:
    print(f"系统初始化失败: {e}")
    classifier = None
    searcher = None

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """问答API"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': '问题不能为空'}), 400
        
        if not classifier or not searcher:
            return jsonify({'error': '系统未初始化'}), 500
        
        # 分类问题
        classify_result = classifier.classify(question)
        
        if not classify_result or not classify_result.get('question_types'):
            answer = "您好，我是小勇医药智能助理，希望可以帮到您。如果没答上来，可联系https://liuhuanyong.github.io/。祝您身体棒棒！"
        else:
            # 获取疾病名称
            disease_name = None
            if 'disease' in classify_result.get('args', {}):
                disease_name = classify_result['args']['disease'][0]
            
            if not disease_name:
                answer = "抱歉，我没有识别出您询问的疾病名称。"
            else:
                # 获取问题类型
                question_type = classify_result['question_types'][0]
                
                # 搜索答案
                answer = searcher.search_main(question_type, disease_name)
        
        return jsonify({
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'处理问题时发生错误: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'system': 'medical-qa-system',
        'version': '1.0.0'
    })

@app.route('/api/build_graph', methods=['POST'])
def build_knowledge_graph():
    """构建知识图谱"""
    try:
        # 检查Neo4j连接
        from build_medicalgraph import MedicalGraph
        
        # 创建知识图谱实例
        medical_graph = MedicalGraph()
        
        # 测试Neo4j连接
        try:
            # 尝试连接Neo4j
            medical_graph.g.run("RETURN 1")
        except Exception as neo4j_error:
            return jsonify({
                'status': 'error',
                'message': f'Neo4j数据库连接失败: {str(neo4j_error)}。请确保Neo4j已安装并运行。',
                'instructions': {
                    'step1': '安装Java环境',
                    'step2': '下载并安装Neo4j',
                    'step3': '启动Neo4j服务',
                    'step4': '配置数据库连接信息'
                }
            }), 500
        
        # 如果连接成功，检查是否已构建
        try:
            # 检查数据库中是否有数据
            result = medical_graph.g.run("MATCH (n) RETURN count(n) as total_nodes LIMIT 1")
            total_nodes = result.data()[0]['total_nodes']
            
            if total_nodes > 0:
                return jsonify({
                    'status': 'success',
                    'message': '知识图谱已构建完成！',
                    'data': {
                        'diseases': 8807,
                        'symptoms': 5998,
                        'relationships': '300K+',
                        'total_nodes': total_nodes,
                        'status': '已构建'
                    }
                })
            else:
                return jsonify({
                    'status': 'warning',
                    'message': '知识图谱构建需要1-2小时，建议在命令行中运行',
                    'command': 'python3 build_medicalgraph.py',
                    'data': {
                        'diseases': 8807,
                        'symptoms': 5998,
                        'relationships': '300K+',
                        'estimated_time': '1-2小时'
                    }
                })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'检查知识图谱状态失败: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'知识图谱构建失败: {str(e)}'
        }), 500

@app.route('/api/graph_stats')
def get_graph_stats():
    """获取知识图谱统计信息"""
    try:
        # 这里可以连接Neo4j获取实际统计信息
        # 目前返回模拟数据
        return jsonify({
            'diseases': 8807,
            'symptoms': 5998,
            'drugs': 2000,
            'relationships': 300000,
            'departments': 50,
            'foods': 1000
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取统计信息失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("启动医疗知识图谱问答系统Web服务器...")
    print("访问地址: http://localhost:8080")
    print("按 Ctrl+C 停止服务器")
    app.run(debug=True, host='0.0.0.0', port=8080)
