import re
import os
import sys
import json
import requests
import urllib.request
import pygame.mixer
from scrapy.selector import Selector

class search(): #歌单搜索歌曲ID
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url ='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_songurls(self, playlist):
        #进入歌单页面，得到歌单里每首歌的ID
        url = self.main_url +'playlist?id=%d'%playlist
        re = self.session.get(url)
        sel = Selector(text = re.text)
        songurls = sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls #所有歌曲组成的list

    def get_songinfos(self, songurls): #多首歌曲
        print("ID - 歌名 - 歌手")
        i = 0
        for songurl in songurls:
            #进入每首歌曲的页面并得到歌曲信息
            url = self.main_url + songurl
            re = self.session.get(url)
            sel = Selector(text = re.text)
            song_id = url.split('=')[1]
            song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
            singer = '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
            #打印输出
            print(song_id + " - "+ song_name + " - " + singer)
            i = i + 1
        print("该歌单共有 %d 首歌曲"%i)

    def work(self, playlist):
        songurls = self.get_songurls(playlist)
        self.get_songinfos(songurls)

    def get_songinfo(self, songurl): #单首歌曲
    	#进入歌曲页面并得到歌曲信息
    	url = self.main_url + songurl
    	re = self.session.get(url)
    	sel = Selector(text = re.text)
    	song_id = url.split('=')[1]
    	song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
    	singer = '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
    	#打印输出
    	print("ID:" + song_id + " 歌名:" + song_name + " 歌手：" + singer)

def download_song(song_ID, dir_path): #下载(缓存)音乐
    song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_ID #用歌曲ID合成url
    path = dir_path + os.sep + "cache.mp3" #文件路径
    urllib.request.urlretrieve(song_url, path)
    return True

def play_song(dir_path): #播放音乐
	path = dir_path + os.sep + "cache.mp3"
	pygame.mixer.init()
	pygame.mixer.music.load(path)
	pygame.mixer.music.play()
	i = 1
	while pygame.mixer.music.get_busy():
		pygame.time.delay(100)
		print('" "暂停/继续、"Stop"停止')
		info = input()
		if info == " ":
			if i == 1:
				pygame.mixer.music.pause()
				i = 0
			else:
				pygame.mixer.music.unpause()
				i = 1
		elif info == "stop" or "STOP" or "Stop":
			pygame.mixer.music.stop()
			pygame.mixer.music.load("Config" + os.sep + "decoupling.mp3")
			return "Stop"
	pygame.mixer.music.stop()
	pygame.mixer.music.load("Config" + os.sep + "decoupling.mp3")
	return True

if __name__ == '__main__':
    search = search()
    print("程序加载完成......")
    print("<---网易云音乐精简版（Beta 0.1.5）--->")
    while True:
    	print("1.播放在线歌曲")
    	print("2.歌单歌曲查询")
    	print("0.Exit")
    	info = input("请输入操作：")
    	if info == "1":
    		print("------")
    		print('请输入歌曲ID("0"返回)')
    		info_1 = input()
    		if info_1 == "0":
    			print("------")
    		else:
    			print("歌曲信息:")
    			songurl = "song?id=" + info_1
    			search.get_songinfo(songurl)
    			download_song(info_1, "Cache")
    			play_song("Cache")
    			print("------")
    	elif info == "2":
    		print("------")
    		print('请输入歌单ID("0"返回)')
    		info_1 = input()
    		if info_1 == "0":
    			print("------")
    		else:
    			print("歌单歌曲列表:")
    			search.work(int(info_1))
    			print("------")
    	elif info == "0":
    		sys.exit(0)