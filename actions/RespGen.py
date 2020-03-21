import random


class RespGen:
    def __init__(self):
        self.bot = None
        self.map = {}
        # load responses
        with open('words.txt', "r", encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                titles = lines[i].strip().split('/')
                i += 1
                resps = []
                while len(lines[i].strip()) > 0:
                    resps.append(lines[i].strip())
                    i += 1
                for t in titles:
                    self.map[t] = resps

                while i < len(lines) and len(lines[i].strip()) <= 0:
                    i += 1

        self.li = []
        with open('', "r", encoding='utf-8') as file:
            lines = file.readlines()
            for l in lines:
                l = l.strip()
                if len(l) == 0:
                    continue
                self.li.append(l)

        self.possibles = self.map.keys()

    def getResp(self, ques: str, userID: str):
        rsp = self.bot.getAnws(ques, userID)
        if len(rsp) > 0:
            return rsp

        keyword = None
        for match in self.possibles:
            if match in ques:
                keyword = match
                break
        rsp = self.map.get(keyword)
        if (rsp is not None):
            chosen = random.randint(0, len(rsp) - 1)
            return rsp[chosen]

        chosen = random.randint(0, len(self.li) - 1)
        return self.li[chosen]


if __name__ == '__main__':
    r = RespGen()
    rsp = r.getResp("你叫什么呢", 1000)
    print(rsp)