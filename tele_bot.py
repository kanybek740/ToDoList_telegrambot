import telebot
import json
import requests
import datetime

bot = telebot.TeleBot('626925053:AAG6GeoY_-ylFAcEF-BDvufrFheT2US_u08')
tasks = []
user_list = []
id_ = 1
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Посмотреть список задач', 'Добавить задачу', 'Очистить список','Выйти')
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Редактировать','Удалить', 'Назад')
filename = 'user_tasks.txt'
old_message = 1
new_message = []
my_task = []


@bot.message_handler(commands = ["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Воспользуйся меню снизу, для работы",
                    reply_markup=keyboard1)

@bot.message_handler(commands = ["help"])
def start_message(message):
    bot.send_message(message.chat.id, "To list - это один из наиболее распространенных инструментов для управления своими делами — это простой перечень дел, их список. \n Если есть какие-либо вопросу можете промолчать :)")

@bot.message_handler(commands = ["info"])
def start_message(message):
    bot.send_message(message.chat.id, "Над этим проектом работали команда №3: \n 1. Каныбек \n 2. Адинай \n 3. Кайрат-Кыргыз \n 4. Батыр \n 5. Бахтияр")


@bot.message_handler(content_types=['text'])
def send_text(message):
    filename = str(message.chat.id)
    if message.text.lower() == 'выйти':
        bot.send_message(message.chat.id, 'Пока, удачного дня!')

    elif message.text.lower() == 'добавить задачу':
        bot.send_message(message.chat.id, 'Ведите новое сообщение:')
        bot.register_next_step_handler(message, add_task)

    elif message.text.lower() == "посмотреть список задач":
        if bool(tasks) == True and str(message.chat.id) in user_list:
            myfile = open(filename, mode='r', encoding='Latin-1')
            list_of_tasks = json.load(myfile)
            result = ''
            i=1
            for user in list_of_tasks:
                print(str(i)+") " + str(user['task']) +" "+ str(user['datetime']))
                result+=(str(i)+") " + str(user['task'])+" "+str(user['datetime'])+"\n")
                i+=1
            bot.send_message(message.chat.id, result, reply_markup=keyboard2)

        else:
            bot.send_message(message.chat.id, 'Список пуст')
        

    elif message.text.lower() == 'удалить':
        bot.send_message(message.chat.id, 'Ведите id дела, которое хотите удалить:',reply_markup=keyboard1)
        bot.register_next_step_handler(message, delete_task)

    elif message.text.lower() == 'редактировать':
        bot.send_message(message.chat.id, 'Ведите id дела, которое хотите изменить:',reply_markup=keyboard1)
        bot.register_next_step_handler(message, edit_task)
        
    elif message.text.lower() == 'очистить список':
        bot.send_message(message.chat.id, 'Вы уверены?')
        bot.register_next_step_handler(message, delete_all)
        
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, "Назад",
                    reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def add_task(message):
    filename = str(message.chat.id)
    if str(message.chat.id) not in user_list:
        user_list.append(str(message.chat.id))
    my_task.append(message.text)
    new_message.append(message.text)
    print(my_task)
    bot.send_message(message.chat.id, 'Введите дату и время через пробелы (гггг, мм, дд, чч, мм)(Пример: 2016 5 10 11 30)')
    bot.register_next_step_handler(message, add_datetime)
    
# 
     
def add_datetime(message):
    # check_datetime(message)
    correct = None
    text = message.text
    time = text.split(" ")
    int_time = []
    first = True
    for i in time:
        if i.isnumeric():
            int_time.append(int(i))
        else:
            first = False
    if len(int_time) < 5:
        first = False
    if first == True:
        try:
            newDate = datetime.datetime(*int_time)
            correct = True
        except ValueError:
            correct = False

    if correct == True: 
        filename = str(message.chat.id)
        print(new_message[0])
        myfile = open(filename, mode='w', encoding='Latin-1')
        print(message.text)
        tasks.append({'task':new_message[0], 'datetime':datetime.datetime(*int_time).strftime("%Y-%m-%d %H:%M")})
        new_message.clear()
        json.dump(tasks, myfile)
        myfile.close()
        bot.send_message(message.chat.id, 'Добавлено')
    else:
        bot.send_message(message.chat.id, 'неверное значение')

# def check_datetime(message):
#     text = message.text
#     time = text.split(" ")
#     for i in time:
#         if i.isnumeric():
#             int_time.append(int(i))
#             return True
#         else:
#             print("Value Error")
#             return False

def delete_task(message):
    if check_type(message) == False:
        filename = str(message.chat.id)
        myfile = open(filename, mode='w', encoding='Latin-1')
        print(message.text)
        tasks.pop(int(message.text)-1)
        json.dump(tasks, myfile)
        myfile.close()
        bot.send_message(message.chat.id, 'Удалено!')

def check_type(message):
    if str(message.text).isnumeric()==False or int(message.text) > len(tasks):
        bot.send_message(message.chat.id, 'неверное значение')
        return True
    else:
        return False

@bot.message_handler(content_types=['text'])
def edit_task(message):
    if check_type(message) == False:
        old_message = int(message.text)
        print(old_message)
        bot.send_message(message.chat.id, 'На что заменить?')
        bot.register_next_step_handler(message, edit_task_helper)

@bot.message_handler(content_types=['text'])
def edit_task_helper(message):
    new_message.append(message.text)
    bot.send_message(message.chat.id, 'На какое время?')
    bot.register_next_step_handler(message, edit_task_datetime)

def edit_task_datetime(message):
    # check_datetime(message)
    text = message.text
    time = text.split(" ")
    int_time = []
    for i in time:
        if i.isnumeric():
            int_time.append(int(i))
        else:
            first = False
    if len(int_time) < 5:
        first = False
    if first == True:
        try:
            newDate = datetime.datetime(*int_time)
            correct = True
        except ValueError:
            correct = False
    if correct == True: 
        filename = str(message.chat.id)
        print(new_message[0])
        myfile = open(filename, mode='w', encoding='Latin-1')
        print(message.text)
        tasks[old_message - 1] = {'task':new_message[0], 'datetime':datetime.datetime(*int_time).strftime("%Y-%m-%d %H:%M")}
        new_message.clear()
        json.dump(tasks, myfile)
        myfile.close()
        bot.send_message(message.chat.id, 'Добавлено')
    else:
        bot.send_message(message.chat.id, 'неверное значение')



def delete_all(message):
    filename = str(message.chat.id)
    if message.text.lower() == "да":
        tasks.clear()
        myfile = open(filename, mode='w', encoding='Latin-1')
        print(message.text)     
        json.dump(tasks, myfile)
        myfile.close()
        print(tasks)
        bot.send_message(message.chat.id, 'Удалено!')
    else:
        bot.send_message(message.chat.id, 'Отменяем удаление')
    

bot.polling()