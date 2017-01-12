#-*- coding:utf-8 -*-
import cv2
import numpy as np
import sys, os, lucene, threading, time
from bs4 import BeautifulSoup
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
#from org.apache.lucene.analysis.standard import CJKAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
import urllib


class img_search_color:
	def __init__(self,img):
		self.num = self.get_color(img)

	def get_color(self,imgs):
		(R,G,B) = cv2.split(imgs)
		R_avg = np.mean(R)
		G_avg = np.mean(G)
		B_avg = np.mean(B)
		max_val = max(R_avg, G_avg, B_avg) + 1
		R_stv = int(R_avg/max_val*10)
		G_stv = int(G_avg/max_val*10)
		B_stv = int(B_avg/max_val*10)
		if R_avg >= G_avg and R_avg >= B_avg: return 1000 + R_stv*100 + G_stv*10 + B_stv
		if G_avg >= R_avg and G_avg >= B_avg: return 2000 + R_stv*100 + G_stv*10 + B_stv
		if B_avg >= G_avg and B_avg >= R_avg: return 3000 + R_stv*100 + G_stv*10 + B_stv


class Ticker(object):

	def __init__(self):
		self.tick = True

	def run(self):
		while self.tick:
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(1.0)

class IndexFiles(object):
	"""Usage: python IndexFiles <doc_directory>"""

	def __init__(self, img_url, toi , tid):

		self.indexDocs(img_url ,toi , tid)
		ticker = Ticker()
		print('commit index')
		threading.Thread(target=ticker.run).start()
		ticker.tick = False
		print('done')

	def indexDocs(self,img_url ,toi , tid ):

		try:
			t1 = FieldType()
			t1.setIndexed(True)
			t1.setStored(True)
			t1.setTokenized(True)
			t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

			print("Adding", img_url)
			name = "Pictures/1.jpg"
			conn = urllib.urlopen(img_url)
			f = open(name,'wb')
			f.write(conn.read())
			f.close()
			img = cv2.imread(name)
			sdf = img_search_color(img)
			storeDir = 'Picture/' + str(sdf.num)
			if not os.path.exists(storeDir):
				os.mkdir(storeDir)
			cv2.imwrite(storeDir+'/'+str(toi)+'___'+str(tid)+'.jpg',img)
			storeDir2 = 'Picture_user/'+str(tid)
			if not os.path.exists(storeDir2):
				os.mkdir(storeDir2)
			cv2.imwrite(storeDir2+'/'+str(toi)+'.jpg',img)
		except Exception ,e:
			print("Failed in indexDocs:", e)


def use_lucene(img_url ,toi , tid):
	try:
		IndexFiles(img_url, toi , tid,)
	except Exception, e:
		print "Failed: ", e
		raise e



