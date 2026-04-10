<?php

class A {
    public $a;
}
class B extends A {}

class C {}

$reflector = new ReflectionClass(A::class);

$reflector->resetAsLazyGhost(new A(), function () {});
$reflector->resetAsLazyGhost(new B(), function () {});

try {
    $reflector->resetAsLazyGhost(new C(), function () {});
} catch (TypeError $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

?>
==DONE==