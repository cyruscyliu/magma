<?php

$values = [
    -PHP_INT_MAX-1,
    (string)(-PHP_INT_MAX-1),
];

foreach ($values as $var) {
    $var--;
    var_dump($var);
}

echo "Done\n";
?>