<?php

function my_error_handler(int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
}

set_error_handler('my_error_handler');

#[\Deprecated]
trait DemoTrait {}

class DemoClass {
	use DemoTrait;
}

?>