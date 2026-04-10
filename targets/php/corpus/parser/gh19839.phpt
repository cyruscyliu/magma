<?php

const X = 'x';

$x = null;
unset(${X});

$a = $GLOBALS;
sort($a);
serialize($a);

?>
===DONE===