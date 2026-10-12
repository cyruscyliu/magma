<?php

interface I {
    public $prop { &get; }
}

class A implements I {
    public $prop;
}

function test(I $i) {
    $ref = &$i->prop;
    $ref = 42;
}

$a = new A();
test($a);
var_dump($a);

?>