import japanize_kivy
import time
import threading
import string
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

Builder.load_file('main.kv')
Builder.load_file('home.kv')
Builder.load_file('howto.kv')
Builder.load_file('gamekv.kv')

class HomeScreen(Screen):
    pass
 
class HowtoScreen(Screen):
    pass

class GameScreen(Screen):

	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.game_init()

	def game_init(self):
		Clock.schedule_once(self.update_stringboxes, 0.01)
		self.CHANCE = 6
		self.LENGTH = 5
		self.xindex = self.yindex = 0
		self.gameover = False
		self.app = App.get_running_app()

		# 文字の背景色などを格納するリスト
		self.pressed_strings = [['', self.app.blank_color] for i in range(self.CHANCE * self.LENGTH)]

		# キーボードの色を格納する辞書
		self.keyboard_colors = {}
		for alpha in list(string.ascii_uppercase):
			self.keyboard_colors[alpha] = self.app.keyboard_default_color

		# ゲームクラスのインスタンス生成
		import game
		self.game = game.Game(self.CHANCE, self.LENGTH)

	def update_stringboxes(self, dt = None):
		# stringboxesの再描画
		self.ids.stringboxes.clear_widgets()
		self.ids.stringboxes.cols = self.LENGTH
		for i in range(self.CHANCE * self.LENGTH):
			self.ids.stringboxes.add_widget(StringBox(
				text = str(self.pressed_strings[i][0]),
				color = (0, 0, 0, 1) if self.pressed_strings[i][1]==self.app.blank_color else (1, 1, 1, 1),
				background_color = self.pressed_strings[i][1]
			))

	def update_keyboard(self):
		for key, value in self.keyboard_colors.items():
			self.ids[key].background_color = value

	def update(self):
		self.update_stringboxes()
		self.update_keyboard()

	def string_pressed(self, text):
		if self.xindex == self.LENGTH or self.gameover == True:
			return

		self.pressed_strings[self.LENGTH * self.yindex + self.xindex][0] = text
		self.xindex += 1
		self.update()

	def enter_pressed(self):
		if self.gameover == True:
			return

		if self.xindex == self.LENGTH:
			strings = [row[0] for row in self.pressed_strings[self.LENGTH * self.yindex:self.LENGTH * self.yindex + self.LENGTH]]
			if ''.join(strings) in self.game.get_words():
				# 文字の位置チェック
				count = index = 0
				for i in range(self.LENGTH * self.yindex, self.LENGTH * self.yindex + self.LENGTH):
					if strings[index] == list(self.game.get_word())[index]:
						# 文字と位置が両方正しい
						count += 1
						self.pressed_strings[i][1] = self.app.correct_color
						self.keyboard_colors[strings[index]] = self.app.correct_color
					elif strings[index] in self.game.get_word():
						# 文字は合っているが位置が正しくない
						self.pressed_strings[i][1] = self.app.close_color
						if self.keyboard_colors[strings[index]] != self.app.correct_color:
							self.keyboard_colors[strings[index]] = self.app.close_color
					else:
						# 両方正しくない
						self.pressed_strings[i][1] = self.app.miss_color
						if self.keyboard_colors[strings[index]] == self.app.keyboard_default_color:
							self.keyboard_colors[strings[index]] = self.app.miss_color

					index += 1

				if count == self.LENGTH:
					self.gameover = True
					self.ids.resultlabel.text = '正解です!'
					self.update()
					return

				self.xindex = 0
				self.yindex += 1

				if self.yindex == self.CHANCE:
					self.ids.resultlabel.text = self.game.get_word()

			else:
				messagethread = threading.Thread(target=self.flash_message, args=('単語リストにありません',))
				messagethread.start()

			self.update()

	def back_pressed(self):
		if self.xindex == 0 or self.gameover == True:
			return

		self.xindex -= 1
		self.pressed_strings[self.LENGTH * self.yindex + (self.xindex)][0] = ''
		self.update()

	def restart(self):
		self.game_init()
		self.ids.resultlabel.text = ''
		self.update()

	def flash_message(self, text):
		self.ids.resultlabel.text = text
		time.sleep(2)
		self.ids.resultlabel.text = ''

class StringBox(Button):
	pass

class NavigationBar(BoxLayout):
	pass

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super(Manager, self).__init__(**kwargs)
		self.transition = NoTransition()

class GameApp(App):
	navigation_active_color = ListProperty([0, 1, 0, 1])
	correct_color = ListProperty([0, .5, 0, 1])
	close_color = ListProperty([.8, .8, 0, 1])
	miss_color = ListProperty([.5, .5, .5, 1])
	keyboard_default_color = ListProperty([.75, .75, .75, 1])
	blank_color = ListProperty([1, 1, 1, 1])

	def __init__(self, **kwargs):
		super(GameApp, self).__init__(**kwargs)
		self.title = 'Wordle'
 
	def build(self):
		return NavigationBar()

if __name__ == '__main__':
    GameApp().run()