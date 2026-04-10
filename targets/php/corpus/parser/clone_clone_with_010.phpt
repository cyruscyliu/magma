<?php

try {
	var_dump(clone(new \Random\Engine\Secure(), [ 'with' => "something" ]));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

try {
	var_dump(clone(new \Random\Engine\Xoshiro256StarStar(), [ 'with' => "something" ]));
} catch (Throwable $e) {
	echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>