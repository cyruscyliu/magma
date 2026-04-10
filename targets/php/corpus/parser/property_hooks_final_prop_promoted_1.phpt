<?php

class A {
    public function __construct(
        public final $prop { get {} set {} }
    ) {}
}

class B extends A {
    public $prop { get {} set {} }
}

?>