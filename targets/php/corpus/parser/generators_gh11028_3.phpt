<?php
function generator() {
    try {
        yield null => 0;
    } finally {
        throw new Exception("exception");
        return [];
    }
}

try {
    var_dump([...generator()]);
} catch (Throwable $e) {
    echo $e->getMessage(), "\n";
}
?>