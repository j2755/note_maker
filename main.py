from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
import data_manage
import datetime
import os

Window.clearcolor = (.2, .27, .5, 1)
dir_path = os.path.dirname(os.path.realpath(__file__))
db_file=dir_path+"\\notes.db"
data_manage.initialize_note_table(db_file)



class Note_card(Button):
	note_id=NumericProperty()
	note_title=StringProperty()
	note_content=StringProperty()
	note_date=StringProperty()

	def __init__(self,**kwargs):
		super(Note_card,self).__init__(**kwargs)
		self.text=str(self.note_title)
		
		
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
        # The touch has occurred inside the widgets area. Do stuff!
			notes_screen=self.parent.parent.parent.parent.parent.get_screen('notes')
			notes_screen.note_id=self.note_id
			iden=notes_screen.ids
			iden.note_title.text=self.note_title
			iden.note_content.text=self.note_content
			
			print(notes_screen.note_id)
			pass



class Note_view(ScrollView):
	def __init__(self,**kwargs):
		super(Note_view,self).__init__(**kwargs)
		self.update_scroll()
		
	def update_scroll(self):
		for c in list(self.children):
			if isinstance(c, GridLayout):
				self.remove_widget(c)
		layout=GridLayout(cols=2, spacing=10, size_hint_y=None)
		layout.bind(minimum_height=layout.setter('height'))
		entry_list=[]
		with data_manage.connect_to_db(db_file) as conn:
			entry_list=data_manage.query_notes(conn)
		print(entry_list)
		for i in entry_list:
			btn=Note_card(note_id=str(i[0]),note_title=str(i[1]),note_content=str(2),note_date=str(i[3]),size_hint_y=None,height=40)
			layout.add_widget(btn)

		self.add_widget(layout)
		





class Home(Screen):
	pass
	

	
class Note(Screen):
	note_id=NumericProperty()



	pass

class ScreenManagement(ScreenManager):
	pass


presentation=Builder.load_file("NotePad.kv")

class NotePadApp(App):

	def build(self):
		return presentation

	def get_note_info(self):
		note_screen=self.root.get_screen('notes')
		iden=note_screen.ids
		n_title=iden.note_title.text
		n_content=iden.note_content.text
		n_id=note_screen.note_id
		if (n_title or n_content)=='':
			n_title='none'
			n_content='none'
		date_of_submission=datetime.date.today()

		entry=[n_title,n_content,date_of_submission]
		return entry

	def submit(self):
		entry=self.get_note_info()
		note_screen=self.root.get_screen('notes')
		old_id=note_screen.note_id

		if old_id!=None:
			
			new_date=datetime.date.today()
			new_entry=[entry[0],entry[1],new_date,old_id]

			data_manage.update_tasks_table(db_file,new_entry)

		elif (entry[1] or entry[2]) != 'none':
			with data_manage.connect_to_db(db_file) as conn:

				data_manage.insert_entry_to_notes(conn,entry)

		else:
			print('none')
			note_screen=self.root.get_screen('notes')
			iden=note_screen.ids
			iden.note_title.hint_text='Write a title for your note'
			iden.note_content.hint_text='Write content for your note'

		
		
	

NotePadApp().run()