<?php

class Test {
    public $prop {
        set($customName) {
            var_dump($customName);
        }
    }
}

$test = new Test();
$test->prop = 42;

?>