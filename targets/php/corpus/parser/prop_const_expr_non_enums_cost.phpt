<?php

class A {
    public $prop = 42;
}

const A = new A();
const A_prop = A->prop;

?>