import json
from random import randint
import re


def process_keywords(input_text):
    with open("animations.json", "r") as animations_file:
        available_animations = json.load(animations_file)

        # removing the keywords that can not be mapped to animations
        input_text_keywords = [word for word in input_text.split() if word.startswith("#")]

        for word in input_text_keywords:
            # print("word:",word)
            if not word[1:] in available_animations.keys():
                input_text = input_text.replace(word, "")

        input_text = re.sub("\s\s+", ' ', input_text)

        # substituting keywords for animation triggers
        for animation_type in available_animations.keys():
            number_of_occurances = input_text.count("#"+str(animation_type))
            i = 0
            while i < number_of_occurances:
                number_of_available_animations = len(available_animations.get(animation_type))
                chosen_animation = available_animations.get(animation_type)[randint(0, number_of_available_animations - 1)]
                value_to_insert = "^pCall(ALAnimationPlayer.run(\"" + str(chosen_animation) + "\"))"
                input_text = input_text.replace("#"+str(animation_type), value_to_insert, 1)
                i += 1
                # print("chosen animation: ",chosen_animation)
                # print("input_text:", input_text)

        return input_text