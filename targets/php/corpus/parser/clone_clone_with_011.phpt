<?php

class Foo {
	private string $bar = 'default';
}

try {
	var_dump(clone(new Foo(), ["\0Foo\0bar" => 'updated']));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>