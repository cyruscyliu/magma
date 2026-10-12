<?php

class MyClass
{
    public function __construct(private int $foo)
    {
        // Heavy initialization logic here.
    }

    public function getFoo()
    {
        return $this->foo;
    }
}

$initializer = static function (MyClass $ghost): void {
    $ghost->__construct(123);
};

$reflector = new ReflectionClass(MyClass::class);
$object = $reflector->newLazyGhost($initializer);

var_dump($object);
var_dump($object->getFoo());
var_dump($object);

?>