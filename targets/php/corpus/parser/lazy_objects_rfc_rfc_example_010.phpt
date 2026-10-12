<?php

class MyClass {
    public $a;
    public $b;
}

$reflector = new ReflectionClass(MyClass::class);
$obj = $reflector->newLazyGhost(function () {});

$reflector->getProperty('a')->setRawValueWithoutLazyInitialization($obj, 'value');

var_dump($obj);

?>
==DONE==