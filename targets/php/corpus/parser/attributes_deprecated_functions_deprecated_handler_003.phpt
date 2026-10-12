<?php

#[\Deprecated]
function my_error_handler(int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	echo $errstr, PHP_EOL;
};

set_error_handler('my_error_handler');

#[\Deprecated]
function test() {
}

test();

?>