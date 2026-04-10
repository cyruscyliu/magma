<?php

class Value {
    public function __construct() {
    }
}

$map = new WeakMap();
$obj = new Value();
$map[$obj] = [$obj, $map];
$ref = WeakReference::create($map);

$map = null;

gc_collect_cycles();

var_dump($ref->get());

?>