#! /usr/bin/python
import numpy
from itertools import count
import matplotlib.pylab as plt
class objectOnTable(object):
	_ids = count(0)
	def __init__(self, x, y, theta = None, shape = 'circle'):
		self.x = x
		self.y = y
		self.shape = shape
		self.theta = theta
		self.delGridX, self.delGridY = self.cellsToOccupy()
		self.tag =  next(self._ids)
	def cellsToOccupy(self):
		if self.shape == 'circle':
			delGridX = 1.5
			delGridY = 1.5
		elif self.shape == 'rectangle':
			length = 5
			delGridX = length * numpy.cos(self.theta) / 2
			delGridY = length * numpy.sin(self.theta) / 2
		return delGridX, delGridY
	def updatePose(self, newX, newY, newTheta):
		self.x = newX
		self.y = newY
		self.theta = newTheta
		self.delGridX, self.delGridY = self.cellsToOccupy()

class costMap(object):
	def __init__(self, objOnTableList):
		self.worldMap = self.createWorldMap(objOnTableList)
		self.matMap = self.createMatMap(objOnTableList)

	def createWorldMap(self, objOnTableList):
		worldMap = {}
		for i in range(len(objOnTableList)):
			obj = objOnTableList[i]
			worldMap[obj.tag] = (obj.x, obj.y, obj.delGridX, obj.delGridY)
		return worldMap
	def createMatMap(self, objOnTableList):
		# table dimensions in cm 
		tableWidth = 50
		tableHeight = 50
		matMap = numpy.zeros([tableWidth, tableHeight])
		for i in range(len(objOnTableList)):
			obj = objOnTableList[i]
			x, y, delGridX, delGridY = (obj.x, obj.y, obj.delGridX, obj.delGridY)
			x = numpy.ceil(x);
			y = numpy.ceil(y);
			delGridX = numpy.ceil(delGridX);
			delGridY = numpy.ceil(delGridY);
			
			rCorn1 = int(x - delGridX)
			cCorn1 = int(y - delGridY)
			rCorn2 = int(x + delGridX)
			cCorn2 = int(y + delGridY)
			matMap[rCorn1:rCorn2, cCorn1:cCorn2] = matMap[rCorn1:rCorn2, cCorn1:cCorn2]- 1
		plt.imshow(matMap, interpolation = 'none', cmap = 'gray')
		plt.show(block=False)
		ch = raw_input("Continue ?")
		return matMap
		
	def updateWorldMap(self, obj):
		self.worldMap[obj.tag] = (obj.x, obj.y, obj.delGridX, obj.delGridY)
	def visualize(self):
		tagsOnTable = self.worldMap.keys()
		for tag in tagsOnTable:
			x, y, delGridX, delGridY = self.worldMap[tag]

def updateObjectOnTable(tableMap, obj, newX, newY, newTheta):
	obj.updatePose(newX, newY, newTheta)
	tableMap.updateWorldMap(obj)
	tableMap.updateMatMap(obj)

def planToTarget(tableMap, targetObject):
	pass

if __name__=="__main__":
	soup = objectOnTable(30, 40)
	spam = objectOnTable(10, 20, numpy.pi/2, shape = 'rectangle')
	glass = objectOnTable(20, 30)
	tableMap = costMap([soup, spam, glass])

