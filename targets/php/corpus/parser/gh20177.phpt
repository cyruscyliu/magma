<?php

class A {
    private $prop = 'A::$prop';

    public function __construct() {
        var_dump(get_object_vars($this));
    }
}

class B extends A {
    protected $prop = 'B::$prop';
}

new B;

?>