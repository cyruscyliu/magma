<?php
$closure = function() {
    return "OK";
};

$foo = $closure->__invoke(...);

echo $foo();
?>