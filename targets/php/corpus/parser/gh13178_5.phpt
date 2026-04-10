<?php
$array = [0, 1, 2];
foreach ($array as &$value) {
    var_dump($value);
    if ($value === 2) {
        unset($array[2]);
        unset($array[1]);
        $array[1] = 3;
        $array[2] = 4;
    }
}
?>