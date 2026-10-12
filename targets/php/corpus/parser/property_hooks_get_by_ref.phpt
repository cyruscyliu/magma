<?php

class Test {
    public $byVal {
        get { return $this->byVal; }
        set { $this->byVal = $value; }
    }
}

$test = new Test;

try {
    $test->byVal = [];
    $test->byVal[] = 42;
} catch (\Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->byVal);

try {
    $test->byVal =& $ref;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>