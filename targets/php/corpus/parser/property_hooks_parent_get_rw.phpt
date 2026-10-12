<?php

class A {
    public int $prop {
        get {
            return 41;
        }
    }
}

class B extends A {
    public int $prop {
        get {
            return ++parent::$prop::get();
        }
    }
}

$b = new B;
var_dump($b->prop);

?>