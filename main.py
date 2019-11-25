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
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.clock import Clock
import data_manage
import datetime
import os
import kivy
Window.clearcolor = (.2, .27, .5, 1)
dir_path = os.path.dirname(os.path.realpath(__file__))
db_file=dir_path+"\\notes.db"
data_manage.initialize_note_table(db_file)
print('made with kivy version 1.11.1')


class Note_card(Button):
	note_id=NumericProperty()
	note_title=StringProperty()
	note_content=StringProperty()
	note_date=StringProperty()

	def __init__(self,**kwargs):
		super(Note_card,self).__init__(**kwargs)
		self.text=str(self.note_title)
		self.background_color=(0,1,0,.5)
		
		
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
        # The touch has occurred inside the widgets area. Do stuff!
			notes_screen=self.parent.parent.parent.parent.parent.get_screen('notes')
			notes_screen.note_id=self.note_id
			iden=notes_screen.ids
			iden.note_title.text=self.note_title
			iden.note_content.text=self.note_content
			iden.note_content.scroll_y=0
			self.parent.parent.parent.parent.manager.current='notes'
			
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
			
		
		for i in entry_list:
			btn=Note_card(note_id=str(i[0]),note_title=str(i[1]),note_content=str(i[2]),note_date=str(i[3]),size_hint_y=None,height=40)
			layout.add_widget(btn)

		self.add_widget(layout)
		

class Delete_card(Button):
	note_id=NumericProperty()
	note_title=StringProperty()
	note_content=StringProperty()
	note_date=StringProperty()
	deletion_status=BooleanProperty()

	def __init__(self,**kwargs):
		super(Delete_card,self).__init__(**kwargs)
		self.text=str(self.note_title)
		self.background_color=(0,1,0,.5)
		self.deletion_status=False
		
		
	def on_touch_down(self,touch):
		if self.collide_point(*touch.pos):
        # The touch has occurred inside the widgets area. Do stuff!
			queue=[]
			del_screen=self.parent.parent.parent.parent
			
			print(del_screen)
			if self.deletion_status==False:
				queue.append(self.note_id)
				del_screen.items_to_delete.append(self.note_id)
				self.deletion_status=True
				self.background_color=(1,0,0,.5)
			else:
				self.deletion_status=False
				self.background_color=(0,1,0,.5)
				print("Button id is: "+str(self.note_id))
				del_screen.items_to_delete.remove(self.note_id)

				
			

		
			
			pass

	pass

class Delete_scroll(ScrollView):
	def __init__(self,**kwargs):
		super(Delete_scroll,self).__init__(**kwargs)
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
			
		
		for i in entry_list:
			btn=Delete_card(note_id=str(i[0]),note_title=str(i[1]),note_content=str(i[2]),note_date=str(i[3]),size_hint_y=None,height=40)
			layout.add_widget(btn)

		self.add_widget(layout)
	pass



class Home(Screen):
	def make_new_note(self):
		new_note=self.manager.get_screen('notes')
		
		new_note.ids.note_title.text=''
		new_note.ids.note_content.text=''
		self.manager.current='notes'

class Delete_screen(Screen):
	items_to_delete=ListProperty()
	def cancel_delete(self):
		self.items_to_delete=[]
		self.manager.current='home'
	def complete_deletion(self):
		
		for item in self.items_to_delete:
			data_manage.delete_entry_by_id(db_file,item)
		self.ids.delete_view.update_scroll()


	pass

	
class Note(Screen):
	note_id=NumericProperty()

	def delete_self(self):
		current_id=self.note_id
		data_manage.delete_entry_by_id(db_file,current_id)
		self.manager.current='home'



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

		if old_id!=0:
			
			new_date=datetime.date.today()

			new_entry=[entry[0],entry[1],new_date,old_id]
			

			data_manage.update_tasks_table(db_file,new_entry)

		elif (entry[1] or entry[0]) != 'none':
			with data_manage.connect_to_db(db_file) as conn:

				data_manage.insert_entry_to_notes(conn,entry)

		else:
			print('none')
			note_screen=self.root.get_screen('notes')
			iden=note_screen.ids
			iden.note_title.hint_text='Write a title for your note'
			iden.note_content.hint_text='Write content for your note'


		
	

NotePadApp().run()