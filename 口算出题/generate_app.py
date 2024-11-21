import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import random
import os
import generate_questions
import ctypes

# 隐藏控制台窗口
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
class GenerateQuestionsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("生成100题文档")

        # 保存路径选择
        self.save_path_label = tk.Label(root, text="选择保存路径:")
        self.save_path_label.pack(pady=5)

        self.save_path_button = tk.Button(root, text="选择路径", command=self.choose_save_path)
        self.save_path_button.pack(pady=5)

        self.selected_path_label = tk.Label(root, text="当前路径: 未选择")
        self.selected_path_label.pack(pady=5)

        # 动态添加题型和题目数量的部分
        self.entries_frame = tk.Frame(root)
        self.entries_frame.pack(pady=10)

        self.type_label = tk.Label(root, text="选择生成的计算题类型并输入题目数量:")
        self.type_label.pack()

        self.add_type_button = tk.Button(root, text="添加题型", command=self.add_question_type)
        self.add_type_button.pack(pady=5)

        # 文档份数输入
        self.total_page_label = tk.Label(root, text="请输入生成的文档份数:")
        self.total_page_label.pack(pady=5)

        self.total_page_entry = tk.Entry(root)
        self.total_page_entry.pack(pady=5)

        # 生成按钮
        self.generate_button = tk.Button(root, text="生成文档", command=self.generate_document)
        self.generate_button.pack(pady=5)

        # 初始化题型列表和保存路径
        self.question_entries = []
        self.save_path = ""

    def choose_save_path(self):
        # 弹出文件选择对话框，获取保存路径
        self.save_path = filedialog.askdirectory()
        if self.save_path:
            self.selected_path_label.config(text=f"当前路径: {self.save_path}")
        else:
            self.selected_path_label.config(text="未选择保存路径")

    def add_question_type(self):
        frame = tk.Frame(self.entries_frame)
        frame.pack(pady=2)

        types = ["20以内退位减法", "两位数加减整十数", "两位数加减一位数",
                 '6以内的乘法练习（求结果）',"6以内的乘法练习（求乘数）","6以内的乘法练习（乘法后加减）",
                 '10以内的乘法练习（求结果）',"10以内的乘法练习（求乘数）","10以内的乘法练习（乘法后加减）"]

        type_var = tk.StringVar()
        type_var.set(types[0])  # 默认选项
        type_menu = tk.OptionMenu(frame, type_var, *types)
        type_menu.pack(side="left")

        num_label = tk.Label(frame, text="题目数量:")
        num_label.pack(side="left", padx=5)

        num_entry = tk.Entry(frame, width=5)
        num_entry.pack(side="left")

        # 存储每一组题型和数量输入
        self.question_entries.append((type_var, num_entry))

    def generate_document(self):
        """ 根据用户输入的题型和题目数量生成文档 """
        save_path = self.save_path
        if not save_path:
            messagebox.showwarning("路径错误", "请先选择保存路径")
            return

        try:
            total_page = int(self.total_page_entry.get())
        except ValueError:
            messagebox.showwarning("输入错误", "请正确输入文档份数")
            return

        # 创建Generate_questions类的实例
        question_generator = generate_questions.Generate_questions()

        for i in range(1, total_page + 1):
            all_questions = []

            # 收集所有输入的题型和数量，并生成对应题目
            total_questions = 0
            for type_var, num_entry in self.question_entries:
                selected_type = type_var.get()
                try:
                    num_questions = int(num_entry.get())
                except ValueError:
                    messagebox.showwarning("输入错误", "请为每个题型输入正确的题目数量")
                    return

                # 根据类型选择对应的生成函数
                if selected_type == "20以内退位减法":
                    generate_function = question_generator.two_digits_less_than_20_minus_one_digit
                elif selected_type == "两位数加减整十数":
                    generate_function = question_generator.two_digits_minus_plus_x0
                elif selected_type == "两位数加减一位数":
                    generate_function = question_generator.two_digits_minus_plus_one_digit
                elif selected_type == "6以内的乘法练习（求结果）":
                    generate_function = question_generator.mutiple_less_than_6
                elif selected_type == "6以内的乘法练习（求乘数）":
                    generate_function = question_generator.solve_multipe_less_than_6
                elif selected_type == "6以内的乘法练习（乘法后加减）":
                    generate_function = question_generator.mutiple_plus_mius_less_than_6
                elif selected_type == "10以内的乘法练习（求结果）":
                    generate_function = question_generator.mutiple_less_than_10
                elif selected_type == "10以内的乘法练习（求乘数）":
                    generate_function = question_generator.solve_multipe_less_than_10
                elif selected_type == "10以内的乘法练习（乘法后加减）":
                    generate_function = question_generator.mutiple_plus_mius_less_than_10

                # 确保总题目数不超过100
                if total_questions + num_questions > 100:
                    messagebox.showwarning("题目数量错误", "题目总数不能超过100，请调整数量")
                    return

                # 生成题目并加入到总题目列表中
                for _ in range(num_questions):
                    all_questions.extend(generate_function())

                total_questions += num_questions

            # 如果总题数不足100，提醒用户
            if total_questions < 100:
                messagebox.showwarning("题目数量不足", "题目总数不足100，请添加更多题目")
                return

            # 打乱题目顺序
            random.shuffle(all_questions)

            # 创建 Word 文档并将题目填入表格
            doc = Document()
            table = doc.add_table(rows=(100 // 4), cols=4)  # 假设每行4题，生成25行表格

            index = 0
            for row in table.rows:
                for cell in row.cells:
                    if index < len(all_questions):
                        cell.text = all_questions[index]
                        index += 1

            # 保存文档，命名为 '口算练习{i}.docx'，如果已有文件则覆盖
            file_path = os.path.join(save_path, f"口算练习{i}.docx")
            doc.save(file_path)

        messagebox.showinfo("生成成功", f"文档已成功生成并保存在 {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GenerateQuestionsApp(root)
    root.mainloop()
