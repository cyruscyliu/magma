<?php

class C {
    public function __construct(public $x) {}
}
function test(
    $a = new C(__CLASS__),
    $b = new C(__FUNCTION__),
    $c = new C(x: __FILE__),
) {
    var_dump($a, $b, $c);
}
test();

// Check that nested new works as well.
function test2($p = new C(new C(__FUNCTION__))) {
    var_dump($p);
}
test2();

?>