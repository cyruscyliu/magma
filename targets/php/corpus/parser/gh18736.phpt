<?php

function &test(): int {
    $x = 0;
    try {
        return $x;
    } finally {
        $x = 'test';
    }
}

try {
    $x = &test();
    var_dump($x);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>