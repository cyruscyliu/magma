<?php

class A {
    public function __construct(
        public final $prop
    ) {}
}

class B extends A {
    public $prop { get {} set {} }
}

?>