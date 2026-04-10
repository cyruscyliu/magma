<?php

class Test {
    public $prop {
        get() {
            var_dump($customName);
        }
    }
}

$test = new Test();
$test->prop = 42;

?>