from config import LINKS, PROXIES
import requests
from bs4 import BeautifulSoup
import traceback
from time import sleep
from threading import Thread, Semaphore
from queue import Queue
from win10toast import ToastNotifier
import webbrowser
import os
import random


# safe print for multithreaded processes
screenlock = Semaphore(value=1)
def safePrint(s):
    screenlock.acquire()
    print(s)
    screenlock.release()
    

class ScannerBot:
    def __init__(self, links, proxies, numOfThreads=2):
        self.links = links
        self.proxies = proxies
        self.numOfThreads = numOfThreads
        self.queue = Queue()
        self.toaster = ToastNotifier()
        self.headers = {
            "User-Agent": "PostmanRuntime/7.26.10",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }

        self.initThreads()

    def initThreads(self):
        for _ in range(self.numOfThreads):
            t = Thread(target=self.threadWorker)
            t.start()

    def alert(self, link):
        def openUrl():
            command = "echo " + link + "| clip"
            os.system(command)
            webbrowser.open(link)

        safePrint("GPU IN STOCK: " + link)
        self.toaster.show_toast("GPU IN STOCK", link, threaded=True, duration=10, callback_on_click=openUrl)

    def scanCanadaComputers(self, link):
        # proxy = random.choice(self.proxies)
        # proxies = {
        #     "https": "https://" + proxy
        # }

        res = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        arr = soup.find("div", class_="pi-prod-availability").find_all("span")
        arr = [x.get_text().strip() for x in arr]

        if arr[0] != "Not Available Online" or arr[1] != "In-Store Out Of Stock":
            self.alert(link)
        else:
            safePrint("Unavailable: " + link)

    def scanMemoryExpress(self, link):
        res = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        val = soup.find("div", class_="c-capr-inventory__availability").find("span").get_text().strip()

        if val != "Out of Stock":
            self.alert(link)
        else:
            safePrint("Unavailable: " + link)

    def scanBestBuy(self, link):
        res = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        arr = soup.find_all("span", class_="availabilityMessage_ig-s5")
        arr = [x.get_text().strip() for x in arr]

        if len(arr) == 1 and (arr[0] != "Sold out online"):
            self.alert(link)
        elif len(arr) == 2 and ((arr[0] not in ["Coming soon", "Sold out online"]) or arr[1] != "Unavailable for store pickup"):
            self.alert(link)
        else:
            safePrint("Unavailable: " + link)

    def scanNewegg(self, link):
        res = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(res.text, "html.parser")

        val = soup.find("div", class_="product-inventory").find("strong").get_text().strip()

        if val != "OUT OF STOCK.":
            self.alert(link)
        else:
            safePrint("Unavailable: " + link)

    def threadWorker(self):
        while True:
            link = self.queue.get()

            if link is None:
                break

            try:
                if "canadacomputers" in link:
                    self.scanCanadaComputers(link)
                elif "memoryexpress" in link:
                    self.scanMemoryExpress(link)
                elif "newegg" in link:
                    self.scanNewegg(link)
                elif "bestbuy" in link:
                    self.scanBestBuy(link)

                self.queue.task_done()

            except Exception as err:
                print(err)
                traceback.print_exc(file=open("errors.txt", "a"))
                print("", file=open("errors.txt", "a"))

    def run(self):
        random.shuffle(self.links)

        for link in self.links:
            self.queue.put(link)
    
    def scanLoop(self):
        while True:
            print("Scanning: ")
            self.run()

            sec = 180 + random.randint(-5, 5)
            sleep(sec)
            print("\n\n\n")
    
    def scanOnce(self):
        self.run()

        # terminates each thread
        for _ in range(self.numOfThreads):
            self.queue.put(None)


if __name__ == "__main__":
    bot = ScannerBot(LINKS, PROXIES, numOfThreads=10)

    bot.scanLoop()
    # bot.scanOnce()
