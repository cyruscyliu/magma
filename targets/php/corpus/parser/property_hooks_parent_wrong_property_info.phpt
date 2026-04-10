<?php

class A {
    private int $prop;
}

class B extends A {
    public int $prop {
        get => parent::$prop::get();
    }
}

$b = new B;
try {
    var_dump($b->prop);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>