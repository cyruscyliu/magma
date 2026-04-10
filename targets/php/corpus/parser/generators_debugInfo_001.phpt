<?php

function foo() {
    yield;
}

$gens = [
    (new class() {
        function a() {
            yield from foo();
        }
    })->a(),
    (function() {
        yield;
    })(),
    foo(),
];

foreach ($gens as $gen) {
    echo "Before:", PHP_EOL;
    var_dump($gen);

    foreach ($gen as $dummy) {
        echo "Inside:", PHP_EOL;
        var_dump($gen);
    }

    echo "After:", PHP_EOL;

    var_dump($gen);
}

?>