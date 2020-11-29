import numpy as np
import time

class EulerBox:
	def __init__ (self, wid, dim, box=None, dgt=None, adjItm=None, adjVal=None):
		self.wid = wid
		self.dim = dim
		if box is None:
			self.box = np.full(shape=(wid ** dim, wid ** dim), fill_value=0)
			self.dgt = self.wid ** np.arange(self.dim)
			adj = np.arange(wid ** dim)[..., np.newaxis] // self.dgt % self.wid
			adjMask = np.count_nonzero(adj, axis=1)
			self.adjItm = adj[np.bitwise_and(0 < adjMask, adjMask < dim)]
			self.adjVal = adj[adjMask == 1]
			for i in range(self.wid): # OPT
				self.setItm(np.sum(self.dgt)*i, i) # OPT
		else:
			self.box, self.dgt, self.adjItm, self.adjVal = np.copy(box), dgt, adjItm, adjVal

	def getItm (self):
		return np.argmax(np.any(self.box == 0, axis=1))

	def setItm (self, itm, val):
		self.box[itm, ...] = -1
		self.box[..., val] = -1
		self.box[itm, val] = 1
		itmAdj = np.sum((self.adjItm + itm // self.dgt % self.wid) % self.wid * self.dgt, axis=1)
		valAdj = np.sum((self.adjVal + val // self.dgt % self.wid) % self.wid * self.dgt, axis=1)
		adj = np.repeat(itmAdj, self.adjVal.shape[0]), np.tile(valAdj, self.adjItm.shape[0])
		self.box[adj] = -1
		return np.all(np.any(self.box >= 0, axis=0)) and np.all(np.any(self.box >= 0, axis=1)) and np.all(np.diff(np.nonzero(self.box[self.dgt] == 1)[1]) > 0)

	def next (self):
		if np.any(self.box == 0):
			itm = self.getItm()
			vals = np.nonzero(self.box[itm, ...] == 0)[0]
			if vals.size > 1:
				boxes = [EulerBox(self.wid, self.dim, self.box, self.dgt, self.adjItm, self.adjVal) for _ in vals]
				post = []
				for box, val in zip(boxes, vals):
					if box.setItm(itm, val):
						post.append(box)
				return [sol for box in post for sol in box.next()]
			elif self.setItm(itm, vals[0]):
				return self.next()
			else:
				return []
		else:
			return [EulerSol(self.wid, self.dim, self.box, self.dgt)]

class EulerSol:
	def __init__ (self, wid, dim, box, dgt):
		self.wid = wid
		self.dim = dim
		self.box = np.nonzero(box == 1)[1].reshape(dim*(wid,))
		self.dgt = dgt
		print(self.box)
		# self.sort()

	def sort (self):
		take = np.transpose(np.array([np.nonzero(self.box == i) for i in range(self.wid)]).reshape(self.wid, self.dim))
		for d in range(self.dim):
			self.box = np.take_along_axis(self.box, take[d].reshape(d*[1]+[self.wid]+(self.dim - d - 1)*[1]), d)
		slctn = tuple(np.identity(self.dim, dtype=int))
		for i in range(self.dim):
			self.box = np.moveaxis(self.box, np.argmin(self.box[slctn][i:]) + i, i)

a = time.time()
x = EulerBox(7, 2).next()
b = time.time()
print(b - a)
print(len(x))