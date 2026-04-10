<?php

class C {
    public int $a = 1;

    public function __destruct() {
        var_dump(__METHOD__, $this);
    }
}

function ghost() {
    $reflector = new ReflectionClass(C::class);

    print "# Ghost:\n";

    print "In makeLazy\n";
    $obj = $reflector->newLazyGhost(function () {
        var_dump("initializer");
    });
    print "After makeLazy\n";

    var_dump($obj->a);
}

function proxy() {
    $reflector = new ReflectionClass(C::class);

    print "# Proxy:\n";

    print "In makeLazy\n";
    $obj = $reflector->newLazyProxy(function () {
        var_dump("initializer");
        return new C();
    });
    print "After makeLazy\n";

    var_dump($obj->a);
}

ghost();
proxy();
