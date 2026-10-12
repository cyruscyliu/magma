<?php

namespace Foo;

const Closure = \Foo\strrev(...);

var_dump(Closure);
var_dump((Closure)("abc"));

?>