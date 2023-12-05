import os
from resume_gpt_evaluator2 import evaluate_resume

def start():

    # 设置保存简历的文件夹路径
    resume_directory = 'resumeList'

    # 获取简历文件夹中所有文件的列表
    resume_files = os.listdir(resume_directory)
    
    # 遍历每个文件
    for filename in resume_files:
        # 完整的文件路径
        file_path = os.path.join(resume_directory, filename)

        # 读取简历内容
        with open(file_path, 'r', encoding='utf-8') as file:
            resume_content_text = file.read()

        # 处理每个简历
        print(filename)
        print(resume_content_text)
        evaluation = evaluate_resume(resume_content_text)



    
start()
