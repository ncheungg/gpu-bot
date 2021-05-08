# read proxies
f = open("proxies.txt", "r")
PROXIES = [line.split("\n")[0] for line in f.readlines()]
f.close()

# read links
f = open("links.txt", "r")
LINKS = [line.split("\n")[0] for line in f.readlines() if line[0] not in ["#", "\n"]]
f.close()