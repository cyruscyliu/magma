<?php
$obj = new stdClass;
$map = new WeakMap;
$integer = 1;
$map[$obj] = 0;
$map[$obj] =& $integer;
$integer++;
var_dump($map[$obj], $map->offsetGet($obj));
?>