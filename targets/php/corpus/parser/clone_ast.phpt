<?php

$x = new stdClass();


try {
	assert(false &&  $y = clone $x);
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x, ));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x, [ "foo" => $foo, "bar" => $bar ]));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x, $array));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x, $array, $extraParameter, $trailingComma, ));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone(object: $x, withProperties: [ "foo" => $foo, "bar" => $bar ]));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone($x, withProperties: [ "foo" => $foo, "bar" => $bar ]));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone(object: $x));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone(object: $x, [ "foo" => $foo, "bar" => $bar ]));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone(...["object" => $x, "withProperties" => [ "foo" => $foo, "bar" => $bar ]]));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

try {
	assert(false && $y = clone(...));
} catch (Error $e) {
	echo $e->getMessage(), PHP_EOL;
}

?>