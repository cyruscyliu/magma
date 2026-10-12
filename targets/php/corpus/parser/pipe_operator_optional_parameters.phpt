<?php

function _test(int $a, int $b = 3) {
    return $a + $b;
}

$res1 = 5 |> '_test';

var_dump($res1);
?>