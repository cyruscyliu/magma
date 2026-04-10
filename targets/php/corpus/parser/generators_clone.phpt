<?php

function gen() {
    yield;
}


try {
    $gen = gen();
    clone $gen;
} catch (Throwable $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>