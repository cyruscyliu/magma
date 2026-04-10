<?php

class MyLazyClass
{
    private int $foo;

    public function __construct()
    {
        $reflector = new ReflectionClass(self::class);
        $reflector->resetAsLazyGhost($this, $this->initialize(...), ReflectionClass::SKIP_DESTRUCTOR);
    }

    public function initialize()
    {
        $this->foo = 123;
    }

    public function getFoo()
    {
        return $this->foo;
    }

    public function __destruct()
    {
        var_dump(__METHOD__);
    }
}

$object = new MyLazyClass();

var_dump($object);
var_dump($object->getFoo());
var_dump($object);

?>
==DONE==