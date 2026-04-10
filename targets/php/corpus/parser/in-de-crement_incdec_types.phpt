<?php

/* Type errors */
$types = [[], new stdClass(), fopen(__FILE__, 'r')];

foreach ($types as $type) {
    try {
        $type++;
    } catch (\TypeError $e) {
        echo $e->getMessage(), PHP_EOL;
    }
    try {
        $type--;
    } catch (\TypeError $e) {
        echo $e->getMessage(), PHP_EOL;
    }
}

echo "Using increment:\n";
$values = [null, false, true, 0, 0.0, '', ' ', '0'];
foreach ($values as $value) {
    echo "Initial value:";
    var_dump($value);
    $value++;
    echo "Result value:";
    var_dump($value);
}

echo "Using decrement:\n";
$values = [null, false, true, 0, 0.0, '', ' ', '0'];
foreach ($values as $value) {
    echo "Initial value:";
    var_dump($value);
    $value--;
    echo "Result value:";
    var_dump($value);
}
?>