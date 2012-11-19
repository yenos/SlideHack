import urllib
import re, os
import argparse
import PIL
import random
from urllib import FancyURLopener
from HTMLParser import HTMLParser
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image

#---------------------------------------------#	
#---------------------------------------------#	
# 		More Stealthness	      #
#---------------------------------------------#	
#---------------------------------------------#	
class MyOpener(FancyURLopener):
	#Common User Agent
	USER_AGENT_TAB 	= ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1',
			   'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:12.0) Gecko/20100101 Firefox/12.0',
			   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
			   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
			   'Mozilla/5.0 (Windows NT 6.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
			   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0.1',
			   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
			   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5',
			   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0',
			   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11']
			   
	p		= random.randrange(12)

	version 	= USER_AGENT_TAB[p]
	print "\n==== User-Agent ===="
	print USER_AGENT_TAB[p]

#---------------------------------------------#	
#---------------------------------------------#	
# 		slidehack class		      #
#---------------------------------------------#	
#---------------------------------------------#	
class slidehack:

	REGEX_TAB_PIN	= 	['\"pin_image_url\":\"(//images\.slidesharecdn\.com/.*)/slide-\d+-\d+\.jpg\"',
				 '\"pin_image_url\":\"(http://m\.slidesharecdn\.com/convert\.php\?file\=.*-slide-)\d+\.jpg\"',
				'\"pin_image_url\":\"(//image\.slidesharecdn\.com/.*)/slide-\d+-\d+\.jpg\"']
	REGEX_TAB_TOT	=	['\"total_slides\":([0-9]+)']



	#---------------------------------------------#	
	# 		Get the options		      #
	#---------------------------------------------#	
	def getargs(self):
		parser = argparse.ArgumentParser(description='SlideHack is a tool to download (I hope) most of SlideShare documents unavailable to download and save it into a PDF file')
		parser.add_argument('-f','--filename', 		help="Your output pdf filename (ex : foobar.pdf)",required=True)
		parser.add_argument('-u','--url', 		help="The presentation URL (ex : http://http://www.slideshare.net/guest66dc5f/rahulanalysisofadversarialcode)",required=True)
		args = vars(parser.parse_args())
		
		fn 	= args['filename']
		url 	= args['url']

		return[fn, url]





	#---------------------------------------------#	
	# 		SlideHack Core		      #
	#---------------------------------------------#	
	def getHtmlSource(self, url):
		urlopen 	= MyOpener().open
		s 		= urlopen(url)
		htmlSource 	= s.read()
		s.close()
		return htmlSource

	def getSlideInfos(self,htmlSource):
		print "\n==== Download Rules ===="
		ok	= False
		i	= 0
		if "title=\"Download this document\"" in htmlSource:
			print "You can download this document from slideshare's website"
			p 	= re.compile('&from_source=(http://www\.slideshare\.net/\S+)\"')
			dl 	= p.findall(htmlSource)[0]
			return (1, dl)
		print "Document not available for downloading, bypassing restriction\n\n"
		print "\n==== REGEX ===="
		while not ok and i <= len(self.REGEX_TAB_PIN) :
			ok	= True
			try:
				print "Trying REGEX number "+str(i+1)
				p 	= re.compile(str(self.REGEX_TAB_PIN[i]))
				pin 	= p.findall(htmlSource)[0]
			except IndexError:
				ok	= False
				i	+= 1
			p 	= re.compile(str(self.REGEX_TAB_TOT[0]))
			tot	= p.findall(htmlSource)[0]
		print tot
		return (pin,tot,i)

	def createPDF(self, si, filename):
		urlretrieve 	= MyOpener().retrieve
		img		= ""
                UrlImage 	= ""
		if si[2] == 0 or si[2] == 2:
			img 		= "http:"+str(si[0])+"/slide-"
                        UrlImage	= img + "1-728.jpg"
		elif si[2] == 1:
                        UrlImage	= str(si[0]) + "1.jpg&big=1"
		n	= int(si[1])

		imageName	= "slide1.jpg"
		urlretrieve(UrlImage, imageName)
		width, height = PIL.Image.open(imageName).size
		ratio = float(width/height)
		height = 728
		width = int(ratio*height)
		
		doc = SimpleDocTemplate(filename, pagesize=(float(height+10), float(width+10)))
		parts = []
		parts.append(Image(imageName))
		print "\n==== Downloading ===="
		print "Downloading slide number 1/"+str(n)
		for i in range(2,n+1):
                        if si[2] == 0 or si[2] == 2:
                                UrlImage	= img + str(i) + "-728.jpg"
                                imageName	= "slide"+str(i)+".jpg"
                                print "Downloading slide number " + str(i) + "/" + str(n)
                        elif si[2] == 1:
                                UrlImage	= str(si[0]) + str(i) + ".jpg&big=1"
                                imageName	= "slide"+str(i)+".jpg"
                                print "Downloading slide number " + str(i) + "/" + str(n)
			urlretrieve(UrlImage, imageName)
			parts.append(Image(imageName))
		print "\n==== Creating " + filename + " ===="
		try:
			doc.build(parts)
		except :
			doc = SimpleDocTemplate(filename, pagesize=(1024.0,1024.0))
			doc.build(parts)
		print "> ok"
		print "\n==== Cleaning img files ===="
		for i in range(1,n+1):
			imageName	= "slide"+str(i)+".jpg"
			os.remove(imageName)
		print "> ok"
	
	#For the future
	def downloadingFile(self, url, fn):
		print "\n==== Downloading " + fn + " ===="
		urlretrieve = MyOpener().retrieve
		urlretrieve(url, fn)
		print "> ok"						


	#---------------------------------------------#	
	# 		Main Call		      #
	#---------------------------------------------#			
	def main(self):
		argTab = sh.getargs()

		sc	= sh.getHtmlSource(argTab[1])
		si	= sh.getSlideInfos(sc)
		fn	= argTab[0]
		if si[0] != 1:
			self.createPDF(si, fn)
		#else:
			#self.downloadingFile(si[1], fn)
			
		

if __name__ == "__main__":
	sh	= slidehack()
	sh.main()