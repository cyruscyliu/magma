<?php

class Test {
    private static function privateMethod() {}

    public function instanceMethod() {}
}

try {
    $fn = 123;
    $fn(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    does_not_exist(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    stdClass::doesNotExist(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    (new stdClass)->doesNotExist(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    [new stdClass, 'doesNotExist'](...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    Test::privateMethod(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    Test::instanceMethod(...);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>