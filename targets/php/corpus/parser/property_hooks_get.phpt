<?php

class Test {
    public $prop {
        get { return 42; }
    }
}

$test = new Test;
var_dump($test->prop);

try {
    $test->prop = 0;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>