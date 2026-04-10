<?php

set_error_handler(function (int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	var_dump($errno, E_USER_DEPRECATED, $errno === E_USER_DEPRECATED);
});

#[\Deprecated]
function test() {
}

test();

?>