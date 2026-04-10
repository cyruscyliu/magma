<?php

interface A
{
    public function method1(): static;
}

class Foo implements A
{
    public function method1(): self
    {
        return $this;
    }
}

$foo = new Foo();

var_dump($foo->method1());
?>