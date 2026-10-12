<?php

set_error_handler(function (int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	var_dump($errno, E_USER_WARNING, $errno === E_USER_WARNING);
});

#[\NoDiscard]
function test(): int {
	return 0;
}

test();

?>