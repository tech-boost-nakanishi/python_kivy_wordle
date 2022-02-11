import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

Builder.load_file('home.kv')
Builder.load_file('howto.kv')
Builder.load_file('gamekv.kv')

class HomeScreen(Screen):
    pass
 
class HowtoScreen(Screen):
    pass

class GameScreen(Screen):
	pass

class GameApp(App):

	def __init__(self, **kwargs):
		super(GameApp, self).__init__(**kwargs)
		self.title = 'Wordle'
 
	def build(self):
		self.sm = ScreenManager(transition=NoTransition())
		self.sm.add_widget(HomeScreen(name='home'))
		self.sm.add_widget(HowtoScreen(name='howto'))
		self.sm.add_widget(GameScreen(name='game'))
		return self.sm

if __name__ == '__main__':
    GameApp().run()