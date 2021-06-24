from aiogram import Bot, Dispatcher, executor, types
import requests
tok = ''
bot = Bot(token = tok)
dp = Dispatcher(bot)
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.post(domen + 'users/' + b).text)
    await message.answer(a)
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.delete(domen + 'users/' + b).text)
    await message.answer(a)
@dp.message_handler(commands=['addk'])
async def subscribek(message: types.Message):
    keyw = ((message.text)[6:]).strip()
    b = str(message.from_user.id)
    a = str(requests.post(domen + 'keywords/' + b + '/' + keyw).text)
    await message.answer(a)
@dp.message_handler(commands=['delk'])
async def unsubscribek(message: types.Message):
    keyw = ((message.text)[6:]).strip()
    b = str(message.from_user.id)
    a = str(requests.delete(domen + 'keywords/' + b + '/' + keyw).text)
    await message.answer(a)
@dp.message_handler(commands=['showk'])
async def showk(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.get(domen + 'keywords/' + b).text)
    await message.answer(a)
@dp.message_handler(commands=['addc'])
async def subscribec(message: types.Message):
    kateg = ((message.text)[6:]).strip()
    b = str(message.from_user.id)
    a = str(requests.post(domen + 'categories/' + b + '/' + kateg).text)
    await message.answer(a)
@dp.message_handler(commands=['delc'])
async def unsubscribec(message: types.Message):
    kateg = ((message.text)[6:]).strip()
    b = str(message.from_user.id)
    a = str(requests.delete(domen + 'categories/' + b + '/' + kateg).text)
    await message.answer(a)
@dp.message_handler(commands=['showc'])
async def showc(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.get(domen + 'categories/' + b).text)
    await message.answer(a)
@dp.message_handler(commands=['newsc'])
async def newsc(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.get(domen + 'newsc/' + b).text)
    f = eval(a)
    for i in range(len(f)):
        if (f[i])[:28] == 'Топ 10 новостей по категории':
            await message.answer(f[i])
        if (f[i])[:7] == 'https:/' or (f[i])[:7] == 'http://':
            await message.answer('<a href="{}">{}</a>'.format(f[i], f[i+1]), parse_mode='html')
@dp.message_handler(commands=['newsk'])
async def newsk(message: types.Message):
    b = str(message.from_user.id)
    a = str(requests.get(domen + 'newsk/' + b).text)
    f = eval(a)
    for i in range(len(f)):
        if (f[i])[:34] == 'Топ 10 новостей по ключевому слову':
            await message.answer(f[i])
        if (f[i])[:7] == 'https:/' or (f[i])[:7] == 'http://':
            await message.answer('<a href="{}">{}</a>'.format(f[i], f[i+1]), parse_mode='html')
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать в новостной бот\nИспользуйте подсказки в команде /help')
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('/subscribe - Подписаться на бота\n/addk text - Подписаться на ключ.слово text\n/delk text'
' - Отписаться от ключ.слова text\n/showk - Посмотреть подписки на ключ.слова\n/addc text - Подписаться на категорию'
' text\n/delc text - Отписаться от категории text\n/showc - Посмотреть подписки на категории\n/newsk - Получить 10 '
'свежих новостей для каждого ключ.слова\n/newsc - Получить 10 релевантных новостей для каждой категории\n/unsubscribe '
'- Отписаться от бота')
executor.start_polling(dp, skip_updates=True)