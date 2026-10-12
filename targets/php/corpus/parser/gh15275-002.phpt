<?php

class It implements \IteratorAggregate
{
    public function getIterator(): \Generator
    {
        yield 'foo';
        try {
            Fiber::suspend();
        } finally {
            var_dump(__METHOD__);
        }
        var_dump("not executed");
    }
}

function f() {
    try {
        var_dump(new stdClass, yield from new It());
    } finally {
        var_dump(__FUNCTION__);
    }
}

function g() {
    try {
        var_dump(new stdClass, yield from f());
    } finally {
        var_dump(__FUNCTION__);
    }
}

$gen = g();

$fiber = new Fiber(function () use ($gen) {
    var_dump($gen->current());
    $gen->next();
    var_dump("not executed");
});

$ref = $fiber;

$fiber->start();

gc_collect_cycles();

?>
==DONE==