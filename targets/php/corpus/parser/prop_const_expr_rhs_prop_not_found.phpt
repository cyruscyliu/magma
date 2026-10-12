<?php

enum A {
    case B;
}

const A_prop = A::B->prop;
var_dump(A_prop);

const A_prop_nullsafe = A::B?->prop;
var_dump(A_prop_nullsafe);

?>