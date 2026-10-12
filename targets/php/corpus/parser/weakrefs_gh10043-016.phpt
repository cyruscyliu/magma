<?php

class K1 { function __construct() {} }
class K2 {}

$map = new WeakMap();
$k1 = new K1();
$map[$k1] = [$k1, $map];

$k2 = new K2();
$map[$k2] = $k2;

gc_collect_cycles();

var_dump($map);
?>