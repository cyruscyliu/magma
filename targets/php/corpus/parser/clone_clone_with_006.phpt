<?php

$x = new stdClass();

try {
	var_dump(clone($x, 1));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>