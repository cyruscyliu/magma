<?php

class It implements \IteratorAggregate
{
    public function getIterator(): \Generator
    {
        yield 'foo';
        Fiber::suspend();
        var_dump("not executed");
    }
}

function f() {
    yield from new It();
}

function g() {
    yield from f();
}

function gen($gen) {
    /* $gen is an intermediate node and will not be marked with IN_FIBER */
    yield from $gen;
}

$g = g();
$a = gen($g);
$b = gen($g);
$c = gen($g);
$d = gen($g);
var_dump($a->current());
var_dump($b->current());

$fiber = new Fiber(function () use ($a, $b, $c, $d, $g) {
    $b->next();
    var_dump("not executed");
});

$ref = $fiber;

$fiber->start();

?>
==DONE==