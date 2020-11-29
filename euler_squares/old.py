import numpy as np
import time

class EulerBox:
	def __init__ (self, wid, dim, box=None, adj=None, dgt=None):
		self.wid = wid
		self.dim = dim
		self.box = np.full(shape=(wid ** dim, wid ** dim), fill_value=0) if box is None else np.copy(box)
		self.adj = np.repeat(np.identity(dim, dtype=int), wid - 1, axis=0) * np.tile(np.arange(1, wid), dim)[..., np.newaxis] if adj is None else adj
		self.dgt = self.wid ** np.arange(self.dim) if dgt is None else dgt

	def getItm (self):
		return np.argmax(np.any(self.box == 0, axis=1))

	def setItm (self, itm, val):
		self.box[itm, ...] = -1
		self.box[..., val] = -1
		self.box[itm, val] = 1
		itmAdj = np.sum((self.adj + itm // self.dgt % self.wid) % self.wid * self.dgt, axis=1)
		valAdj = np.sum((self.adj + val // self.dgt % self.wid) % self.wid * self.dgt, axis=1)
		adj = np.repeat(itmAdj, self.adj.shape[0]), np.tile(valAdj, self.adj.shape[0])
		self.box[adj] = -1
		return np.all(np.any(self.box >= 0, axis=0)) and np.all(np.any(self.box >= 0, axis=1))

	def next (self):
		if np.any(self.box == 0):
			itm = self.getItm()
			vals = np.nonzero(self.box[itm, ...] == 0)[0]
			if vals.size > 1:
				boxes = [EulerBox(self.wid, self.dim, self.box, self.adj, self.dgt) for _ in vals]
				post = []
				for box, val in zip(boxes, vals):
					if box.setItm(itm, val):
						post.append(box)
				return [sol for box in post for sol in box.next()]
			else:
				self.setItm(itm, vals[0])
				return self.next()
		else:
			return [EulerSol(self.wid, self.dim, self.box)]

class EulerSol:
	def __init__ (self, wid, dim, box):
		self.wid = wid
		self.dim = dim
		self.box = np.nonzero(box == 1)[1]
		print(self.box)

a = time.time()
x = EulerBox(4, 2).next()
b = time.time()
print(b - a)
print(len(x))