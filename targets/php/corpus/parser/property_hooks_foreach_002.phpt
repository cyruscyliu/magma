<?php

class A extends stdClass {
    public $foo {
        &get => $this->foo;
    }
}

$a = new A;
foreach ($a as $k => &$v) {
    if ($k == "foo") {
        $a->bar = "baz";
    }
    var_dump($k);
}

?>