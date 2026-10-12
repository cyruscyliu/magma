<?php

class Test {
	public function __call($name, $args) {
        var_dump($name, $args);
    }
	public static function __callStatic($name, $args) {
        var_dump($name, $args);
    }
}

$test = new Test;

$array = ["unpacked"];

echo "-- Non-static cases --\n";
$test->test(1, 2, a: 123);
$test->test(...)(1, 2);
$test->test(...)(1, 2, a: 123, b: $test);
$test->test(...)(a: 123, b: $test);
$test->test(...)();
$test->test(...)(...$array);

echo "-- Static cases --\n";
Test::testStatic(1, 2, a: 123);
Test::testStatic(...)(1, 2);
Test::testStatic(...)(1, 2, a: 123, b: $test);
Test::testStatic(...)(a: 123, b: $test);
Test::testStatic(...)();
Test::testStatic(...)(...$array);

echo "-- Reflection tests --\n";
$reflectionFunction = new ReflectionFunction(Test::fail(...));
var_dump($reflectionFunction->getParameters());
$argument = $reflectionFunction->getParameters()[0];
var_dump($argument->isVariadic());
$type = $argument->getType();
var_dump($type);
var_dump($type->getName());

?>