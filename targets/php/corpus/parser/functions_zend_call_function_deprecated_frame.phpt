<?php

#[Deprecated]
function foo(string $v) {
	return $v . '!';
}

set_error_handler(function ($number, $message) {
	throw new Exception($message);
});

$a = array_map(foo(...), ['Hello', 'World']);
var_dump($a);

?>