import japanize_kivy
from kivy.app import App
from kivy.uix.label import Label

class GameApp(App):

	def __init__(self, **kwargs):
		super(GameApp, self).__init__(**kwargs)
		self.title = 'Wordle'
 
	def build(self):
		return Label(text='Wordle')

if __name__ == '__main__':
    GameApp().run()