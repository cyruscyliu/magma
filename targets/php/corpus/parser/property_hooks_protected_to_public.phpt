<?php

class A {
    protected $prop {
        get => 42;
    }
}

class B extends A {
    public $prop {
        set {}
    }
}

$b = new B();
var_dump($b->prop);

?>