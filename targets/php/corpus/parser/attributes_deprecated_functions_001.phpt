<?php

#[\Deprecated]
function test() {
}

#[\Deprecated("use test() instead")]
function test2() {
}

class Clazz {
	#[\Deprecated]
	function test() {
	}

	#[\Deprecated("use test() instead")]
	function test2() {
	}
}

$closure = #[\Deprecated] function() {
};

$closure2 = #[\Deprecated] function() {
};

class Constructor {
	#[\Deprecated]
	public function __construct() {
	}

	#[\Deprecated]
	public function __destruct() {
	}
}

test();
test2();
call_user_func("test");

$cls = new Clazz();
$cls->test();
$cls->test2();

call_user_func([$cls, "test"]);

$closure();

$closure2();

new Constructor();

?>