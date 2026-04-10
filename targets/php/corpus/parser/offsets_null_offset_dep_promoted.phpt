<?php

set_error_handler(function ($errno, $errstr) {
    throw new Exception($errstr);
});

try {
	$a = ['foo' => 'bar', null => new stdClass];
} catch (Throwable $e) {
	echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
?>