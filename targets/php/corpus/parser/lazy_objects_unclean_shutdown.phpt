<?php

class C {
    public $a;
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    // Trigger a fatal error to get an unclean shutdown
    class bool {}
});

var_dump($obj->a);