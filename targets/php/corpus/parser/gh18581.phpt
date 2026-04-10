<?php

function g() {
    yield '100' => 'first';
    yield '101' => 'second';
    yield '102' => 'third';
    yield 'named' => 'fourth';
}

function test($x = null, $y = null, ...$z) {
    var_dump($x, $y, $z);
    var_dump($z[0]);
    var_dump($z['named']);
}

test(...g());

?>