import telebot as tb
from telebot import types
import sqlite3
bot = tb.TeleBot('6406717020:AAEJYdw0pjQE-cykfr5tzrw3sDmUic8PdQw')


def generate_physics_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    mechanics = types.InlineKeyboardButton('Механика', callback_data='sect1')
    thermodynamics = tb.types.InlineKeyboardButton('Термодинамика и МКТ', callback_data='sect2')
    electricity = tb.types.InlineKeyboardButton('Электричество и магнетизм', callback_data='sect3')
    optics = tb.types.InlineKeyboardButton('Оптика', callback_data='sect4')
    quantums = tb.types.InlineKeyboardButton('Квантовая и ядерная физика', callback_data='sect5')
    markup.add(mechanics, thermodynamics, electricity, optics, quantums)
    bot.send_message(chat_id, '<b>Выберите раздел физики куда вы хотите добавить задачу</b>', reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['add_problem'])
def topic(message):
    bot.delete_message(message.chat.id, message.message_id)
    #bot.send_message(message.chat.id, 'включен режим добавления задач')
    generate_physics_menu(message.chat.id)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    num[0]+=1
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # сюда пишешь путь до папки где будут появляться картинки
    save_path = f'C:/Users/R1303-We2-5-Stud/Desktop/prod/images/sphoto_{section1[-1]}_{subsection1[-1]}_{diff1[-1]}_num{num[0]}.jpg'
    image.append(save_path)
    print(section1[-1], subsection1[-1], diff1[-1], task[-1], answer1[-1], image[-1])
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, 'Фотография сохранена.')
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Все верно', callback_data='да')
    no = types.InlineKeyboardButton('Редактировать', callback_data='нет')
    markup.add(yes, no)
    task_photo = open(save_path, 'rb')
    bot.send_photo(message.chat.id, task_photo,
                   caption=f'Ваша задача: {task[-1]}. \n Ответ: {answer1[-1]} ',reply_markup=markup)

num=[0]
section1 = []
subsection1 = []
diff1 = []
task = []
answer1 = []
image = ['']
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    def subsection(section, *args):
        c = 0
        buttons = []
        for i in args:
            c += 1
            buttons.append(types.InlineKeyboardButton(str(i), callback_data=f'{section}_{c}'))
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(*buttons)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, f'<b>Выберите подраздел</b>', reply_markup=markup, parse_mode='html')

    if callback.data == 'нет_фото':
        image[-1] = None
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton('Все верно', callback_data='да')
        no = types.InlineKeyboardButton('Редактировать', callback_data='нет')
        markup.add(yes, no)

        bot.send_message(callback.message.chat.id,
                       f'Ваша задача {task[-1]}. Ответ: {answer1[-1]} ', reply_markup=markup)
    if callback.data == 'да':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        conn = sqlite3.connect('физика.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO задачи (раздел, подраздел,сложность, задача, ответ, фото) VALUES (?,?,?,?,?,?)',
            (section1[-1], subsection1[-1], diff1[-1], task[-1], answer1[-1], image[-1]))

        print(section1[-1], subsection1[-1], diff1[-1], task[-1], answer1[-1])
        conn.commit()
        conn.close()

        bot.send_message(callback.message.chat.id, 'Задача успешно добавлена')
        generate_physics_menu(callback.message.chat.id)
    if callback.data == 'нет':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        #bot.send_message(callback.message.chat.id, '')
        mess = bot.send_message(callback.message.chat.id, 'Введите задачу')
        bot.register_next_step_handler(mess, task_insert)


    if callback.data == 'sect1':
        subsection('sect1', 'Кинематика', 'Динамика', 'Статика')
    if callback.data == 'sect2':
        subsection('sect2', 'Молекулярная физика', 'Изопроцессы', 'Влажность', 'Тепловые процессы')
    if callback.data == 'sect3':
        subsection('sect3', 'Электростатика', 'Электродинамика', 'Электромагнитные волны', 'Магнетизм')
    if callback.data == 'sect4':
        subsection('sect4', 'Геометрическая оптика', 'Волновая оптика')
    if callback.data == 'sect5':
        subsection('sect5', 'Квантовая механика', 'Радиоактивность', 'Специальная теория относительности')

    if callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 2:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        #print(callback.data)
        markup = types.InlineKeyboardMarkup(row_width=2)
        first = types.InlineKeyboardButton('1', callback_data=f'{callback.data}_1')
        second = types.InlineKeyboardButton('2', callback_data=f'{callback.data}_2')
        third = types.InlineKeyboardButton('3', callback_data=f'{callback.data}_3')
        fourth = types.InlineKeyboardButton('4', callback_data=f'{callback.data}_4')
        markup.add(first, second, third, fourth)

        bot.send_message(callback.message.chat.id, 'Выберите уровень сложности', reply_markup=markup)

    if callback.data.startswith('sect') and len(list(map(str, callback.data.split('_')))) == 3:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)


        #callback_subsection = str(callback.data)[:-4]
        search = callback.data.split('_')
        section = search[0]
        subsection = search[1]
        diff = search[2]
        section1.append(section)
        subsection1.append(subsection)
        diff1.append(diff)
        #print(section, subsection, diff)
        mess = bot.send_message(callback.message.chat.id, 'Введите задачу')
        bot.register_next_step_handler(mess, task_insert)




def task_insert(message):
    task.append(message.text)
    bot.send_message(message.chat.id, "Введите ответ к задаче")
    bot.register_next_step_handler(message, ans)


def ans(message):
    answer1.append(message.text)

    markup = types.InlineKeyboardMarkup(row_width=1)
    image = types.InlineKeyboardButton('Фото не прилагается', callback_data='нет_фото')
    markup.add(image)
    bot.send_message(message.chat.id, "Отправьте фото к задаче, если оно прилагается", reply_markup=markup)

    #bot.register_next_step_handler(message, photo)



#def check(message):




bot.polling(none_stop = True)
