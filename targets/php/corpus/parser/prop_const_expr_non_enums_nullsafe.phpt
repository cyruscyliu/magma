<?php

class A {
    public $prop = 42;
}

const A_prop = (new A)?->prop;

?>