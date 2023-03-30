import openai as ai
import yaml
import listenerLocal
import talker
import rospy
from std_msgs.msg import String
import time
import multiprocessing
# import STT_Prototype_2
# import tablet
# Python 2 codeFal

# IP = "192.168.171.35"

# tts = ALProxy("ALTextToSpeech", IP, 9559)
rospy.init_node('GPT', anonymous=True)
persona_file = 'persona.txt'
keywords_file = 'keywords.yaml'
question_file = 'questions.txt'
history_file = 'history2.txt'
prompt_file = 'prompt.txt'
final_stage_file = 'questions_professors.txt'
openai_key = "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"
# def generate_message(messages,question):
#     with open(question_file, 'r', encoding='utf8') as file1:
#         with open(history_file, 'r', encoding='utf8') as file2:
#             lines = file1.readlines()
#             index = 0
#             for i in range(len(lines)):
#                 index = index+1
#                 if i%2 == 1:
#                     messages.insert(index, {"role": "assistant", "content": lines[i]})
#                 else:
#                     messages.insert(index, {"role": "user", "content": lines[i]})
#             lines = file2.readlines()
#             for i in range(len(lines)):
#                 index = index+1
#                 if i%2 == 1:
#                     messages.insert(index, {"role": "assistant", "content": lines[i]})
#                 else:
#                     messages.insert(index, {"role": "user", "content": lines[i]})

#             messages.insert(index+1, {"role": "user", "content": question})
#     return messages
def extract_topics(string_with_topics):
    topics = ["Computer Vision",
    "Machine Learning"
    "AI",
    "Communications",
    "Computer Architecture",
    "Analog Electronics",
    "Signal Processing",
    "Control Systems",
    "Wearable Devices",
    "Semiconductors",
    "Circuits",
    "Embedded Systems",
    "Robotics",
    "Networks"]
    interested_topics = []
    if "none of the above" in string_with_topics.lower():
        return ["none"]
    if "not sure" in string_with_topics.lower():
        return ["?"]
    for topic in topics:
        if topic.lower() in string_with_topics.lower():
            interested_topics.append(topic.lower())
    return interested_topics

def change_prompt_file(prompt):
    with open(prompt_file, 'w',encoding="utf8") as the_file:
        chat_log = the_file.write(prompt)
        string = open('prompt.txt').read()
        for word in string.split():
            if len(word) >= 4096:
                print("the file is so large!!!! higher than 4096 tokens")


def attach_keyword_information(question,cnt = 0):
    chat_log = ""
    words = question.split()
    with open(keywords_file, 'r') as file:
        keywords_yaml = yaml.safe_load(file)
    for word in words:
        if word.lower() in keywords_yaml.keys():
            if cnt == 0:
                chat_log = f"{chat_log}\n {keywords_yaml.get(word)}"
                word_previous = word
            else:
                if (keywords_yaml.get(word_previous))[-1] != keywords_yaml.get(word)[-1]:
                    chat_log = f"{chat_log}\n {keywords_yaml.get(word)}"
                else:
                    pass
            cnt = cnt + 1
    return chat_log

def attach_history_information(chat,name):
    with open(history_file, 'a',encoding="utf8") as the_file:
        chat_log = the_file.write(f"{name}: {chat}\n")

# def chat(question, chat_log=None) -> str:
#     if chat_log is None:
#         chat_log = start_chat_log
#     key_information = attach_keyword_information(question)
#     prompt = f"{chat_log}\n{key_information}\n"
#     change_prompt_file(prompt)
#     message=[{"role": "system", "content": prompt}]
#     message = generate_message(message,question)
#     response = ai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages = message,
#         temperature=0.5,
#     )
#     # print("response:",response)
#     # print("message",message)
#     content = response['choices'][0]['message']['content']

#     return content

def send_request(queue_,model_,prompt_,temperature_,max_tokens_,top_p_,frequency_penalty_,presence_penalty_,stop_):
    chat_response = completion.create(model=model_,
    prompt=prompt_,
    temperature=temperature_,
    max_tokens=max_tokens_,
    top_p=top_p_,
    frequency_penalty=frequency_penalty_,
    presence_penalty=presence_penalty_,
    stop=stop_
    )
    queue_.put(chat_response)

