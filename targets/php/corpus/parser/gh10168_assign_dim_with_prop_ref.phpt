<?php

class Test {
    static ?Test $test;

    function __destruct() {
        $GLOBALS['a'] = null;
    }
}

$a = [new Test];
Test::$test = &$a[0];
var_dump($a[0] = new Test);

?>