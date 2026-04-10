<?php
try {
    $foo = clone(array());
} catch (Error $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}
?>