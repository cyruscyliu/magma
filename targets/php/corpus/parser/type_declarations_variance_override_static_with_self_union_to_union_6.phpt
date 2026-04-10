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
    public function methodScalar1(): C|array { return []; }
}

$b = new B();
var_dump($b->methodScalar1());
?>