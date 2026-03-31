<?php

class Foo {
    public function __destruct() {
        debug_print_backtrace();
    }
}

function bar() {
    yield from foo();
}

function foo() {
    $foo = new Foo();
    yield;
}

$gen = bar();
foreach ($gen as $dummy);

?>