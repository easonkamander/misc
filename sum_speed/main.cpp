#include <cmath>
#include <chrono>
#include <iostream>

// Calculate a sum of numbers from 1 to n

int sumLoop (int n) { // manually add
	int out = 0;
	for (int i = 1; i <= n; i++) {
		out += i;
	}
	return out;
}

int sumTriI (int n) { // triangular number formula with integers
	return n * (n + 1) / 2;
}

int sumTriF (int n) { // triangular number formula with floats
	return (int)(0.5f * (float)n * ((float)n + 1.0f));
}

float invsqrt (float x) { // fast inverse sqrt hack
	float x2 = 0.5f * x;
	long x3 = *(long *) &x;
	x3 = 0x5f3759df - (x3 >> 1);
	x = *(float *) &x3;
	x *= (1.5f - (x * x * x2));
	x *= (1.5f - (x * x * x2));
	x *= (1.5f - (x * x * x2));
	return x;
}

int sumHack (int n) { // derived from n * (n + 1) = 1/(1/n + 1/(n + 1))
	float x = (float)n;
	float x1 = invsqrt(x);
	float x2 = invsqrt(x + 1.f);
	float x3 = invsqrt((x1 + x2) * (x1 - x2));
	return (int)(0.5f * x3 * x3 + 0.5f);
}

long loop (int (*func) (int), int repeat, int rangeA, int rangeB) { // speed test
	std::chrono::steady_clock::time_point time1 = std::chrono::steady_clock::now();
	for (int i = 0; i < repeat; i++) {
		for (int j = rangeA; j < rangeB; j++) {
			func(j);
		}
	}
	std::chrono::steady_clock::time_point time2 = std::chrono::steady_clock::now();
	return std::chrono::duration_cast<std::chrono::microseconds> (time2 - time1).count();
}

int main () {
	int i = 1;
	int diff = 0;
	while (i < 1000 && diff == 0) {
		i++;
		diff = sumHack(i) - sumTriI(i);
	}
	std::cout << "Hack Works Up To: " << i << std::endl; // 157 using float32 and three newton approx
	std::cout << std::endl;
	std::cout << "Loop: " << loop(sumLoop, 10000, 100, 150) << std::endl; // about 300 nanoseconds each
	std::cout << "TriI: " << loop(sumTriI, 10000, 100, 150) << std::endl; // about   3 nanoseconds each
	std::cout << "TriF: " << loop(sumTriF, 10000, 100, 150) << std::endl; // about   3 nanoseconds each
	std::cout << "Hack: " << loop(sumHack, 10000, 100, 150) << std::endl; // about 100 nanoseconds each
	return 0;
}