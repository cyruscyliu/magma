<?php

class Clazz {
	#[\Deprecated]
	function __call(string $name, array $params) {
	}

	#[\Deprecated("due to some reason")]
	static function __callStatic(string $name, array $params) {
	}
}

$cls = new Clazz();
$cls->test();
Clazz::test2();

?>