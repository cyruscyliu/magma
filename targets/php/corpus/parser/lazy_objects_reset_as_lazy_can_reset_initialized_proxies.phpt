<?php

class A {
    public function __construct(
        public $a,
        public $proxy,
    ) {}
    public function __destruct() {
        var_dump(__METHOD__);
        var_dump($this);
    }
}

$reflector = new ReflectionClass(A::class);

$proxy = $reflector->newLazyProxy(function ($proxy) {
    return new A(1, $proxy);
});

print "Init\n";

$reflector->initializeLazyObject($proxy);

var_dump($proxy);

print "Reset\n";

$proxy = $reflector->resetAsLazyProxy($proxy, function () {
    return new A(2);
});

?>