<?php

$e = new Exception();
$a = new stdClass();
zend_weakmap_attach($e, $a);
unset($a);
$e2 = $e;
unset($e2); // add to roots
gc_collect_cycles();

?>
==DONE==