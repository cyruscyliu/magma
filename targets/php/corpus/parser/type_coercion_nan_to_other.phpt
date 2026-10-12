<?php

$nan = fdiv(0, 0);
var_dump($nan);

function implicit_to_bool(bool $v) {
    var_dump($v);
}
function implicit_to_string(string $v) {
    var_dump($v);
}

implicit_to_bool($nan);
implicit_to_string($nan);

var_dump((int) $nan);
var_dump((bool) $nan);
var_dump((string) $nan);
var_dump((array) $nan);
var_dump((object) $nan);

$types = [
    'null',
    'bool',
    'int',
    'string',
    'array',
    'object',
];

foreach ($types as $type) {
    $nan = fdiv(0, 0);
    settype($nan, $type);
    var_dump($nan);
}

?>