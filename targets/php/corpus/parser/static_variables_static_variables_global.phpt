<?php

function foo() {
    static $a = 42;
    var_dump($a);
    global $a;
    $a = 41;
    var_dump($a);
}

foo();
foo();

?>