<?php
$map = new WeakMap;

class Test {
	public stdClass|string $obj;
}

$test = new Test;
$test->obj = new stdClass;

$map[$test->obj] = new class {
    function __destruct() {
		global $test;
		var_dump($test->obj);
        throw new Exception("Test");
    }
};

headers_sent($test->obj);
?>