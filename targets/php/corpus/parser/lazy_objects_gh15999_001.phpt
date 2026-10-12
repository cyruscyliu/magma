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
    global $o;
    $o = null;
});
$p = new stdClass;

try {
    $o->s = $p;
} catch (Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

print "# Proxy:\n";

$o = $r->newLazyProxy(function ($obj) {
    global $o;
    $o = null;
    return new C();
});
$p = new stdClass;

try {
    $o->s = $p;
} catch (Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

print "# GC cycle:\n";

$o = $r->newLazyGhost(function ($obj) {
    global $o;
    $o->s = $o;
    $o = null;
    gc_collect_cycles();
});
$p = new stdClass;

$o->s = $p;
gc_collect_cycles();

print "# Nested error (ghost):\n";

$r = new ReflectionClass(C::class);

$o = $r->newLazyGhost(function ($obj) {
    global $o;
    $o = null;
    return new stdClass;
});
$p = new stdClass;

try {
    $o->s = $p;
} catch (Error $e) {
    do {
        printf("%s: %s\n", $e::class, $e->getMessage());
    } while ($e = $e->getPrevious());
}

print "# Nested error (proxy):\n";

$r = new ReflectionClass(C::class);

$o = $r->newLazyProxy(function ($obj) {
    global $o;
    $o = null;
    return new stdClass;
});
$p = new stdClass;

try {
    $o->s = $p;
} catch (Error $e) {
    do {
        printf("%s: %s\n", $e::class, $e->getMessage());
    } while ($e = $e->getPrevious());
}

?>
==DONE==