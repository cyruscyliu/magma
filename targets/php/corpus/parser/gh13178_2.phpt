<?php
$array = [100 => 'foo'];
foreach ($array as $key => &$value) {
    var_dump($key);
    unset($array[$key]);
    $array[] = 'foo';
    if ($key === 110) {
        break;
    }
}
?>