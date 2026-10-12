<?php

class C {
    public function __construct(
        public $prop { set => $value * 2; }
    ) {}
}

$c = new ReflectionClass(C::class)->newInstanceWithoutConstructor();
var_dump($c);

?>