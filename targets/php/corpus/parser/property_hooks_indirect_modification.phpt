<?php


class Test {
    public $byVal {
        set {
            echo __METHOD__, "\n";
            $this->byVal = $value;
        }
    }
}

$test = new Test;

$test->byVal = 0;
$test->byVal++;
++$test->byVal;
$test->byVal += 1;
var_dump($test->byVal);
$test->byVal = [];
try {
    $test->byVal[] = 1;
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->byVal);
try {
    $ref =& $test->byVal;
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}
$ref = 42;
var_dump($test->byVal);

?>