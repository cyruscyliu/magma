<?php

class A {
    function __destruct() {
        eval('try { throw new Error(); } catch (Error $e) {}');
        debug_print_backtrace();
    }
}

B::$b = new A;

?>