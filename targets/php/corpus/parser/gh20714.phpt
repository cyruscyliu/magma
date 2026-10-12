<?php

function gen(): Generator {
    try {
        yield 1;
    } finally {}
}

function process(): void {
    $g = gen();
    foreach ($g as $_) {
        throw new Exception('ERROR');
    }
}

try {
    process();
} catch (Exception $e) {
    echo "Caught\n";
}

?>