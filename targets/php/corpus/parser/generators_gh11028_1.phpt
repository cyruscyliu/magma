<?php
function generator($x) {
    try {
        yield $x => 0;
    } finally {
        return [];
    }
}

function test($msg, $x) {
    echo "yield $msg\n";
    try {
        var_dump([...generator($x)]);
    } catch (Throwable $e) {
        echo $e->getMessage(), "\n";
    }
}

test("null", null);
test("false", false);
test("true", true);
test("object", new stdClass);
?>