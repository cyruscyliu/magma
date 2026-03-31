<?php

function test() {
    global $ref;
    byVal(getRef()[0]);
    var_dump($ref);
    byRef(getRef()[0]);
    var_dump($ref);
}

/* Intentionally declared after test() to avoid compile-time checking of ref args. */

function &getRef() {
    global $ref;
    $ref = [];
    return $ref;
}

function byVal($arg) {
    $arg[] = 42;
}

function byRef(&$arg) {
    $arg[] = 42;
}

test();

?>