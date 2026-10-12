<?php
try {
    assert(false && "Is this evaluated?");
} catch (Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
?>