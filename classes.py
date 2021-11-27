
from transitions import Machine
import logging
import re


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('transitions').setLevel(logging.INFO)


class PizzaBot(object):

    states = ['idle', 'pizza_size_q', 'payment_method_q', 'thanks', 'check']

    def __init__(self):
        self.respond = 'Какую вы хотите пиццу? Большую или маленькую?'
        self.request = ''
        self.is_okay = True
        self.is_finished = False
        self.pizza_size = 'большую'
        self.payment_method = 'наличкой'

        self.machine = Machine(model=self, states=PizzaBot.states, initial='idle')

        self.machine.add_transition('hi', 'idle', 'pizza_size_q', after='size_respond')

        self.machine.add_transition('pay', 'pizza_size_q', 'payment_method_q',
                                    after='pay_respond', conditions=['size_checker'])

        self.machine.add_transition('check', 'payment_method_q', 'check',
                                    after='check_order_respond', conditions=['payment_method_checker'])

        self.machine.add_transition('thx', 'check', 'thanks',
                                    after='thanks_respond', conditions=['check_checker'])
        self.machine.add_transition('thx', 'check', 'pizza_size_q', after='size_respond')

        self.machine.add_transition('hi', 'thanks', 'pizza_size_q', after='size_respond')

    def size_respond(self):
        self.respond = 'Какую вы хотите пиццу? Большую или маленькую?'
        return self.respond

    def pay_respond(self):
        self.respond = 'Как вы будете платить?'
        return self.respond

    def check_order_respond(self):
        self.respond = f'Вы хотите {self.pizza_size} пиццу, оплата - {self.payment_method}?'
        return self.respond

    def thanks_respond(self):
        self.respond = 'Спасибо за заказ'
        self.is_finished = True
        return self.respond

    @property
    def size_checker(self):
        if re.match(r'больш', self.request, re.IGNORECASE):
            self.pizza_size = 'большую'
            self.is_okay = True
            self.request = ''
            return True
        elif re.match(r'мал', self.request, re.IGNORECASE):
            self.pizza_size = 'маленькую'
            self.is_okay = True
            self.request = ''
            return True
        else:
            self.is_okay = False
            self.request = ''
            return False

    @property
    def payment_method_checker(self):
        if re.match(r'^нал|день', self.request, re.IGNORECASE):
            self.payment_method = 'наличкой'
            self.is_okay = True
            self.request = ''
            return True
        elif re.match(r'карт|безнал|кредит', self.request, re.IGNORECASE):
            self.payment_method = 'картой'
            self.is_okay = True
            self.request = ''
            return True
        else:
            self.is_okay = False
            return False

    @property
    def check_checker(self):
        if re.match(r'д', self.request, re.IGNORECASE):
            self.is_okay = True
            self.request = ''
            return True
        elif re.match(r'н', self.request, re.IGNORECASE):
            self.is_okay = False
            self.request = ''
            # self.to_idle()
            return False
        else:
            self.is_okay = False
            return False


class Chats(object):
    def __init__(self):
        self.chats = {}

    def new_chat(self, chat_id: str):
        if chat_id not in self.chats:
            self.chats[chat_id] = PizzaBot()

    def update(self, chat_id, request):
        if self.chats[chat_id].state == 'idle':
            self.chats[chat_id].hi()
            return self.chats[chat_id].respond
        elif self.chats[chat_id].state == 'pizza_size_q':
            self.chats[chat_id].request = request
            self.chats[chat_id].pay()
            return self.chats[chat_id].respond
        elif self.chats[chat_id].state == 'payment_method_q':
            self.chats[chat_id].request = request
            self.chats[chat_id].check()
            return self.chats[chat_id].respond
        elif self.chats[chat_id].state == 'check':
            self.chats[chat_id].request = request
            self.chats[chat_id].thx()
            result = self.chats[chat_id].respond
            if self.chats[chat_id].is_finished:
                print('killed ', chat_id)
                self.chats.pop(chat_id)
            return result

