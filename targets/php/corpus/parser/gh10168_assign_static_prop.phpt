<?php

class Test {
    static ?Test $test;

    function __destruct() {
        Test::$test = null;
    }
}

Test::$test = new Test;
var_dump(Test::$test = new Test);

?>