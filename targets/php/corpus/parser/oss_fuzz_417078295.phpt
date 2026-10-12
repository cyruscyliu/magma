<?php

function foo() {
    $a = new stdClass();
    static $a = $a;
    debug_zval_dump($a);
}

foo();

?>