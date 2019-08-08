import requests as req
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.title("CodeForces Fetch")
root.geometry("300x60+"+str(int(root.winfo_screenwidth()/2-150))+"+"
	+str(int(root.winfo_screenheight()/2-30)))
name_entry = Entry(root)

def get_crap(event):
	if name_entry.get() != "":
		fetch(name_entry.get())

#GUI Part
def GUI():
	name = Label(root, text="Contest Code :")
	button = Button(root, text="Submit")
	name.grid(row=0, column=0, pady=2, padx=2, sticky=E)
	name_entry.grid(row=0, column=1)
	button.grid(row=1, column=1, columnspan=2)
	button.bind("<Button-1>", get_crap)
	root.mainloop()

# Fetching Part
def fetch(contest_id):
	root.destroy()
	url = "https://codeforces.com/contest/" + contest_id
	src = req.get(url).text
	soup = bs(src, "lxml")
	
	rt = Tk()
	rt.withdraw()
	dirName = filedialog.askdirectory()
	dirName = dirName + "/CodeForces/" + contest_id
	rt.destroy()
	if not os.path.exists(dirName):
	    os.makedirs(dirName)

	print("Fetching Problem Name")
	problems = [ i.a.text.strip() for i in soup.find_all("td", class_="id")]

	print("Fetching Testcases & making sinpets")
	for problem in problems:
		url = "https://codeforces.com/contest/" + contest_id + "/problem/" + problem
		pro_src = req.get(url).text
		pro_soup = bs(pro_src, "lxml")
		problem_name = pro_soup.find("div", class_="title").text.split(".")[1].strip()
		Dir = dirName+ "/" + problem_name

		if not os.path.exists(Dir):
			os.makedirs(Dir)
		print("\t" + problem_name)
		print("\t\t|-Making C++, Java, Python3.6 sinpet")
		sinpet = '''#include <bits/stdc++.h>\nusing namespace std;\nint main(){\n\tcout
					<<"Hello world!" << endl;\n\treturn 0;\n}'''
		with open(Dir + "/code.cpp", "w") as file:
			file.write(sinpet)

		sinpet = 'print("Hello World")'
		with open(Dir + "/code.py", "w") as file:
			file.write(sinpet)

		sinpet = '''public class Main\n{\n\tpublic static void main(String[] args)
					{\n\t\tSystem.out.println("Hello World");\n\t}\n}'''
		with open(Dir + "/code.java", "w") as file:
			file.write(sinpet)

		print("\t\t|-Fetching Testcases")
		testcases = pro_soup.find_all("pre")
		i = 1
		a = 0
		while a < len(testcases):
			with open(Dir + "/input" + str(i) + ".txt", "w") as file:
				file.write(testcases[a].text.strip())
			with open(Dir + "/output" + str(i) + ".txt", "w") as file:
				file.write(testcases[a+1].text.strip())
			a = a + 2
			i = i + 1
		print()
	print("Fetching Completed!!")

if __name__ == '__main__':
	GUI()