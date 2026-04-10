<?php

interface I {}
interface J {}

class A implements I {}
class B implements J {}
class C implements I, J {}

class Test {
    public function __construct(
        public I $a,
        public J $b,
    ) {
    }
}

function test($obj, $a, $b) {
    $obj->$b =& $obj->$a;
    try {
        $obj->$a = new B;
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    try {
        $obj->$b = new A;
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    $obj->$a = new C;
    unset($obj->$a);
    $obj->$b = new B;
}

$reflector = new ReflectionClass(Test::class);
$obj = $reflector->newLazyProxy(function () {
    return new Test(new C, new C);
});

test($obj, 'a', 'b');

var_dump($obj);

?>