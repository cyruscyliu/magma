<?php
$array = ['foo'];
foreach ($array as $key => &$value) {
    var_dump($key);
    unset($array[$key]);
    $array[] = 'foo';
    if ($key === 10) {
        break;
    }
}
?>