<?php

$values = [
    PHP_INT_MAX,
    (string)PHP_INT_MAX
];

foreach ($values as $var) {
    $var++;
    var_dump($var);
}
echo "Done\n";
?>