<?php

class Value {
    public function __construct(public readonly string $value) {
    }
}

$map = new WeakMap();
$obj = new Value('a');
$value = [$obj];
$map[$obj] = $value;
$obj = null;

gc_collect_cycles();

var_dump($map);

gc_collect_cycles();

$value = null;

gc_collect_cycles();

var_dump($map);

?>