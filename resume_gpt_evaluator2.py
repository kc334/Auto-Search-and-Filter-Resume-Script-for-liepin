import openai
import time


def evaluate_resume(resume_text, max_retries=10, timeout=10):
    file_path = 'apiKey.txt'
    with open(file_path, 'r') as file:
            openai.api_key = file.readline().strip()

    system_msg = "您是小智，您是一个房地产公司的人力资源经理。您的任务是通过分析申请者的简历内容来对简历进行分类，然后决定他们是否招聘他们做房地产销售。"
    user_msg1 = "如果其求职兴趣包括房产销售或者销售，那么他们就合适。在分析的时候，请考虑到零售，贸易，人事，行政等不算销售。我会给您一个申请人的求职兴趣，您需要逐步分析它，以确定是否申请人适合做房地产销售。明白吗？"
    #user_msg1 = "如果其求职兴趣包括房产销售或者销售，那么他们就合适。我会给您一个申请人的求职兴趣，您需要逐步分析它，以确定是否申请人适合做房地产销售。明白吗？"
    assistant_msg1 = "是的，我明白。我是小智，我将分析您的申请人求职兴趣"
    user_msg2 = ["听上去不错！那么让我们开始吧 :)\n对于给定的工作：\n","\n 这个申请人是否适合做房地产销售"]
    user_msg3 = "谢谢您的分析。请您基于以上分析给出结论，选择是否招聘这个申请人’"
    def evaluate(resume_text):
        retries = 0
        while retries < max_retries:
            try:
                print("attempt:", retries)
                messages = [
                    {"role": "system",
                     "content": system_msg},
                    {"role": "user",
                     "content": user_msg1},
                    {"role": "assistant", "content": assistant_msg1},
                    {"role": "user",
                     "content": user_msg2[0] + resume_text + user_msg2[1]},
                ]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0,
                    timeout=timeout
                )
                return response.choices[0].message.content
            except openai.error.OpenAIError as e:
                print(f"OpenAI API调用出错: {e}")
                retries += 1
                time.sleep(1)  # 在重试之前稍微等待一下
            except Exception as e:
                print(f"发生未知错误: {e}")
                break
    def hire(resume_text, assistant_msg2):
        retries = 0
        while retries < max_retries:
            try:
                print("attempt:", retries)
                messages = [
                    {"role": "system",
                     "content": system_msg},
                    {"role": "user",
                     "content": user_msg1},
                    {"role": "assistant", "content": assistant_msg1},
                    {"role": "user",
                     "content": user_msg2[0] + resume_text + user_msg2[1]},
                ]
                functions = [
                    {
                        "name": "hire",
                        "description": "如果申请人合适，运行该函数将其标注为合适并且发放录用通知书",
                        "parameters":{"type": "object", "properties": {}}
                    }
                ]
                messages.append({"role": "assistant", "content": assistant_msg2})
                messages.append({"role": "user", "content": user_msg3})

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0,
                    timeout=timeout,
                    functions=functions,
                    function_call="auto"
                )
                return response
            except openai.error.OpenAIError as e:
                print(f"OpenAI API调用出错: {e}")
                retries += 1
                time.sleep(1)  # 在重试之前稍微等待一下
            except Exception as e:
                print(f"发生未知错误: {e}")
                break
    evaluation = evaluate(resume_text)
    print(evaluation)
    response = hire(resume_text,evaluation)
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        print(True)
        return True
    else:
        print(False)
        print(response["choices"][0]["message"]["content"])
        return False

