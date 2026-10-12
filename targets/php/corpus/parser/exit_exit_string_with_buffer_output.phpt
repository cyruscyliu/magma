<?php

ob_start(function ($text) {
    fwrite(STDOUT, "Handler: " . $text);
    throw new Exception('test');
}, chunk_size: 10);

try {
    exit("Hello world!\n");
} catch (Throwable $e) {
    echo $e::class, ': ', $e->getMessage(), PHP_EOL;
}
echo "After?\n";

?>