# -*- coding: utf-8 -*-
# """suggestion_gpt.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1QGJdQ2Fua4ScKP9TNhgQu1wETTOOh-zf
# 

scale_amt = 1

#messages to store the conversation
messages = []
generated_questions = []
messages_user = ["how do i improve my credit score","what is a credit score","what is a ltv percentage","how do i improve my ltv","what is financial advice for my 20s","can you give me credit score advice","can you help with my ltv","can you help with financial advice","what is a DTI"]
match scale_amt:
    case 1:
         messages.append({"role": "system", "content": "You are a helpful financial assistant talking to a young child."})
    case 2:
         messages.append({"role": "system", "content": "You are a helpful financial assistant explaining financial concepts to a teenager with basic financial literacy."})
    case 3:
         messages.append({"role": "system", "content": "You are a skilled financial assistant explaining complex financial concepts."})

#ngram stuff
from collections import Counter
from collections import defaultdict
import numpy as np
import string


def unzip(pairs):
    return tuple(zip(*pairs))

def freqs(messages_user):
  """
  Input:
    messages_user
  """
  letters = set(string.ascii_lowercase)

  messages = " ".join(messages_user)
  counter = Counter(messages)

  total = sum(counter.values())
  return [(char, cnt/total) for char, cnt in counter.most_common()]

freqs(["why didnt that work", "why was my credit score bad"])

def train_n_gram(messages, n):
  raw_lm = defaultdict(Counter) #  history -> {char -> count}
  history = "~" * (n - 1)  #  length n - 1 history
  string = "~~~".join(messages)

  for char in string:
      raw_lm[history][char] += 1
      # slide history window to the right by one character
      history = history[1:] + char

  # {history -> [(char, freq), ...]}
  lm = {history : freqs(counter) for history, counter in raw_lm.items()}  #
  return lm

lm = train_n_gram(messages_user, 12)

print(lm)

def generate_letter(lm, history):
    """
    """

    if not history in lm:
        return "~"
    letters, probs = unzip(lm[history])
    i = np.random.choice(letters, p=probs)
    return i


def generate_text(lm, n, nletters = 10):
    history = "~" * (n - 1)
    text = []
    for i in range(nletters):
        c = generate_letter(lm, history)
        if c == "~":
          return "".join(text)
        text.append(c)
        history = history[1:] + c

    if text in messages_user:
      generate_text(lm, n, nletters)

    return "".join(text)

(generate_text(lm, 12, 70))

import openai
#Please add your open AI API key here.
from google.colab import userdata
openai.api_key = userdata.get('api_key')





#Append the message to the conversation history
def add_message(role, message):
    messages.append({"role": role, "content": message})

#Trigger the Open AI APIs
def converse_with_chatGPT():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #Open AI model name
        messages=messages, # user query
        max_tokens = 1024, # this is the maximum number of tokens that can be used to provide a response.
        n=1, #number of responses expected from the Chat GPT
        stop=None,
        temperature=0.5 #making responses deterministic or not much imaginative
    )
    # print(response)
    message = response.choices[0].message.content
    add_message("assistant", message)
    return message.strip()

# process user prompt
def process_user_query(prompt):
    user_prompt = (f"{prompt}")
    add_message("user", user_prompt)
    result = converse_with_chatGPT()
    print(result)

#Request user to provide the query
def user_query():
    while True:
        print(generated_questions)
        prompt = input("Enter your question: ")
        response = process_user_query(prompt)
        messages_user.append(prompt)
        print(response)

        lm = train_n_gram(messages_user, 12)

        q = generate_text(lm, 12, 40)
        while q in generated_questions:
          q = generate_text(lm, 12, 40)
        generated_questions.append(q)

        if len(generated_questions) > 3:
          generated_questions.pop(0)

# Call user_query to start conversation with user
user_query()



