<?php

class A {
    public $a;
}

class B extends A {
    public $b;
}

class C extends A {
    public $a;
    public $c;
}

class D extends A {
    public readonly int $d;
    public function __construct(bool $init = false) {
        if ($init) {
            $this->d = 1;
        }
    }
}

$reflector = new ReflectionClass(A::class);

printf("# B\n");

$obj = new B();
$obj->a = 1;
$obj->b = 2;
$reflector->resetAsLazyGhost($obj, function () {});
var_dump($obj->b);
var_dump($obj);
var_dump($obj->a);
var_dump($obj);

printf("# C\n");

$obj = new C();
$obj->a = 1;
$obj->c = 2;
$reflector->resetAsLazyGhost($obj, function () {});
var_dump($obj->c);
var_dump($obj);
var_dump($obj->a);
var_dump($obj);

printf("# D\n");

$obj = new D();
$obj->a = 1;
$reflector->resetAsLazyGhost($obj, function ($obj) {
    $obj->__construct(true);
});
var_dump($obj->d ?? 'undef');
var_dump($obj);
var_dump($obj->a);
var_dump($obj);
