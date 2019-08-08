import requests as req
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.title("CodeChef Fetch")
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
	url = "https://www.codechef.com/" + contest_id
	src = req.get(url).text
	soup = bs(src, "lxml")
	rt = Tk()
	rt.withdraw()
	dirName = filedialog.askdirectory()
	dirName = dirName + "/CodeChef/" + contest_id
	rt.destroy()
	if not os.path.exists(dirName):
		os.makedirs(dirName)

	print("Fetching Problem Name")
	problem_id = []
	problems = soup.find_all("b")
	problems = [ str(i) for i in problems ]
	problems = [ i[3:len(i)-4] for i in problems ]
	problems = problems[:problems.index('Liked the Contest? Hit Like Button below.')]

	print("Fetching Problen Code")
	tbody = soup.find("table", class_="dataTable").tbody
	tr = tbody.find_all("tr")
	for i in tr:
		i = i.find_all("td")
		i = str(i[1])
		i = i[4:len(i)-5]
		problem_id.append(i)

	print("Fetching Testcases & making sinpets")
	for i in range(len(problems)):
		print("\t" + problems[i])
		url = url + "/problems/" + problem_id[i]
		pro_src = req.get(url).text
		url = "https://www.codechef.com/" + contest_id
		pro_soup = bs(pro_src, "lxml")
		
		Dir = dirName + "/" + problems[i]
		if not os.path.exists(Dir):
			os.makedirs(Dir)

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
		testcases = pro_soup.find_all("div", class_="content")[1].get_text()
		
		if "Explanation" in testcases:
			testcases = testcases.split("Explanation")[0]
		else:
			testcases = testcases.split("Scoring")[0]

		if "Example Input" in testcases:
			testcases = testcases.split("Example Input")[1]
		else:
			testcases = testcases.split("Example")[1]

		testcases = testcases.split("### Example Output")
		Str = "\n```"
		with open(Dir + "/input.txt", "w") as file:
			file.write(testcases[0].split(Str)[1])
		with open(Dir + "/output.txt", "w") as file:
			file.write(testcases[1].split(Str)[1])
		print()
	print("Fetching Completed!!")

if __name__ == '__main__':
	GUI()