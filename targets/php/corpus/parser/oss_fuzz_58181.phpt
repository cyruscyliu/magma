<?php
function test(array $data) {
    $iterator = new ArrayIterator($data);
    $iterator = new \CallbackFilterIterator($iterator, fn&() => true);
    $iterator->rewind();
}

test(['a', 'b']);
?>