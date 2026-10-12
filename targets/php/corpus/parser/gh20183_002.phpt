<?php

function gen() {
    try {
        yield 1;
    } finally {
        eval('try { throw new Error(); } catch (Error) {}');
        debug_print_backtrace();
    }
}

class A {
    private $gen;
    function __construct() {
        $this->gen = gen();
        $this->gen->rewind();
    }
}

B::$a = new A();

?>