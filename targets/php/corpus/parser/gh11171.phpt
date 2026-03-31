<?php
$all = ['test'];
foreach ($all as &$item) {
    $all += [$item];
}
var_dump($all);
?>