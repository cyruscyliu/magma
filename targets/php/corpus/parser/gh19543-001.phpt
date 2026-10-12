<?php

$e = new Exception();
$a = new stdClass();
zend_weakmap_attach($e, $a);
unset($a);
gc_collect_cycles();

?>
==DONE==