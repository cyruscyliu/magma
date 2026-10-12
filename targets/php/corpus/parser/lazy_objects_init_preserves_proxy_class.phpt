<?php


class A {
    public string $s;
}
class B extends A {
    public function foo() {
        var_dump(__METHOD__);
    }
}

$reflector = new ReflectionClass(B::class);
$o = $reflector->newLazyProxy(function (B $o) {
    return new A();
});

var_dump(get_class($o));
$o->foo();
$o->s = 'init';
var_dump(get_class($o));
$o->foo();


?>