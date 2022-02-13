import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
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
	close_color = ListProperty([.9, .9, 0, 1])
	miss_color = ListProperty([.5, .5, .5, 1])

	def __init__(self, **kwargs):
		super(GameApp, self).__init__(**kwargs)
		self.title = 'Wordle'
 
	def build(self):
		return NavigationBar()

if __name__ == '__main__':
    GameApp().run()