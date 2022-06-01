import telebot
import pytz
import datetime

import settings

schedule_fry = ['6:40', '7:10', '7:40', '8:10', '8:40', '9:15',
                '9:50', '10:25', '11:00', '11:35', '12:15', '12:55',
                '13:35', '14:15', '14:55', '15:35', '16:15', '16:55',
                '17:35', '18:15', '18:45', '19:15', '19:45', '20:15',
                '20:45', '21:15', '21:45', '22:20', '22:55', '23:30']
schedule_msc = ['5:25', '5:55', '6:25', '6:55', '7:25', '8:00',
                '8:35', '9:10', '9:45', '10:20', '11:00', '11:40',
                '12:20', '13:00', '13:40', '14:20', '15:00', '15:40',
                '16:20', '17:00', '17:30', '18:00', '18:20', '19:00',
                '19:30', '20:00', '20:30', '21:05', '21:40', '22:15']
# экземляр бота создаем
bot = telebot.TeleBot(settings.TG_TOKEN)

# функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи!')

@bot.message_handler(commands=["bus_to_msc"])
def bus_to_msc(m, res=False):
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    hour = int(now.hour)
    minute = int(now.minute)
    flag = 0
    hour_sch = -1
    min_sch = -1
    for i in schedule_msc:
        hour_sch = i.split(':')[0]
        min_sch = i.split(':')[1]

        if (int(hour_sch) > hour and flag == 0) or (flag == 0 and int(hour_sch) == hour and int(min_sch) >= minute):
            flag = 1
            break
    if flag == 1:
        bot.send_message(m.chat.id, 'Следующий автобус Чижово-Щелковская отправится в ' + str(hour_sch) + ':' + str(min_sch))
    else:
        bot.send_message(m.chat.id, 'Автобусов сегодня нет :(')

@bot.message_handler(commands=["bus_to_fry"])
def bus_to_fry(m, res=False):
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    hour = int(now.hour)
    minute = int(now.minute)
    flag = 0
    hour_sch = -1
    min_sch = -1
    for i in schedule_fry:
        hour_sch = i.split(':')[0]
        min_sch = i.split(':')[1]
        if (int(hour_sch) > hour and flag == 0) or (flag == 0 and int(hour_sch) == hour and int(min_sch) >= minute):
            flag = 1
            break
    if flag == 1:
        bot.send_message(m.chat.id, 'Следующий автобус Щелковская-Чижово отправится в ' + str(hour_sch) + ':' + str(min_sch))
    else:
        bot.send_message(m.chat.id, 'Автобусов сегодня нет :(')

@bot.message_handler(commands=["schedule_to_msc"])
def schedule_to_msc(m, res=False):
    mess = ""
    for i in schedule_msc:
        mess += i + '\n'
    bot.send_message(m.chat.id, 'Расписание автобусов Чижово-Щелковская:\n' + mess)


@bot.message_handler(commands=["schedule_to_fry"])
def schedule_to_fry(m, res=False):
    mess = ''
    for i in schedule_fry:
        mess += i + '\n'
    bot.send_message(m.chat.id, 'Расписание автобусов Щелковская-Чижово:\n' + mess)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Не усложняйте мне жизнь, просто спросите меня что-нибудь из этого:\n '
                                      '\nБлижайший автобус в Москву\n/bus_to_msc\n'
                                      '\nБлижайший автобус во Фрязино\n/bus_to_fry\n'
                                      '\nРасписание автобусов в Москву\n/schedule_to_msc\n'
                                      '\nРасписание автобусов во Фрязино\n/schedule_to_fry\n')
                                      # '\nОстановка бота\n/stop\n')


bot.polling(none_stop=True, interval=0)
