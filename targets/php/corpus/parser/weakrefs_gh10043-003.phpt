<?php

class Value {
    public function __construct(public readonly string $value) {
    }
}

$map = new WeakMap();
$obj = new Value('a');
$map[$obj] = [$obj, $map];
$ref = WeakReference::create($map);

gc_collect_cycles();

var_dump($ref->get());

gc_collect_cycles();

// $obj is first in the root buffer
$obj = null;
$map = null;
gc_collect_cycles();

var_dump($ref->get());

?>