<?php

$inputs = [
    0,
    null,
    false,
    true,
    "",
    [],
    NAN,
];

$nan = fdiv(0, 0);
var_dump($nan);
foreach ($inputs as $right) {
    echo 'Using ';
    var_export($right);
    echo ' as right op', PHP_EOL;
    var_dump($nan == $right);
    var_dump($nan != $right);
    var_dump($nan === $right);
    var_dump($nan !== $right);
    var_dump($nan < $right);
    var_dump($nan <= $right);
    var_dump($nan > $right);
    var_dump($nan >= $right);
    var_dump($nan <=> $right);
}

?>