def chat(question,chat_log = None,final_stage = False) -> str:
    if(final_stage==False):
        with open(question_file,'r',encoding="utf8") as the_file:
            questions = the_file.read()
        with open(history_file,'r',encoding="utf8") as the_file:
            history = the_file.read()
        if(chat_log == None):
            chat_log = start_chat_log
        key_information = attach_keyword_information(question)
        prompt = f"{chat_log}\n{key_information}\n{questions}\n{history}\nHuman: {question}\nAI:"
    else:
        with open(final_stage_file,'r',encoding="utf8") as the_file:
            final_stage_prompt = the_file.read()
        prompt = f"{final_stage_prompt}\n{question}"
    change_prompt_file(prompt)
    queue = multiprocessing.Queue()
    chat_proc = multiprocessing.Process(target=send_request,kwargs={"queue_":queue,
    "model_":"text-davinci-003",
    "prompt_":prompt,
    "temperature_":0, # randomness
    "max_tokens_":400, # word length
    "top_p_":0.5, # output diversity(cumulative probability)
    "frequency_penalty_":0.0, # output repetitive
    "presence_penalty_":0.0, # input repetitive
    "stop_":["Human:", "AI:"]}
    )
    chat_proc.start()
    start_time = time.time()
    flag = True
    while(chat_proc.is_alive() == True):
        if(time.time()-start_time > 2 and flag):
            talker.talk("#think let me think, I might take a while.")
            flag = False
    chat_proc.join()
    return queue.get().choices[0].text

# def modify_start_message(chat_log,question,answer) -> str:
#     if chat_log == None:
#         chat_log = start_chat_log
#     chat_log += f"Human: {question}\nAI: {answer}\n"
#     with open(question_file, 'a',encoding="utf8") as the_file:
#         start_chat_log = the_file.write(f"Human: {question}\nAI: {answer}\n")
#     return chat_log

def extract_command(msg):
    if "*" in msg:
        command=msg[msg.find("*")+1:].split()[0]
        message = msg.split('*')[0]
    else:
        command="Non"
        message = msg
    return message,command

if __name__ == "__main__":
    ig = listenerLocal.InfoGetter()
    rospy.Subscriber('nlp_input', String, ig)
    ai.api_key = openai_key
    data = []
    with open(persona_file,'r',encoding="utf8") as the_file:
        start_chat_log = the_file.read()
    completion = ai.Completion()
    mode = input("Input 1 for free tour, input 2 for fix tour:")
    if mode=="2":
        print("fix tour mode executed")
        question_file = "questions2.txt"
    else:
        print("free tour mode executed")
    while True:
        question = ""
        # trigger = listenerLocal.wait_trigger()
        # talker.talk("red",'leds')
        msg = ig.get_msg()
        ig.clear_event()
        question = msg.data
        talker.talk("green",'leds')
        # question = input("question:")
        if question != "":
            if question == "stop":
                break
            elif question == "forget":
                with open(history_file, 'w',encoding="utf8") as the_file:
                    chat_log = the_file.write("")
            response = chat(question,start_chat_log)
            res, command = extract_command(response)
            # print("res:",res)
            talker.talk(res)
            if "room" in command:
                room = (command[4:len(command)])
                print("find a room!!!!", room)
                print("len",len(room))
                if len(room) == 3:
                    room = "0"+room
                talker.talk(room,'target')
                print("Command sent to topic target with value:" + room)
            elif "goal_cancel" in command:
                talker.talk(command,'goal_cancel')
            elif "next_stage" in command:
                with open(history_file, 'w',encoding="utf8") as the_file:
                    chat_log = the_file.write("")
                talker.talk("06mlift",'target')
                talker.talk("Now we can go visit any professors you might be interested in. What part of Electronic Engineering interests you most?",'speak')
                question = ig.get_msg()
                response = chat(question,None,True)
                print("response2:",response)
                potential_topics = extract_topics(response)
                print(potential_topics)
                ig.clear_event()
                if "robotics" in potential_topics:
                    talker.talk("Robotics sounds like a great fit for you! #follow_back Come with me to Professor Yiannis Demiris's office. He loves robots!",'speak')
                    msg = ig.get_msg()
                    question = msg.data
                    if "continue" in question.lower():
                        talker.talk("Professor Demiris's office is Room 1011, let's go!",'speak')
                        talker.talk("room1011",'target')
            elif not "Non" in command:
                talker.talk(command,'target')
            attach_history_information(question,"Human")
            attach_history_information(response,"AI")
            print("AI: ",response)
            print("Command:",command)
            question = ""
            ig.clear_event()
            