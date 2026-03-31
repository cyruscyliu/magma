<?php

class A {
    public $prop = 42;
}

function foo($prop = (new A)->prop) {}

function test() {
    try {
        foo();
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
}

test();
test();

?>