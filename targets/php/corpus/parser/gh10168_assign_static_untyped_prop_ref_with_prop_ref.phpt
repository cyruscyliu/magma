<?php

class Test {
    static $test;
    static ?Test $test2;

    function __destruct() {
        Test::$test = null;
    }
}

Test::$test = new Test;
Test::$test2 = &Test::$test;
$tmp = new Test;
var_dump(Test::$test = &$tmp);

?>