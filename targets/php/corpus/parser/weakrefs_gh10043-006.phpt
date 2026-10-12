<?php

class Value {
    public function __construct(public readonly string $value) {
    }
}

$map = new WeakMap();
$obj = new Value('a');
$map[$obj] = $obj;

gc_collect_cycles();

$obj2 = $obj;
$obj = null;
$map2 = $map;
$map = null;

gc_collect_cycles();

var_dump($map2);

?>