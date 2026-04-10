<?php

set_error_handler(function (int $errno, string $errstr, ?string $errfile = null, ?int $errline = null) {
	throw new \ErrorException($errstr, 0, $errno, $errfile, $errline);
});

class Clazz {
	#[\Deprecated(self::TEST)]
	public const TEST = "from itself";

	#[\Deprecated]
	public const TEST2 = "from another";

	#[\Deprecated(self::TEST2)]
	public const TEST3 = 1;
}

try {
	Clazz::TEST;
} catch (ErrorException $e) {
	echo "Caught: ", $e->getMessage(), PHP_EOL;
}

try {
	Clazz::TEST3;
} catch (ErrorException $e) {
	echo "Caught: ", $e->getMessage(), PHP_EOL;
}

?>