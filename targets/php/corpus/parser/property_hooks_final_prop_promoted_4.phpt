<?php

class A {
    public function __construct(
        final $prop
    ) {}
}

class B extends A {
    public $prop;
}

?>