<?php

function test() {
	$k = 1;
	return function () use ($k) {
		foo();
	};
}

ini_set('memory_limit', '2M');

$array = [];
for ($i = 0; $i < 10_000; $i++) {
	$array[] = test();
}

?>