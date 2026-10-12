<?php

interface A
{
    public function methodScalar1(): static|bool;
}

final class B implements A
{
    public function methodScalar1(): self|array { return []; }
}

$b = new B();
var_dump($b->methodScalar1());
?>