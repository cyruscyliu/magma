<?php

class C
{
    public $s;
}
$r = new ReflectionClass(C::class);
$o = $r->newLazyProxy(function () { return new C; });

// Comparison calls initializers, which releases $o
var_dump($o >
$r->newLazyGhost(function () {
    global $o;
    $o = null;
}));

?>