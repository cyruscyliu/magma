<?php

function _test(int $a): int {
    return $a + 1;
}

$res1 = 5 |> '_test';

var_dump($res1);
?>