# Core Pkgs
import streamlit as st 

# EDA pkg
import pandas as pd 

# Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import plotly.express as px 
from PIL import Image
import os

# Database Mgtmt
import sqlite3
conn = sqlite3.connect('userdata.db')
c = conn.cursor()

#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


@st.cache
def load_image(img):
	im = Image.open(os.path.join(img))
	return im

# Fxn
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_data(username,password):	
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data 




def main():
	"""Programming Language Search Term App"""
	
	html_temp = """
		<div style="background-color:{};padding:10px;border-radius:10px">
		<h1 style="color:{};text-align:center;">Programming Languages Trend App </h1>
		</div>
		"""
	st.markdown(html_temp.format('royalblue','white'),unsafe_allow_html=True)

	menu = ["Home","Login","SignUp","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		st.subheader("Programming Language Search Term Trend")
		st.image(load_image('imgs/different-programming-languages.png'))

		# Image

	elif choice == "Login":
		username = st.sidebar.text_input("Username")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			st.subheader("Trend App")
			create_table()
			hashed_pswd_init = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd_init))
			if result:
				st.success("Logged In as : {}".format(username))
				task = st.selectbox("Task",["Plots","Trends"])
				if task == "Plots":
					st.subheader("Data Visualization")
					# Plots
					df = pd.read_csv("data/clean_with_dates.csv",parse_dates=['Week'],index_col=['Week'])
					# st.dataframe(df)

					# All Columns
					all_columns = df.columns.tolist()
					lang_choices = st.multiselect("Choose Language",all_columns)
					new_df = df[lang_choices]

					# Line Chart
					st.line_chart(new_df)

					# Area Chart
					if st.checkbox("Area Chart"):
						all_columns = df.columns.tolist()
						prog_lang_choices = st.multiselect("Choose Programming Language",all_columns)
						new_df2 = df[prog_lang_choices]
						st.area_chart(new_df2)


					if st.checkbox("Total Count of Terms"):
						
						count_df = pd.read_csv("data/lang_sum_num_data.csv")
						st.write(count_df.plot.barh(x='lang',y='Sum'))
						st.pyplot()
						#st.set_option('deprecation.showPyplotGlobalUse', False)





				elif task == "Trends":
					st.subheader("Time Series Trends for Search Term")
					# Plotly
					df = pd.read_csv("data/clean_with_dates.csv",parse_dates=['Week'],index_col=['Week'])
					# st.dataframe(df)

					# All Columns
					all_columns = df.columns.tolist()
					lang_choices = st.multiselect("Choose Program Language",all_columns,default=["Python"])
					year_interval = st.selectbox("Select Year",["2015","2016","2017","2018","2019","2020","All"])
					if year_interval == "All":
						ts = df 
					else:
						ts = df[year_interval]
					
					# Using Plotly
					fig = px.line(ts,x=ts.index,y=lang_choices)
					st.plotly_chart(fig,use_container_width=True)

			else:
				st.warning("Incorrect Username/Password")
		

	elif choice == "SignUp":
		st.subheader("Create An Account")
		new_username = st.text_input("Username")
		new_password = st.text_input("Password",type='password')
		if st.button("Sign Up"):
			create_table()
			hashed_pswd = make_hashes(new_password)
			add_data(new_username,hashed_pswd)
			st.success("You have successfully created an Account")



if __name__ == '__main__':
	main()