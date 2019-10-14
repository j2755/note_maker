from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput 
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.screenmanager import ScreenManager,Screen


class Home(Screen):
	pass
	
class Other(Screen):
	pass

class ScreenManagement(ScreenManager):
	pass


presentation=Builder.load_file("NotePad.kv")

class NotePadApp(App):
	def build(self):
		return presentation
	def process(self):
		home=self.root.get_screen('home')
		text=home.ids.input.text
		print(text)
	

NotePadApp().run()