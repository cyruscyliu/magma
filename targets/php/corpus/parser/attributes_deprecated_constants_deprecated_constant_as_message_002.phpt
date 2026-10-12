<?php

set_error_handler(function (int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
});

#[\Deprecated(TEST)]
const TEST = "from itself";

#[\Deprecated]
const TEST2 = "from another";

#[\Deprecated(TEST2)]
const TEST3 = 1;

try {
	TEST;
} catch (ErrorException $e) {
	echo "Caught: ", $e->getMessage(), PHP_EOL;
}

try {
	TEST3;
} catch (ErrorException $e) {
	echo "Caught: ", $e->getMessage(), PHP_EOL;
}

?>