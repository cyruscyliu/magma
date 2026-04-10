<?php

class C {
    const Closure = strrev(...);
}

var_dump(C::Closure);
var_dump((C::Closure)("abc"));

?>