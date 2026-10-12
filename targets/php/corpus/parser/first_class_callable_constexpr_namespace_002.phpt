<?php

namespace Foo;

const Closure = strrev(...);

var_dump(Closure);
var_dump((Closure)("abc"));

?>