<?php

try {
    $a = clone $b;
} catch (Error $e) {
    echo $e::class, ": ", $e->getMessage(), PHP_EOL;
}

?>