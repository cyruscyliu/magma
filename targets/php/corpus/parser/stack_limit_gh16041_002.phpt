<?php

function map() {
    array_map('map', [1]);
}

try {
    map();
} catch (\Throwable $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

?>