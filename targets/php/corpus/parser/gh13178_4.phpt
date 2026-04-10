<?php
$array = ['foo'];
reset($array);
while (true) {
    $key = key($array);
    next($array);
    var_dump($key);
    unset($array[$key]);
    $array[] = 'foo';
    if ($key === 10) {
        break;
    }
}
?>