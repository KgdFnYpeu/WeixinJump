
import os #命令行模块
import threading #线程模块
import time #
import math
from PIL import Image
from PIL import ImageFilter

# print("hello")

def shell(command):
	return os.system(command)
phoneFile="/sdcard/screencap/1.png"
file="1.png"
phoneWidth = 1080
phontHeight=1920
startX=240
startY=340
resize=1

manTopRgb=(52,53,56)
manBottomRgb = (54,61,99)
def getScreencap():
	while True:
		startTime= time.time()
		shell("adb shell screencap -p "+phoneFile)
		shell("adb pull "+phoneFile+" ./"+file) #获取屏幕截图
		print("screencap ------%s"% (time.time()-startTime))
		startTime=time.time()
		im = Image.open(file)
		width,height = im.size

		# im = im.resize((width//resize,height//resize))
		r,g,b,a = im.split()
		im = Image.merge("RGB", (r,g,b))
		# im = r.filter(ImageFilter.CONTOUR) # 滤波

		bgRGB=im.getpixel((739,1600))
		# print(bgRGB)
		if bgRGB==(255,255,255):
			print("-------游戏结束--------")
			return
		
		boxX,boxY=getBoxXy(im)
		manX,manY=getManXy(im)
		addPoint(im,boxX,boxY,(255,255,255)) #白
		addPoint(im,manX,manY,(0,0,0)) # 黑 454 206

		im.show()
		print("getBoxXy %s %s" %(boxX,boxY))
		print("getManBottom %s %s" %(manX,manY))

		distance = math.sqrt(math.pow(boxX-manX,2)+math.pow(boxY-manY,2))
		t=getTime(distance)# 长按时间，根据距离算出
		print("距离 %f 时间=%f runTime=%s" % (distance,t,time.time()-startTime))
		longPress(t)
		startTime = time.time()

		# print("the curent thrading %s is running,scrreen %f time" % (threading.current_thread().name,time.time()-startTime))
		time.sleep(1) #单位s
		im.close()
		print("run------%s"% (time.time()-startTime))
		# return

def getTime(distance):
	 # 时间=距离/速度
	return (int)(distance/0.65)

def getSleepTime(distance):
	 # 时间=距离/速度
	return (int)(distance/0.3)

def getBoxXy(im):
	topX=0;
	topY=0;

	width,height = im.size
	bgRGB=im.getpixel((startX,startY))

	for y in range(startY,height-10):
		if topX!=0:
			rgb=im.getpixel((topX,y))
			# print("y= %d rgb=%s" % (y,rgb))
			if isSameColor(bgRGB,rgb):
				endY=y;

				print("新目标的最顶点（%d,%d）最低点（%d,%d）rgb=%s" % (topX,topY,topX,endY,rgb))
				addPoint2(im,topX,topY)
				addPoint2(im,topX,endY)
				boxHeight=endY-topY #新盒子的高
				return topX,topY+boxHeight//2
			continue
		for x in range(startX,width-10):
			rgb=im.getpixel((x,y))
			if not isSameColor(bgRGB,rgb): # 新目标的最顶点
				topX=x
				topY=y
				# print("newStartX=%d x=%d,y=%d rgb=%s" % (topX,x,y,rgb))
				break
	return 0,0

def getManXy(im):
	startY=1575
	startX=940
	rightX=0
	leftX=0
	width,height = im.size
	isStart=False
	for y in range(startY,10,-1): #step 为2，运算更快
		for x in range(startX,10,-1):
			r,g,b= im.getpixel((x,y))
			# print(" X=%s y=%s rgb=%s %s %s" %(x,y,r,g,b))
			if not isStart and isManColor(manBottomRgb[0],r) and isManColor(manBottomRgb[1],g) and isManColor(manBottomRgb[2],b):
				rightX =x
				isStart=True
			elif isStart and not (isManColor(manBottomRgb[0],r) or isManColor(manBottomRgb[1],g) or isManColor(manBottomRgb[2],b)):
				leftX=x
				# print("rightX =%s leftX=%s y=%s" %(rightX,leftX,y))
				return (rightX+leftX)//2,y
	return 0,0

#是否为同一颜色
def isSameColor(color1,color2):
	return isColor(color1[0],color2[0]) and isColor(color1[1],color2[1]) and isColor(color1[2],color2[2])

def isColor(color1,color2):
	return abs(color1-color2)<=20

def isManColor(color1,color2):
	return abs(color1-color2)<=5


def addPoint2(im,boxX,boxY):
	rgb=(255,255,255)

	minX=boxX
	if boxX>=5: minX = boxX
	minY =boxY
	if boxY>=5:minY=boxY-5
	for x in range(minX,boxX+5):
		im.putpixel((x,boxY),rgb)
	for y in range(minY,boxY+5):
		im.putpixel((boxX,y),rgb)

def addPoint1(im,boxX,boxY):
	rgb=(255,255,255)
	im.putpixel((boxX,boxY),rgb)

def addPoint(im,boxX,boxY,rgb):
	minX=boxX
	if boxX>=5: minX = boxX
	minY =boxY
	if boxY>=5:minY=boxY-5
	for x in range(minX,boxX+5):
		for y in range(minY,boxY+5):
			im.putpixel((x,y),rgb)

def longPress(time):
	shell("adb shell input swipe 100 100 100 100 %d" % time) #长按点


# print("the curent thrading %s is running" % (threading.current_thread().name))
getScreencap()
screenThread = threading.Thread(target=getScreencap)
# screenThread.start()
