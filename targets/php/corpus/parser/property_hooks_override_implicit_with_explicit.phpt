<?php

class A {
    public $prop;
}

class B extends A {
    public $prop {
        get { echo __CLASS__ . '::' . __METHOD__ . "\n"; return 3; }
        set { echo __CLASS__ . '::' . __METHOD__ . "\n"; }
    }
}

$a = new A;
$a->prop = 1;
var_dump($a->prop);

$b = new B;
$b->prop = 2;
var_dump($b->prop);

?>