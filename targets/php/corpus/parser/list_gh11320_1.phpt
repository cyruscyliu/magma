<?php
$index = 1;
function getList() { return [2, 3]; }
var_dump([$index => list($x, $y) = getList()]);
var_dump([$index => [$x, $y] = getList()]);
?>