import openai as ai
import yaml
question_file = 'questions.txt'
def generate_message():
    messages = []
    with open(question_file, 'r', encoding='utf8') as the_file:
        lines = the_file.readlines()
        for i in range(len(lines)):
            if i%2 == 1:
                messages.insert(i, {"role": "asistent", "content": lines[i]})
            else:
                messages.insert(i, {"role": "user", "content": lines[i]})
    return messages
m  = generate_message()
print(m)