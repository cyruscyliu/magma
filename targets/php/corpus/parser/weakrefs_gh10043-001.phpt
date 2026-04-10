<?php

class Value {
    public function __construct(public readonly string $value) {
    }
}

$map = new WeakMap();
$obj = new Value('a');
$map[$obj] = $obj;

gc_collect_cycles();

var_dump($map);

$obj = null;
gc_collect_cycles();

var_dump($map);

?>