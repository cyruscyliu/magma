<?php

class Test {
    public $prop {
        get {
            static $foo = [];
            static $count = 1;
            $foo[] = $count++;
            return $foo;
        }
    }
}

$test = new Test;
var_dump($test->prop);
var_dump($test->prop);
var_dump($test->prop);

?>