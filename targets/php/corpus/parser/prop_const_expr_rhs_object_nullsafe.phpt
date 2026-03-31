<?php

class A {}
class B {}

const A_prop = (new A)?->{new B};

var_dump(A_prop);

?>