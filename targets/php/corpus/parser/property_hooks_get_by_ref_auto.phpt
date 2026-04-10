<?php

class Test {
    public $byVal { get { return []; } }
}

$test = new Test;

try {
    $test->byVal[] = 42;
} catch (\Error $e) {
    echo get_class($e) . ': ' . $e->getMessage() . "\n";
}
var_dump($test->byVal);

try {
    $test->byVal =& $ref;
} catch (Error $e) {
    echo get_class($e) . ': ' . $e->getMessage() . "\n";
}

?>