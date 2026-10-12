<?php

class A {
    public $prop {
        get { echo __CLASS__ . '::' . __METHOD__, "\n"; return 42; }
    }
}

class B extends A {
    public $prop {
        get { echo __CLASS__ . '::' . __METHOD__, "\n"; return 42; }
        set { echo __CLASS__ . '::' . __METHOD__, "\n"; }
    }
}

$a = new A;
try {
    $a->prop = 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($a->prop);

$b = new B;
$b->prop = 1;
var_dump($b->prop);

?>