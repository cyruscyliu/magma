<?php

class C {
    public $prop {
        set => $value;
    }
}

$nonLazy = new C;

$lazy = (new ReflectionClass(C::class))->newLazyProxy(function () {
    echo "init\n";
    return new C;
});

function foo(C $c) {
    $c->prop = 1;
    var_dump($c->prop);
}

foo($nonLazy);
foo($lazy);

?>