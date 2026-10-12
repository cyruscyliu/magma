<?php

class Value {
    public function __construct(public readonly string $value) {
    }
}

$map = new WeakMap();
$obj = new Value('a');
$map[$obj] = [$map, $obj];
$ref = WeakReference::create($map);

gc_collect_cycles();

var_dump($ref->get());

gc_collect_cycles();

// $map is first in the root buffer
$map = null;
$obj = null;
gc_collect_cycles();

var_dump($ref->get());

?>