# DESCRIPTION:

# Optimally choose the centers of taylor series to best approximate log2 from 1 to 2

# FORMULAS:

# The taylor series for log(x) centerd at c with depth d
# log(c) - log(e) * sum(n = 1 => d, 1/n * (1 - x/c)^n)

# The error of the taylor series is the sum of the remaining terms
# log(e) * |sum(n = d => inf, 1/n * (1 - x/c)^n)|

# Because the taylor series has alternating signs
# The only zero of the error function is at c

# Integrating the error
# log(e) * |integral(sum(n = d => inf, 1/n * (1 - t/c)^n)*dt)|
# Simplify
# u = 1 - t/c; du = -1/c*dt; dt = -c*du
# c * log(e) * |integral(sum(n = d => inf, 1/n * u^n)*du)|
# c * log(e) * |sum(n = d => inf, 1/n(n+1) * (1 - t/c)^n+1)|
# c * log(e) * |sum(n = d + 1 => inf, 1/n(n-1) * (1 - t/c)^n)|
# When using the integral from a to b
# The sign may change at c, so split the range into (from a to c) and (from c to b)
# Both c terms simplify to zero because (1-c/c)=0
# The a term is always positive, and the b term is alternating
# c * log(e) * sum(n = d + 1 => inf, 1/n(n-1) * ((1 - a/c)^n - (-1)^d * (1 - b/c)^n))

# From two center points, calculate the ideal boundary
# Error at point x using the first center = Error at point x using the second center
# log(e) * |sum(n = d => inf, 1/n * (1 - x/c1)^n)| = log(e) * |sum(n = d => inf, 1/n * (1 - x/c2)^n)|
# |sum(n = d => inf, 1/n * (1 - x/c1)^n)| - |sum(n = d => inf, 1/n * (1 - x/c2)^n)| = 0
# This will be solved analytically with Newton's method

# CODE:

import numpy as np

epsilon = 0.0001
epsilon_modifiers_center = epsilon * np.arange(-1, 2)[np.newaxis, np.newaxis, ..., np.newaxis]
epsilon_modifiers_length = epsilon * np.array([-1, 1])[np.newaxis, ..., np.newaxis]

def get_boundaries (centers, depth):
	indx = np.arange(depth, 2000)
	centers_adjacent = np.transpose(np.vstack((centers[:-1], centers[1:])))[..., np.newaxis, np.newaxis]
	boundaries = np.sum(centers_adjacent, axis=1, keepdims=True)/2
	for _ in range(5):
		boundaries_iter = 1 - (boundaries + epsilon_modifiers_center) / centers_adjacent
		boundaries_iter_val = np.abs(np.sum(boundaries_iter**indx / indx, axis=3))
		boundaries_iter_diff = boundaries_iter_val[:, 0, :] - boundaries_iter_val[:, 1, :]
		boundaries_iter_move = (2 * epsilon * boundaries_iter_diff[:, 1] / (boundaries_iter_diff[:, 2] - boundaries_iter_diff[:, 0]))
		boundaries -= boundaries_iter_move[..., np.newaxis, np.newaxis, np.newaxis]
	boundaries_all = np.hstack((1, boundaries[:, 0, 0, 0], 2))
	return np.transpose(np.vstack((boundaries_all[:-1], boundaries_all[1:])))

def cost_centers (centers, depth):
	indx = np.arange(depth, 2000)
	boundaries = get_boundaries(centers, depth)[..., np.newaxis]
	centers_final = centers[..., np.newaxis, np.newaxis]
	centers_iter = 1 - boundaries / centers_final
	centers_iter_val = np.abs(np.sum(centers_iter**indx/(indx*(indx-1)), axis=2))
	centers_iter_col = centers * np.sum(centers_iter_val, axis=1)
	return np.log2(np.e) * np.sum(centers_iter_col)

def cost_descend (centers, depth, steps):
	print('New Trial', steps)
	for _ in range(steps):
		centers_iter = (centers + np.identity(centers.size)[:, np.newaxis, :] * epsilon_modifiers_length).reshape(centers.size*2, centers.size)
		centers_val = np.array([cost_centers(i, depth) for i in centers_iter]).reshape(centers.size, 2)
		centers_gradient = (centers_val[:, 1] - centers_val[:, 0]) / (2 * epsilon)
		centers -= centers_gradient
	cost = cost_centers(centers, depth)
	boundaries = get_boundaries(centers, depth)
	print(cost)
	return cost, centers, boundaries

def cost_all (length, depth, trials):
	pool = sorted((cost_descend(1 + np.sort(np.random.random(length)), depth, trials[0][1]) for _ in range(trials[0][0])), key=lambda i: i[0])
	for t in trials[1:]:
		pool = pool[:t[0]]
		pool = sorted((cost_descend(p[1], depth, t[1]) for p in pool), key=lambda i: i[0])
	return pool

for solution in cost_all(6, 4, [(500, 3), (50, 10), (10, 50), (5, 150), (2, 300)]):
	print()
	print('New Solution')
	print(solution[0])
	print(solution[1])
	print(solution[2])
