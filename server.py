import sqlite3
from newsapi import NewsApiClient
from flask import Flask, request
newsapi = NewsApiClient(api_key='')
app = Flask(__name__)
class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()
    def get_users(self, status = True):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `users` WHERE `status` = ?', (status,)).fetchall()
    def users_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    def add_users(self, user_id, status = True):
        with self.connection:
            return self.cursor.execute('INSERT INTO `users` (`user_id`, `status`) VALUES(?,?)', (user_id,status))
    def update_users(self, user_id, status):
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `status` = ? WHERE `user_id` = ?', (status, user_id))
    def get_key(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT key FROM `keywords` WHERE `user_id` = ?', (user_id,)).fetchall()
    def key_exists(self, user_id, key):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `keywords` WHERE `user_id` = ? AND `key` = ?', (user_id, key)).fetchall()
            return bool(len(result))
    def add_key(self, user_id, key):
        with self.connection:
            return self.cursor.execute('INSERT INTO `keywords` (`user_id`, `key`) VALUES(?,?)', (user_id,key))
    def del_key(self, user_id, key):
        with self.connection:
            result = self.cursor.execute('DELETE FROM `keywords` WHERE `user_id` = ? AND `key` = ?', (user_id, key)).fetchall()
            return bool(len(result))
    def get_categ(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT name FROM `categories` WHERE `user_id` = ?', (user_id,)).fetchall()
    def categ_exists(self, user_id, name):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `categories` WHERE `user_id` = ? AND `name` = ?', (user_id, name)).fetchall()
            return bool(len(result))
    def add_categ(self, user_id, name):
        with self.connection:
            return self.cursor.execute('INSERT INTO `categories` (`user_id`, `name`) VALUES(?,?)', (user_id,name))
    def del_categ(self, user_id, name):
        with self.connection:
            result = self.cursor.execute('DELETE FROM `categories` WHERE `user_id` = ? AND `name` = ?', (user_id, name)).fetchall()
            return bool(len(result))
    def close(self):
        self.connection.close()
base = SQLighter('base.db')
@app.route('/users/<userid>', methods=['POST', 'DELETE'])
def subscribe_unsubscribe(userid):
    if request.method == 'POST':
        if (not base.users_exists(userid)):
            base.add_users(userid)
            return 'Вы успешно подписались на рассылку'
        else:
            base.update_users(userid, True)
            return 'Вы успешно подписались на рассылку'
    if request.method == 'DELETE':
        if (not base.users_exists(userid)):
            base.add_users(userid, False)
            return 'Вы небыли подписаны'
        else:
            base.update_users(userid, False)
            return 'Вы успешно отписаны от рассылки'
@app.route('/keywords/<userid>/', methods=['POST'])
def keynone(userid):
    if request.method == 'POST':
        return 'Пустое поле, введите ключевое слово через пробел после команды'
@app.route('/keywords/<userid>/', methods=['DELETE'])
def keynonedel(userid):
    if request.method == 'DELETE':
        return 'Пустое поле, введите ключевое слово через пробел после команды'
@app.route('/keywords/<userid>/<keyw>', methods=['POST', 'DELETE'])
def keyoptions(userid, keyw):
    if request.method == 'POST':
        if keyw != '':
            if (not base.key_exists(userid, keyw)):
                base.add_key(userid, keyw)
                return 'Вы успешно подписались на ключевое слово' + ' ' + '"' + keyw + '"'
            else:
                return 'Вы уже подписаны на ключевое слово' + ' ' + '"' + keyw + '"'
        else:
            return 'Недопустимое название для ключевого слова'
    if request.method == 'DELETE':
        if (not base.key_exists(userid, keyw)):
            return 'Вы небыли подписаны на ключевое слово' + ' ' + '"' + keyw + '"'
        else:
            base.del_key(userid, keyw)
            return 'Вы успешно отписаны от ключевого слова' + ' ' + '"' + keyw + '"'
@app.route('/keywords/<userid>', methods=['GET'])
def keyshow(userid):
    if request.method == 'GET':
        a = 'Список ключевых слов в подписке:'
        inp = base.get_key(userid)
        for i in range(len(inp)):
            inp2 = str(inp[i])
            a += '\n' + inp2[2:-3]
        return (a)
@app.route('/categories/<userid>/', methods=['POST'])
def categnone(userid):
    if request.method == 'POST':
        return 'Пустое поле, введите категорию через пробел после команды\nПопробуйте:\nbusiness\nentertainment\ngeneral\nhealth\nscience\nsports\ntechnology'
@app.route('/categories/<userid>/', methods=['DELETE'])
def categnonedel(userid):
    if request.method == 'DELETE':
        return 'Пустое поле, введите категорию через пробел после команды'
@app.route('/categories/<userid>/<kateg>', methods=['POST', 'DELETE'])
def categoptions (userid, kateg):
    if request.method == 'POST':
        if kateg in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
            if (not base.categ_exists(userid, kateg)):
                base.add_categ(userid, kateg)
                return 'Вы успешно подписались на категорию' + ' ' + '"' + kateg + '"'
            else:
                return 'Вы уже подписаны на категорию' + ' ' + '"' + kateg + '"'
        else:
            return 'Недопустимое название для категории\nПопробуйте:\nbusiness\nentertainment\ngeneral\nhealth\nscience\nsports\ntechnology'
    if request.method == 'DELETE':
        if (not base.categ_exists(userid, kateg)):
            return 'Вы небыли подписаны на категорию' + ' ' + '"' + kateg + '"'
        else:
            base.del_categ(userid, kateg)
            return 'Вы успешно отписаны от категории' + ' ' + '"' + kateg + '"'
@app.route('/categories/<userid>', methods=['GET'])
def categshow(userid):
    if request.method == 'GET':
        a = 'Список категорий в подписке:'
        inp = base.get_categ(userid)
        for i in range(len(inp)):
            inp2 = str(inp[i])
            a += '\n' + inp2[2:-3]
        return (a)
@app.route('/newsc/<userid>', methods=['GET'])
def newsc(userid):
    if request.method == 'GET':
        inp = base.get_categ(userid)
        s = []
        for i in range(len(inp)):
            inp2 = str(inp[i])[2:-3]
            top_headlines = newsapi.get_top_headlines(category=inp2)
            sources = newsapi.get_sources()
            s.append('Топ 10 новостей по категории' + ' ' + '"' + inp2 + '"' + ':')
            for i in range(10):
                newstext = (top_headlines['articles'][i])
                a = newstext['title']
                b = newstext['url']
                s.append(b)
                s.append(a)
        return str(s)
@app.route('/newsk/<userid>', methods=['GET'])
def newsk(userid):
    if request.method == 'GET':
        inp = base.get_key(userid)
        s = []
        for i in range(len(inp)):
            inp2 = str(inp[i])[2:-3]
            all_articles = newsapi.get_everything(q= inp2, sort_by='relevancy')
            sources = newsapi.get_sources()
            s.append('Топ 10 новостей по ключевому слову' + ' ' + '"' + inp2 + '"' + ':')
            while True:
                try:
                    for i in range(10):
                        newstext = (all_articles['articles'][i])
                        a = newstext['title']
                        b = newstext['url']
                        s.append(b)
                        s.append(a)
                    break
                except IndexError:
                    s.append('Мало новостей по данному ключевому слову')
                    break
        return str(s)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)



