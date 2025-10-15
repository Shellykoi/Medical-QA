#!/usr/bin/env python3
# coding: utf-8
# 医疗知识图谱问答系统 - GUI版本

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import os
import re
from datetime import datetime

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

class MedicalQAGUI:
    """医疗问答系统GUI"""
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_medical_system()
        
    def setup_ui(self):
        """设置用户界面"""
        self.root.title("医疗知识图谱问答系统")
        self.root.geometry("1200x800")
        self.root.configure(bg='#ffffff')
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap('img/wechat.jpg')
        except:
            pass
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🏥 医疗知识图谱问答系统", 
                               font=('Arial', 24, 'bold'), foreground='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # 副标题
        subtitle_label = ttk.Label(main_frame, text="智能医疗助手，为您提供专业的医疗知识问答服务", 
                                  font=('Arial', 14), foreground='#7f8c8d')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 25))
        
        # 输入框架
        input_frame = ttk.LabelFrame(main_frame, text="💬 请输入您的问题", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # 问题输入框
        self.question_var = tk.StringVar()
        self.question_entry = ttk.Entry(input_frame, textvariable=self.question_var, 
                                       font=('Arial', 14), width=50)
        self.question_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.question_entry.bind('<Return>', self.ask_question)
        
        # 提问按钮
        self.ask_button = ttk.Button(input_frame, text="🔍 提问", 
                                   command=self.ask_question, style='Accent.TButton')
        self.ask_button.grid(row=0, column=1)
        
        # 清空按钮
        self.clear_button = ttk.Button(input_frame, text="🗑️ 清空", 
                                      command=self.clear_conversation)
        self.clear_button.grid(row=0, column=2, padx=(10, 0))
        
        # 对话显示区域
        chat_frame = ttk.LabelFrame(main_frame, text="💭 对话记录", padding="10")
        chat_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # 创建滚动文本框
        self.chat_text = scrolledtext.ScrolledText(chat_frame, 
                                                  font=('Arial', 13), 
                                                  wrap=tk.WORD, 
                                                  height=20,
                                                  bg='#ffffff',
                                                  fg='#2c3e50',
                                                  selectbackground='#3498db',
                                                  selectforeground='white')
        self.chat_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置标签样式
        self.chat_text.tag_configure("user", foreground="#2c3e50", font=('Arial', 13, 'bold'))
        self.chat_text.tag_configure("assistant", foreground="#27ae60", font=('Arial', 13))
        self.chat_text.tag_configure("timestamp", foreground="#95a5a6", font=('Arial', 11))
        self.chat_text.tag_configure("error", foreground="#e74c3c", font=('Arial', 13))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("系统已就绪，请输入您的问题")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 示例问题按钮
        example_frame = ttk.Frame(main_frame)
        example_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(example_frame, text="💡 示例问题：", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        examples = [
            "乳腺癌的症状有哪些？",
            "糖尿病",
            "为什么有的人会失眠？",
            "感冒要多久才能好？"
        ]
        
        for example in examples:
            btn = ttk.Button(example_frame, text=example, 
                           command=lambda e=example: self.set_question(e))
            btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # 初始化欢迎消息
        self.add_welcome_message()
        
    def setup_medical_system(self):
        """初始化医疗系统"""
        try:
            self.classifier = MedicalQuestionClassifier()
            self.searcher = MedicalAnswerSearcher()
            self.status_var.set("医疗知识图谱已加载，系统就绪")
        except Exception as e:
            self.status_var.set(f"系统初始化失败: {str(e)}")
            messagebox.showerror("错误", f"系统初始化失败: {str(e)}")
    
    def add_welcome_message(self):
        """添加欢迎消息"""
        welcome_msg = """🏥 欢迎使用医疗知识图谱问答系统！

我是您的智能医疗助手，可以为您提供以下服务：
• 疾病症状查询
• 疾病描述说明  
• 疾病病因分析
• 疾病治疗建议

请在上方输入框中输入您的问题，或点击下方的示例问题开始对话。

⚠️ 重要提醒：本系统仅供参考，不能替代专业医疗建议。如有严重疾病，请及时就医。"""
        
        self.chat_text.insert(tk.END, welcome_msg + "\n\n", "assistant")
        self.chat_text.see(tk.END)
    
    def set_question(self, question):
        """设置问题到输入框"""
        self.question_var.set(question)
        self.question_entry.focus()
    
    def ask_question(self, event=None):
        """处理问题提问"""
        question = self.question_var.get().strip()
        if not question:
            return
        
        # 显示用户问题
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert(tk.END, f"[{timestamp}] 用户: ", "timestamp")
        self.chat_text.insert(tk.END, f"{question}\n", "user")
        
        # 清空输入框
        self.question_var.set("")
        
        # 更新状态
        self.status_var.set("正在分析您的问题...")
        
        # 在新线程中处理问题
        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()
    
    def process_question(self, question):
        """处理问题（在后台线程中）"""
        try:
            # 分类问题
            classify_result = self.classifier.classify(question)
            
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
                    answer = self.searcher.search_main(question_type, disease_name)
            
            # 在主线程中更新UI
            self.root.after(0, self.display_answer, answer)
            
        except Exception as e:
            error_msg = f"处理问题时发生错误: {str(e)}"
            self.root.after(0, self.display_error, error_msg)
    
    def display_answer(self, answer):
        """显示答案"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert(tk.END, f"[{timestamp}] 小勇: ", "timestamp")
        self.chat_text.insert(tk.END, f"{answer}\n\n", "assistant")
        self.chat_text.see(tk.END)
        self.status_var.set("回答完成，请输入下一个问题")
    
    def display_error(self, error_msg):
        """显示错误信息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert(tk.END, f"[{timestamp}] 系统错误: ", "timestamp")
        self.chat_text.insert(tk.END, f"{error_msg}\n\n", "error")
        self.chat_text.see(tk.END)
        self.status_var.set("发生错误，请重试")
    
    def clear_conversation(self):
        """清空对话记录"""
        self.chat_text.delete(1.0, tk.END)
        self.add_welcome_message()
        self.status_var.set("对话记录已清空")

def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置主题样式
    style = ttk.Style()
    style.theme_use('clam')
    
    # 配置按钮样式
    style.configure('Accent.TButton', foreground='white', background='#3498db')
    style.map('Accent.TButton', background=[('active', '#2980b9')])
    
    # 创建应用
    app = MedicalQAGUI(root)
    
    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出医疗问答系统吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动应用
    root.mainloop()

if __name__ == '__main__':
    main()
