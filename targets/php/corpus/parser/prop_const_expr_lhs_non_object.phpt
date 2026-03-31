<?php

const A_prop = (42)->prop;
var_dump(A_prop);

const A_prop_nullsafe = (42)?->prop;
var_dump(A_prop_nullsafe);

?>