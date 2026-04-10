<?php
$a = [null];
$a[1] = $a[0]?->x;
var_dump($a);
?>