from classes import Chats
import random

# варианты диалогов
q1 = ['/start', 'большую', 'наличкой', 'да']
a1 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите большую пиццу, оплата - наличкой?', 'Спасибо за заказ']

q2 = ['/start', 'маленькую', 'наличкой', 'да']
a2 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите маленькую пиццу, оплата - наличкой?', 'Спасибо за заказ']

q3 = ['/start', 'большую', 'картой', 'да']
a3 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите большую пиццу, оплата - картой?', 'Спасибо за заказ']

q4 = ['/start', 'маленькую', 'картой', 'да']
a4 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите маленькую пиццу, оплата - картой?', 'Спасибо за заказ']

q5 = ['/start', 'большую', 'наличкой', 'нет', 'маленькую', 'наличкой', 'да']
a5 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите большую пиццу, оплата - наличкой?', 'Какую вы хотите пиццу? Большую или маленькую?',
      'Как вы будете платить?', 'Вы хотите маленькую пиццу, оплата - наличкой?', 'Спасибо за заказ']

q6 = ['/start', 'маленькую', 'наличкой', 'нет', 'большую', 'картой', 'да']
a6 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите маленькую пиццу, оплата - наличкой?', 'Какую вы хотите пиццу? Большую или маленькую?',
      'Как вы будете платить?', 'Вы хотите большую пиццу, оплата - картой?', 'Спасибо за заказ']

q7 = ['/start', 'большую', 'картой', 'нет', 'маленькую', 'картой', 'да']
a7 = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
      'Вы хотите большую пиццу, оплата - картой?', 'Какую вы хотите пиццу? Большую или маленькую?',
      'Как вы будете платить?', 'Вы хотите маленькую пиццу, оплата - картой?', 'Спасибо за заказ']

dialogs_questions = [q1, q2, q3, q4, q5, q6, q7]
dialog_answers = [a1, a2, a3, a4, a5, a6, a7]
tests = []
chat = Chats()

for dialog_answer, dialog_question in zip(dialog_answers, dialogs_questions):
    chat.new_chat('0007')
    print(dialog_answer)
    test = []
    for answer, question in zip(dialog_answer, dialog_question):
        answered = chat.update('0007', question)
        print(question)
        print(answer)
        if answered == answer:
            test.append(True)
        else:
            test.append(False)

    if False in test:
        tests.append(False)
    else:
        tests.append(True)



print('\n\n\nparallel execution')
chat_ids = []
parallel_test = {
    '1': [],
    '2': []
}
# количество независимых чатов
for i in range(3):
    chat_ids.append(str(random.randint(10000, 20000)))

chats = Chats()

chats.new_chat(chat_ids[0])
chats.new_chat(chat_ids[1])

for i in range(4):
    answered_1 = chats.update(chat_ids[0], q1[i])
    print('Q1: ', q1[i])
    print('A1: ', answered_1, '\n')
    if answered_1 == a1[i]:
        parallel_test['1'].append(True)
    else:
        parallel_test['1'].append(False)

    answered_2 = chats.update(chat_ids[1], q2[i])
    print('Q2: ', q2[i])
    print('A2: ', answered_2, '\n')
    if answered_2 == a2[i]:
        parallel_test['2'].append(True)
    else:
        parallel_test['2'].append(False)






print('Single mode execution results: ', tests)
print('Parallel mode execution results: ', parallel_test)
