#include <cmath>
#include <chrono>
#include <iostream>

int powInt (int a, int b) { // calculate an integer exponent with recursion
	return (b % 2 * (a - 1) + 1) * (b > 1 ? powInt(a * a, b / 2) : 1);
}

int powDbl (int a, int b) { // calculate an integer exponent the normal way
	return (int)pow(a, b);
}

long loop (bool native, int a1, int a2, int b1, int b2, int repetitions) { // speed test
	int (*func) (int, int) = native ? powInt : powDbl;
	std::chrono::steady_clock::time_point time1 = std::chrono::steady_clock::now();
	for (int a = a1; a < a2; a++) {
		for (int b = b1; b < b2; b++) {
			for (int c = 0; c < repetitions; c++) {
				func(a, b);
			}
		}
	}
	std::chrono::steady_clock::time_point time2 = std::chrono::steady_clock::now();
	return std::chrono::duration_cast<std::chrono::microseconds> (time2 - time1).count();
}

int main () {
	std::cout << "For small powers between 0 and 16, integer recursion is faster: " << std::endl;
	std::cout << "Using Integer Recursion: " << loop(true, 0, 400, 0, 16, 1000) << std::endl; // about 80 milliseconds
	std::cout << "Using Floating Point Math: "<< loop(false, 0, 400, 0, 16, 1000) << std::endl; // about 130 milliseconds
	std::cout << std::endl;
	std::cout << "As powers grow larger, floating point becomes more efficient:" << std::endl;
	std::cout << "Using Integer Recursion: " << loop(true, 0, 400, 36, 37, 10000) << std::endl; // about 90 milliseconds
	std::cout << "Using Floating Point Math: "<< loop(false, 0, 400, 36, 37, 10000) << std::endl; // about 90 milliseconds
	return 0;
}