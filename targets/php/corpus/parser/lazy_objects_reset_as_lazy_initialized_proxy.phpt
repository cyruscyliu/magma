<?php

class Obj {
    public function __construct(
        public string $name,
    ) {}
}

$r = new ReflectionClass(Obj::class);

$obj = new Obj('obj1');
var_dump($obj);
$r->resetAsLazyProxy($obj, function () {
    return new Obj('obj2');
});
$r->initializeLazyObject($obj);
var_dump($obj);
$r->resetAsLazyProxy($obj, function () {
    return new Obj('obj3');
});
var_dump($obj);
$r->initializeLazyObject($obj);
var_dump($obj);

?>
==DONE==