<?php

function my_error_handler(int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
}

set_error_handler('my_error_handler');

#[\Deprecated]
function my_exception_handler($e) {
	echo "Handled: ", $e->getMessage(), PHP_EOL;
};

set_exception_handler('my_exception_handler');

#[\Deprecated]
function test() {
}

test();

?>