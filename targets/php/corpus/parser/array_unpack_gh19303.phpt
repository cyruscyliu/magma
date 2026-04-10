<?php
$a = [0];
unset($a[0]);
var_dump([...$a]);
?>