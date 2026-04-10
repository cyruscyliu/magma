<?php

class A {
    public $a;
}
class B {
    public $b;
}
class C {
    public $c;
}

$aReflector = new ReflectionClass(A::class);
$bReflector = new ReflectionClass(B::class);
$cReflector = new ReflectionClass(C::class);

$c = $cReflector->newLazyGhost(function ($c) {
    $c->c = 1;
});

$b = $bReflector->newLazyGhost(function () {
    throw new \Exception('xxx');
});

$a = $aReflector->newLazyGhost(function ($a) use ($b, $c) {
    $a->a = $c->c + $b->b;
});

try {
    $a->init = 'please';
} catch (\Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

var_dump($a, $b, $c);

?>