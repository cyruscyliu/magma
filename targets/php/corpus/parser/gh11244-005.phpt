<?php

$data = [0, 1, 2];

foreach ($data as $key => &$value) {
    echo "$value\n";
    if ($value === 1) {
        $cow_copy = [$data, $data, $data];
        echo "unset $value\n";
        unset($cow_copy[0][$key]);
        unset($data[$key]);
        unset($cow_copy[2][$key]);
    }
}

print_r($cow_copy);

?>