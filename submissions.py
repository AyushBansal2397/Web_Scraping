from bs4 import BeautifulSoup as bs
import requests as req
from tkinter import *
from colorama import Fore, Style
import matplotlib.pyplot as plt

root = Tk()
root.title("CodeForces")
root.geometry("300x60+"+str(int(root.winfo_screenwidth()/2-150))+"+"
	+str(int(root.winfo_screenheight()/2-30)))
name_entry = Entry(root)

def get_crap(event):
	if name_entry.get() != "":
		fetch(name_entry.get())

#GUI Part
def GUI():
	name = Label(root, text="Handle :")
	button = Button(root, text="Fetch")
	name.grid(row=0, column=0, pady=2, padx=2, sticky=E)
	name_entry.grid(row=0, column=1)
	button.grid(row=1, column=1, columnspan=2)
	button.bind("<Button-1>", get_crap)
	root.mainloop()

# Fetching Part
def fetch(Handle):
	root.destroy()
	summary = {
		"Compilation" : 0,
		"Runtime" : 0,
		"Wrong" : 0,
		"Accepted" : 0,
		"Time" : 0
	}
	url = "https://codeforces.com/submissions/" + Handle + "/page/"
	source = req.get(url + "1")
	soup = bs(source.text, "lxml")
	no = len(soup.find_all("span", class_="page-index"))
	page_no = i = 1
	while page_no <= no:
		source = req.get(url + str(page_no))
		soup = bs(source.text, "lxml")
		table = soup.find_all("tr")
		page_no = page_no + 1
		for tag in range(26, len(table)-1):
			required = table[tag].find_all("td", class_="status-small")
			contest_name = required[1].a.text.strip()
			try:
				result = required[2].span.span.text
			except:
				result = required[2].span.text
			result = result.split(" ")
			length = len(result)
			if length == 1:
				print(Fore.GREEN + str(i) + " : " + contest_name)
			if length == 2:
				print(Fore.CYAN + str(i) + " : " + contest_name)
			if length == 6:
				print(Fore.BLUE + str(i) + " : " + contest_name)
			if length == 5:
				if result[0] == "Wrong":
					print(Fore.RED + str(i) + " : " + contest_name)
				else:
					print(Fore.WHITE + str(i) + " : " + contest_name)
			summary[result[0]] += 1
			print(Style.RESET_ALL, end="")
			i = i + 1

	plt.axis("equal")
	plt.pie(summary.values(), labels=summary.keys(), autopct=None)
	plt.show()

if __name__ == '__main__':
	GUI()