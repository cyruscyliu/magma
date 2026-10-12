<?php

function test1() {}
function test2() { return 42; }

var_dump(test1(...));
var_dump(test2(...));

?>