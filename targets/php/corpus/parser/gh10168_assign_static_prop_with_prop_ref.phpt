<?php

class Test {
    static ?Test $test;
    static ?Test $test2;

    function __destruct() {
        Test::$test = null;
    }
}

Test::$test = new Test;
Test::$test2 = &Test::$test;
var_dump(Test::$test = new Test);

?>