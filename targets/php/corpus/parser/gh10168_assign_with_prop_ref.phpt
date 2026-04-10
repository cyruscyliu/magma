<?php

class Test {
    static ?Test $test;

    function __destruct() {
        $GLOBALS['a'] = null;
    }
}

$a = new Test;
Test::$test = &$a;
var_dump($a = new Test);

?>