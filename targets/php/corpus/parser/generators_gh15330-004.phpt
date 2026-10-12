<?php

class Canary {
    public function __construct(public mixed $value) {}
    public function __destruct() {
        var_dump(__METHOD__);
    }
}

function g() {
    yield 'foo';
    Fiber::suspend();
}

function f($canary) {
    var_dump(yield from g());
}

$canary = new Canary(null);

$iterable = f($canary);

$fiber = new Fiber(function () use ($iterable, $canary) {
    var_dump($canary, $iterable->current());
    $iterable->next();
    var_dump("not executed");
});

$canary->value = $fiber;

$fiber->start();

$iterable->current();

$fiber = $iterable = $canary = null;

gc_collect_cycles();

?>
==DONE==