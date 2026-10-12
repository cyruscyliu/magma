<?php

$x = new stdClass();

$ref = 'reference';
$with = ['x' => &$ref];

try {
	var_dump(clone($x, $with));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

unset($ref);

try {
	var_dump(clone($x, $with));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>