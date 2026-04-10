<?php

function foo(callable $fn) {
    var_dump($fn);
}

$values = [
    'exit',
    'die',
    exit(...),
    die(...),
];

foreach ($values as $value) {
    foo($value);
}

?>