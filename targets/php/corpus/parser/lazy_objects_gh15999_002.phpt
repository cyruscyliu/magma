<?php

class C {
    public $s;
    public function __destruct() {
        var_dump(__METHOD__);
    }
}

print "# Ghost:\n";

$r = new ReflectionClass(C::class);

$o = $r->newLazyGhost(function ($obj) {
    global $p;
    $p = null;
});

$p = new stdClass;
var_dump($o->s = $p);
var_dump($o->s);

print "# Proxy:\n";

$r = new ReflectionClass(C::class);

$o = $r->newLazyProxy(function ($obj) {
    global $p;
    $p = null;
    return new C();
});

$p = new stdClass;
var_dump($o->s = $p);
var_dump($o->s);

?>
==DONE==