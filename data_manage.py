import sqlite3
from sqlite3 import Error
import datetime
import os

def connect_to_db(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	

def create_table(conn, create_table_sql):
	try:
		c=conn.cursor()
		c.execute(create_table_sql)
		conn.commit()
	except Error as e:
		print(e)

def initialize_note_table(db_file):
	with connect_to_db(db_file) as conn:
		

		sql=""" CREATE TABLE IF NOT EXISTS notes(
		id integer PRIMARY KEY,
		note_title text NOT NULL,
		note_content text NOT NULL,
		date_written date NOT NULL
		);"""
		create_table(conn,sql)

def insert_entry_to_notes(conn,note_entry):
	sql=''' INSERT INTO notes(note_title,note_content,date_written)
	VALUES(?,?,?)'''
	cur=conn.cursor()
	cur.execute(sql,note_entry)
	conn.commit()
	
def query_notes(conn):
	cur=conn.cursor()
	cur.execute("SELECT * FROM notes")
	rows=cur.fetchall()

	return rows
def update_tasks_table(db_file,new_note):

	with connect_to_db(db_file) as conn:
		cursor=conn.cursor()
		sql_update_query=""" 
		UPDATE  notes
		SET note_title=?,
		note_content=?,
		date_written=?
		where id= ? 
		"""
		cursor.execute(sql_update_query,new_note)
		conn.commit()
