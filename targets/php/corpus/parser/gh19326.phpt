<?php

class It implements IteratorAggregate {
    public function getIterator(): Generator {
        yield "";
        Fiber::suspend();
    }
}

function g() {
    yield from new It();
}

$b = g();
$b->rewind();

$fiber = new Fiber(function () use ($b) {
    $b->next();
});

$fiber->start();

try {
    $b->throw(new Exception('test'));
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

$fiber->resume();

?>