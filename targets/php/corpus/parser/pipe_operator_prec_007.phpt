<?php

$value = 42;
$value
    |> (fn ($x) => $x ?? throw new Exception('Value may not be null'))
    |> (fn ($x) => var_dump($x));

$value = null;
$value
    |> (fn ($x) => $x ?? throw new Exception('Value may not be null'))
    |> (fn ($x) => var_dump($x));

?>