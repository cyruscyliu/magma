<?php

define('MESSAGE', 'value-' . (random_int(1, 2) == 1 ? 'a' : 'b'));

#[\Deprecated(MESSAGE)]
function test() {
}

test();

?>