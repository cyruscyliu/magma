<?php

class MyClass {
    public $id;
    public $b;
}

$reflector = new ReflectionClass(MyClass::class);
$object = $reflector->newLazyGhost(function () {
    throw new \Exception('initialization');
});

$reflector->getProperty('id')->skipLazyInitialization($object);

$object->id = 1;
var_dump($object->id);

?>
==DONE==