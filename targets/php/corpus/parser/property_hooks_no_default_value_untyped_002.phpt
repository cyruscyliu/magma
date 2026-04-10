<?php

class A {
    public $prop;
}

class B extends A {
    public $prop {
        set {}
    }
}

$b = new B;
var_dump($b->prop);

?>