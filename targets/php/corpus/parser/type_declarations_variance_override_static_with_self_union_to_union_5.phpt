<?php

interface A
{
    public function methodScalar1(): static|bool;
}

final class C
{
}

final class B implements A
{
    public function methodScalar1(): C { return new C(); }
}

$b = new B();
var_dump($b->methodScalar1());
?>