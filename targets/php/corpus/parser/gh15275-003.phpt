<?php

class It implements \IteratorAggregate
{
    public function getIterator(): \Generator
    {
        yield 'foo';
        throw new \Exception();
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

var_dump($gen->current());
$gen->next();

?>
==DONE==