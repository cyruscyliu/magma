<?php

class Vec {
    public function __construct(public float $x, public float $y, public float $z) {}
}

static $a = new Vec(x: 0.0, y: 1.0, z: 2.0);
var_dump($a);

static $b = new Vec(z: 0.0, y: 1.0, x: 2.0);
var_dump($b);

static $c = new Vec(0.0, z: 1.0, y: 2.0);
var_dump($c);

try {
    eval('static $d = new Vec(x: 0.0, x: 1.0);');
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>