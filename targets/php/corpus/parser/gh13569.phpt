<?php

$wm = new WeakMap();
$objs = [];
for ($i = 0; $i < 30_000; $i++) {
    $objs[] = $obj = new stdClass;
    $wm[$obj] = $obj;
}

gc_collect_cycles();

$tmp = $wm;
$tmp = null;

gc_collect_cycles();
?>
==DONE==