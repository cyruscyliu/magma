<?php

class A {
    public $prop = 42;
}

class B extends A {
    public $prop = 42 {
        set {}
    }
}

$b = new B;
array_walk($b, function (&$item) {
    var_dump($item);
});

?>