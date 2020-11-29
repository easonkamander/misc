let canvas = document.querySelector('#main');
let context = canvas.getContext("2d");

let px = 800;
let size = 15;
let font = 0.9;
let fontX = font * 9.6;
let fontY = font * 11.5;
let slope = 0.5;

context.font = ''+font+'em Roboto Mono';

let factorial = (n) => {
	out = 1;
	i = 1;
	while (i <= n) {
		out *= i;
		i++;
	}
	return out;
}

let gridToPx = (grid) => {
	return {
		x: px / (size + 1) * (grid.x - grid.y / 2) + px / 2,
		y: px / (size + 1) * (grid.y + 0.5)
	};
};

let draw = (row, move) => {
	context.fillStyle = 'white';
	context.fillRect(0, 0, px, px);
	context.fillStyle = 'black';

	for (let i = 0; i < row; i++) {
		for (let j = 0; j <= i; j++) {
			let center = gridToPx({x: j, y: i});
			let num = factorial(i) / (factorial(j) * factorial(i - j));
			context.fillText(num.toString(), center.x - fontX * num.toString().length / 2, center.y + fontY / 2);
		}
	}

	for (let k = 0; k <= row; k++) {
		let center = gridToPx({x: k, y: row});
		let num = factorial(row) / (factorial(k) * factorial(row - k));

		if (move > 1) {
			let mot = px / (2 * size + 2);

			context.fillText(
				num.toString(),
				center.x - fontX * num.toString().length / 2 - mot,
				center.y + fontY / 2 + slope * mot + (move - 1) * (px / (size + 1) - slope * mot)
			);
	
			context.fillText(
				num.toString(),
				center.x - fontX * num.toString().length / 2 + mot,
				center.y + fontY / 2 - slope * mot + (move - 1) * (px / (size + 1) + slope * mot)
			);

			context.fillStyle = 'rgba(0, 0, 0, '+(move - 1)+')';
			context.fillText(num.toString(), center.x - fontX * num.toString().length / 2, center.y + fontY / 2);
			context.fillStyle = 'black';
		} else {
			let mot = move * px / (2 * size + 2);

			context.fillText(
				num.toString(),
				center.x - fontX * num.toString().length / 2 - mot,
				center.y + fontY / 2 + slope * mot
			);
	
			context.fillText(
				num.toString(),
				center.x - fontX * num.toString().length / 2 + mot,
				center.y + fontY / 2 - slope * mot
			);
		}
	}
}

let r = 0;
let m = 0;
setInterval(() => {
	m += 0.01;
	if (m > 2) {
		m = 0;
		r++;
	}
	if (r < size) {
		draw(r, m);
	} else {
		draw(size, 0);
	}
}, 20);