<?php

$data = ["k" => 0, 1, 2, 3];
unset($data[1]);

foreach ($data as $key => &$value) {
    echo "$value\n";
    if ($value === 1) {
        $cow_copy = $data;
        echo "unset $value\n";
        unset($data[$key]);
    }
}

?>