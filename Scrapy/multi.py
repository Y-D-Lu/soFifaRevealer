from scrapy import cmdline
from multiprocessing import Pool


def multi_task(name,version,op):
    cmdline.execute(("scrapy crawl "+op+" -a ver="+version).split())


def getPlayersInfo():
    p.apply_async(multi_task, args=(i, ver_list[i],"fifa"))


def getPlayers():
    p.apply_async(multi_task, args=(i, ver_list[i],"check"))


if __name__=='__main__':
    p = Pool(8)
    path = "ver_list.txt"
    f = open(path)  # read from version list

    lines = f.readlines()
    ver_list = []
    for ver in lines:
        ver_list.append(ver)
    f.close()

    # a switcher should be here to decide which function should be called
    for i in range(len(ver_list)):
        getPlayersInfo()
    p.close()
    p.join()
