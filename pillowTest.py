
from PIL import Image
from PIL import ImageFilter

file="1.png"

im = Image.open(file)
print(im.format,im.size,im.mode)
		# im.show()
box = (100,100,300,300)
region = im.crop(box)#切割指定区域，左上角开始
region.save("score.png")
		# region.show()
		# im.show()

		# out =im.resize((size[0]//10,size[1]//10))#压缩图片size
out=im.rotate(45) #旋转
out = im.transpose(Image.ROTATE_90) #旋转
		# out = im.convert("L") #色彩转换
		# out.show()

		# outF = im.filter(ImageFilter.DETAIL)
conF = im.filter(ImageFilter.CONTOUR)
edgeF = im.filter(ImageFilter.FIND_EDGES) # 滤波
		# outF.show()
conF.show()
conF.save("contour.png")
edgeF.show()
edgeF.save("edges.jpg")