import requests
from bs4 import BeautifulSoup as BS
import tkinter as tk

iskl = ("", "Мобильная версия", "Главная", "О сайте", "Частые вопросы (FAQ)", "Беларусь", "Литва", "Россия", "Украина",
        "Все страны", "Москва (ВДНХ)", "См. на карте", "Контакты", ">>>")


class Window:
    def __init__(self, links):
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title("Прагноз лучьшей погды для езгнания диавола из русичьки")
        self.check = []
        self.lbl1 = tk.Label(self.root, wraplength=800, font=("Comic sans", 14))
        self.lbl1.grid(row=0, column=0, columnspan=2)
        self.set_txt(links)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.grid(row=1, column=0, sticky="E")

        self.btn = tk.Button(self.root, text="Ищи!",command=lambda x=links:self.check_input(x))
        self.btn.grid(row=1, column=1, sticky="W")

        self.lbl2 = tk.Label(self.root, wraplength=800, font=("Comic sans", 14))
        self.lbl2.grid(row=2, column=0, columnspan=2)

    def set_txt(self, links):
        text = ""
        for city in links:
            self.check.append(city)
            text += city + ', '
        text = text[:-2]
        self.lbl1.configure(text=text)

    def check_input(self, links):
        town = self.entry.get()
        if town not in self.check:
            return
        else:
            self.parse_wthr(links[town])

    def parse_wthr(self, link):
        city_wthr = Weather(link)
        data1 = city_wthr.soup.find("div", {"id": "archiveString"})
        t = data1.find("span", {"class": "t_0"}).text
        txt = data1.find("a", {"class": "ArchiveStrLink"}).text
        if txt is None:
            txt = data1.find("div", {"class": "ArchiveInfo"}).text
        self.lbl2.configure(text=t + "\n" + txt)


class Weather:
    def __init__(self, link):
        self.link = link
        r = requests.get(self.link).text
        self.soup = BS(r, "html.parser")

    def get_cities(self):
        data = self.soup.find_all("a")
        links = {}
        for block in data:
            text = block.__str__()
            name = block.get_text()
            text = text[text.find('href="'):][6:]
            last = text.find('"')
            text = text[:last]
            if name not in iskl:
                links[name] = "https://rp5.ru" + text
        sorted_links = {key: value for key, value in sorted(links.items())}
        return sorted_links


url = "https://rp5.ru/Погода_в_России"
w = Weather(url)
data = w.get_cities()
print(data)
wndw = Window(data)
wndw.root.mainloop()
