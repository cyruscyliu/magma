<?php

function test(
    Closure $name = strrev(...)
) {
    var_dump($name("abc"));
}

test();
test(strlen(...));

?>