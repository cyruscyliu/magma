<?php

function test($a, #[\SensitiveParameter] ...$x) {
	debug_print_backtrace();
}

test(b: 1, a: 2, c: 3);

?>