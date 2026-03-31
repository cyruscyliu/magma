<?php

class It implements \IteratorAggregate
{
    public function getIterator(): \Generator
    {
        yield 'foo';
        echo "baz\n";
        throw new \Exception();
    }

    public function __destruct()
    {
        throw new \Exception();
    }
}

function f() {
    var_dump(new stdClass, yield from new It());
}

$gen = f();

var_dump($gen->current());
$gen->next();

gc_collect_cycles();

?>
==DONE==